"""One bounded, observable API attempt. Retry and accounting belong to the ledger."""
from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import time
from email.utils import parsedate_to_datetime
import urllib.error
import urllib.parse
import urllib.request

MAX_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_EVENT_BYTES = 256 * 1024
MAX_TOOL_CALLS = 16


class ApiError(RuntimeError):
    def __init__(self, reason, kind="protocol", retryable=False, billing_unknown=True,
                 http_status=None, retry_after=None, metrics=None):
        super().__init__(reason)
        self.reason = reason
        self.kind = kind
        self.retryable = bool(retryable)
        self.billing_unknown = bool(billing_unknown)
        self.http_status = http_status
        self.retry_after = retry_after
        self.metrics = dict(metrics or {})


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def _redact(value):
    for name in ("AI_API_KEY_PRIMARY", "AI_API_KEY_BACKUP", "HF_TOKEN", "GH_TOKEN"):
        secret = os.environ.get(name)
        if secret:
            value = value.replace(secret, "[REDACTED]")
    return value


def _safe_usage(value, depth=0):
    # Usage is optional, never replace unavailable accounting with zero.
    if not isinstance(value, dict) or depth > 3 or len(value) > 64:
        return {}
    result = {}
    for key, item in value.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-zA-Z0-9_]{1,80}", key):
            continue
        if type(item) is int and item >= 0:
            result[key] = item
        elif isinstance(item, dict):
            result[key] = _safe_usage(item, depth + 1)
    return result


def _clean_message(message):
    if not isinstance(message, dict):
        raise ApiError("API message missing")
    content = message.get("content")
    if content is not None and not isinstance(content, str):
        raise ApiError("API content must be text")
    clean = {"role": "assistant", "content": _redact(content) if content is not None else None}
    calls = message.get("tool_calls", [])
    if not isinstance(calls, list) or len(calls) > MAX_TOOL_CALLS:
        raise ApiError("API tool calls exceed bound")
    if calls:
        result = []
        for call in calls:
            if not isinstance(call, dict) or not isinstance(call.get("function"), dict):
                raise ApiError("API tool call malformed")
            function = call["function"]
            if (not isinstance(call.get("id"), str) or not call["id"] or len(call["id"]) > 256
                    or call.get("type", "function") != "function"
                    or not isinstance(function.get("name"), str)
                    or not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", function["name"])
                    or not isinstance(function.get("arguments"), str)
                    or len(function["arguments"]) > MAX_EVENT_BYTES):
                raise ApiError("API tool call malformed")
            result.append({"id": _redact(call["id"]), "type": "function", "function": {
                "name": function["name"], "arguments": _redact(function["arguments"])}})
        if len({call["id"] for call in result}) != len(result):
            raise ApiError("API tool call IDs duplicated")
        clean["tool_calls"] = result
    if not calls and not content:
        raise ApiError("API returned no usable output")
    return clean


def _socket_timeout(response, timeout):
    # urllib retains proxy/CA compatibility; HTTPResponse.read1 performs at most
    # one underlying read, so even a slow drip cannot extend the total deadline.
    stream = getattr(response, "fp", None)
    raw = getattr(stream, "raw", None)
    sock = getattr(raw, "_sock", None)
    if sock is not None:
        sock.settimeout(timeout)


def _retry_after(headers):
    value = headers.get("Retry-After", "") if headers else ""
    if re.fullmatch(r"\d+(?:\.\d+)?", value):
        return min(60.0, max(0.0, float(value)))
    try:
        return min(60.0, max(0.0, parsedate_to_datetime(value).timestamp()-time.time()))
    except (ValueError, TypeError, OverflowError):
        return None


def _call_api(profile, messages, tools, force_tool=None, session_id=None, *,
             max_output=8192, total_timeout=240, idle_timeout=45, stream=True):
    started = time.monotonic()
    metrics = {"streaming": bool(stream), "response_bytes": 0, "events": 0,
               "headers_ms": None, "first_event_ms": None, "first_visible_delta_ms": None}

    def elapsed():
        return round((time.monotonic() - started) * 1000, 3)

    def fail(reason, kind="protocol", retryable=False):
        raise ApiError(reason, kind, retryable, True, metrics=dict(metrics, total_ms=elapsed()))

    name = str(profile).upper()
    key = os.environ.get("AI_API_KEY_" + name, "")
    base = os.environ.get("AI_" + name + "_BASE_URL", "").rstrip("/")
    model = os.environ.get("AI_" + name + "_MODEL", "")
    parsed = urllib.parse.urlsplit(base)
    if (name not in {"PRIMARY", "BACKUP"} or not key or not model or len(model) > 256
            or parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment
            or type(max_output) is not int or not 1 <= max_output <= 65536
            or not 0 < idle_timeout <= total_timeout <= 600
            or (session_id is not None and not re.fullmatch(r"[a-zA-Z0-9_-]{1,128}", session_id))):
        raise ApiError("API configuration incomplete or invalid", "configuration", False, False)
    payload = {"model": model, "messages": messages, "tools": tools,
               "tool_choice": {"type": "function", "function": {"name": force_tool}} if force_tool else "auto",
               "max_tokens": max_output, "stream": bool(stream)}
    if stream:
        payload["stream_options"] = {"include_usage": True}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(body) > 2 * 1024 * 1024:
        raise ApiError("API request exceeds bound", "configuration", False, False)
    metrics["request_bytes"] = len(body)
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json",
               "Accept": "text/event-stream, application/json", "User-Agent": "HostLab-AIReview/2"}
    if session_id:
        headers["x-opencode-session"] = session_id
    request = urllib.request.Request(base + "/chat/completions", data=body, headers=headers)
    deadline = started + total_timeout
    usage = {}
    response_model = model
    finish_reason = None
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=min(90, total_timeout)) as response:
            metrics["headers_ms"] = elapsed()
            is_sse = "text/event-stream" in response.headers.get("Content-Type", "").lower()
            metrics["streaming"] = is_sse
            raw_json = bytearray()
            pending = bytearray()
            event = []
            event_bytes = 0
            content = []
            calls = {}
            done = False

            def handle_event():
                nonlocal usage, response_model, finish_reason, done
                if not event:
                    return
                text = b"\n".join(event).decode("utf-8")
                if text.strip() == "[DONE]":
                    done = True
                    return
                data = json.loads(text)
                if not isinstance(data, dict) or data.get("error"):
                    fail("API stream error", "provider", True)
                metrics["events"] += 1
                if metrics["first_event_ms"] is None:
                    metrics["first_event_ms"] = elapsed()
                if isinstance(data.get("model"), str) and 0 < len(data["model"]) <= 256:
                    response_model = _redact(data["model"])
                if isinstance(data.get("usage"), dict) and data["usage"]:
                    usage = _safe_usage(data["usage"])
                choices = data.get("choices", [])
                if not isinstance(choices, list) or len(choices) > 1:
                    fail("API choices malformed")
                if not choices:
                    return
                choice = choices[0]
                if not isinstance(choice, dict) or choice.get("index", 0) != 0:
                    fail("API choice index malformed")
                if choice.get("finish_reason") is not None:
                    finish_reason = choice["finish_reason"]
                delta = choice.get("delta", {})
                if not isinstance(delta, dict):
                    fail("API delta malformed")
                if delta.get("content") is not None:
                    if not isinstance(delta["content"], str):
                        fail("API content delta malformed")
                    content.append(delta["content"])
                fragments = delta.get("tool_calls", [])
                if not isinstance(fragments, list) or len(fragments) > MAX_TOOL_CALLS:
                    fail("API tool delta malformed")
                if (delta.get("content") or fragments) and metrics["first_visible_delta_ms"] is None:
                    metrics["first_visible_delta_ms"] = elapsed()
                for fragment in fragments:
                    if not isinstance(fragment, dict) or type(fragment.get("index")) is not int:
                        fail("API tool index malformed")
                    index = fragment["index"]
                    if not 0 <= index < MAX_TOOL_CALLS:
                        fail("API tool index exceeds bound")
                    call = calls.setdefault(index, {"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
                    function = fragment.get("function", {})
                    if not isinstance(function, dict) or fragment.get("type", "function") != "function":
                        fail("API tool delta malformed")
                    for owner, field, value in ((call, "id", fragment.get("id")),
                                                (call["function"], "name", function.get("name")),
                                                (call["function"], "arguments", function.get("arguments"))):
                        if value is not None:
                            if not isinstance(value, str):
                                fail("API tool fragment must be text")
                            owner[field] += value
                            if len(owner[field]) > MAX_EVENT_BYTES:
                                fail("API tool fragment exceeds bound")

            while not done:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    fail("API total deadline exceeded", "timeout", True)
                _socket_timeout(response, min(idle_timeout, remaining))
                chunk = response.read1(8192)
                if time.monotonic() > deadline:
                    fail("API total deadline exceeded", "timeout", True)
                if not chunk:
                    break
                metrics["response_bytes"] += len(chunk)
                if metrics["response_bytes"] > MAX_RESPONSE_BYTES:
                    fail("API response exceeds bound")
                if not is_sse:
                    raw_json.extend(chunk)
                    continue
                pending.extend(chunk)
                while b"\n" in pending and not done:
                    line, _, tail = pending.partition(b"\n")
                    pending = bytearray(tail)
                    line = line.rstrip(b"\r")
                    if len(line) > MAX_EVENT_BYTES:
                        fail("API stream line exceeds bound")
                    if not line:
                        handle_event()
                        event = []
                        event_bytes = 0
                    elif line.startswith(b"data:"):
                        value = line[5:]
                        if value.startswith(b" "):
                            value = value[1:]
                        event.append(value)
                        event_bytes += len(value) + 1
                        if event_bytes > MAX_EVENT_BYTES:
                            fail("API stream event exceeds bound")
                if len(pending) > MAX_EVENT_BYTES:
                    fail("API stream line exceeds bound")
            if is_sse:
                if not done:
                    fail("API stream interrupted before DONE", "interrupted", True)
                if finish_reason not in {"stop", "tool_calls"}:
                    fail("API output incomplete", "incomplete", True)
                message = {"content": "".join(content) or None,
                           "tool_calls": [calls[index] for index in sorted(calls)]}
            else:
                data = json.loads(raw_json.decode("utf-8"))
                if not isinstance(data, dict) or not isinstance(data.get("choices"), list) or len(data["choices"]) != 1:
                    fail("API response envelope malformed")
                choice = data["choices"][0]
                finish_reason = choice.get("finish_reason")
                if finish_reason not in {"stop", "tool_calls"}:
                    fail("API output incomplete", "incomplete", True)
                message = choice.get("message")
                usage = _safe_usage(data.get("usage"))
                if isinstance(data.get("model"), str) and 0 < len(data["model"]) <= 256:
                    response_model = _redact(data["model"])
            clean = _clean_message(message)
            offered = {item.get("function", {}).get("name") for item in tools if isinstance(item, dict)}
            if offered and any(call["function"]["name"] not in offered for call in clean.get("tool_calls", [])):
                fail("API returned an unavailable tool")
            if any(_redact(call["function"]["name"]) != call["function"]["name"] for call in clean.get("tool_calls", [])):
                fail("API returned an invalid tool name")
            known_usage = any(type(usage.get(key)) is int and usage[key] > 0
                              for key in ("total_tokens", "prompt_tokens", "completion_tokens", "input_tokens", "output_tokens"))
            metrics.update(total_ms=elapsed(), finish_reason=finish_reason, usage_received=known_usage)
            return clean, dict(usage, _transport=metrics, _usage_unknown=not known_usage), response_model
    except ApiError as exc:
        if not exc.metrics:
            exc.metrics = dict(metrics, total_ms=elapsed())
        raise
    except urllib.error.HTTPError as exc:
        status = exc.code
        retry_after = _retry_after(exc.headers)
        exc.close()
        raise ApiError("API HTTP " + str(status), "http", status in {408, 409, 425, 429, 500, 502, 503, 504},
                       True, status, retry_after, dict(metrics, total_ms=elapsed())) from None
    except (TimeoutError, socket.timeout):
        fail("API timeout", "timeout", True)
    except (urllib.error.URLError, OSError):
        fail("API connection interrupted", "network", True)
    except (ValueError, TypeError, KeyError, UnicodeError):
        fail("API response malformed", "protocol", False)


def call_api(profile, messages, tools, force_tool=None, session_id=None, *,
             max_output=8192, total_timeout=240, idle_timeout=45, stream=True):
    """Isolate DNS/TLS/headers too: terminate and reap a stalled single-POST worker.

    Private messages travel through pipes only. A killed request remains potentially
    billed; neither this worker nor its parent retries a POST.
    """
    if (type(total_timeout) not in {int, float} or type(idle_timeout) not in {int, float}
            or not 0 < idle_timeout <= total_timeout <= 600):
        raise ApiError("API timeout configuration invalid", "configuration", False, False)
    envelope = {"profile": profile, "messages": messages, "tools": tools, "force_tool": force_tool,
                "session_id": session_id, "max_output": max_output, "total_timeout": total_timeout,
                "idle_timeout": idle_timeout, "stream": stream}
    raw = json.dumps(envelope, ensure_ascii=False, separators=(",", ":")).encode()
    if len(raw) > 2 * 1024 * 1024:
        raise ApiError("API request exceeds bound", "configuration", False, False)
    started = time.monotonic()
    try:
        worker = subprocess.Popen([sys.executable, "-u", os.path.abspath(__file__), "--worker"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except OSError:
        raise ApiError("API worker could not start", "configuration", False, False) from None
    try:
        output, _ = worker.communicate(raw, timeout=max(.001, total_timeout-(time.monotonic()-started)))
    except subprocess.TimeoutExpired:
        worker.kill()
        worker.communicate(timeout=10)
        raise ApiError("API total deadline exceeded", "timeout", True, True,
                       metrics={"total_ms": round((time.monotonic()-started)*1000, 3), "worker_terminated": True}) from None
    if worker.returncode or len(output) > MAX_RESPONSE_BYTES:
        raise ApiError("API worker interrupted", "interrupted", True, True)
    try:
        value = json.loads(output)
        if "error" in value:
            error = value["error"]
            raise ApiError(error["reason"], error["kind"], error["retryable"], error["billing_unknown"],
                           error.get("http_status"), error.get("retry_after"), error.get("metrics"))
        message, usage, model = value["result"]
        usage["_transport"]["wall_ms"] = round((time.monotonic()-started)*1000, 3)
        return message, usage, model
    except (ValueError, TypeError, KeyError):
        raise ApiError("API worker response malformed", "protocol", False, True) from None


if __name__ == "__main__":
    try:
        if sys.argv[1:] != ["--worker"]:
            raise ApiError("API worker invocation invalid", "configuration", False, False)
        raw = sys.stdin.buffer.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ApiError("API worker input exceeds bound", "configuration", False, False)
        result = {"result": _call_api(**json.loads(raw))}
    except ApiError as error:
        result = {"error": {key: getattr(error, key) for key in (
            "reason", "kind", "retryable", "billing_unknown", "http_status", "retry_after", "metrics")}}
    except Exception:
        result = {"error": {"reason": "API worker failed", "kind": "protocol",
                            "retryable": False, "billing_unknown": True}}
    sys.stdout.write(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
