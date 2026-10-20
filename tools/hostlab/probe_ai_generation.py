"""Three dependent synthetic generation checks; no source or tool execution."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

from check_ai_connectivity import NoRedirect, MAX_ERROR_BYTES, configuration, credential_shape, error_summary, safe_request_id
from ai_transport import request_interval, _retry_after, select_tools

OUTPUT = Path(__file__).resolve().parents[2] / "runtime/hostlab/probe"
STAGES = (("minimal_chat", 128), ("stream", 1024), ("forced_tool", 1024))
TOTAL_TIMEOUT = 180
STAGE_TIMEOUT = 50
MAX_RESPONSE_BYTES = 256 * 1024
MAX_EVENT_BYTES = 64 * 1024
TOOL_NAME = "hostlab_probe_echo"
USAGE_KEYS = frozenset({"prompt_tokens", "completion_tokens", "total_tokens", "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"})
USAGE_DETAILS = frozenset({"prompt_tokens_details", "completion_tokens_details", "input_tokens_details", "output_tokens_details"})


def safe_usage(value):
    if not isinstance(value, dict):
        return {}
    result = {key: item for key, item in value.items() if key in USAGE_KEYS and type(item) is int and 0 <= item <= 10**9}
    for key in USAGE_DETAILS:
        row = value.get(key)
        if isinstance(row, dict):
            result[key] = {name: item for name, item in row.items() if name in USAGE_KEYS and type(item) is int and 0 <= item <= 10**9}
    return result


def payload(config, stage, include_usage):
    tokens = dict(STAGES)[stage]
    body = {"model": config["model"], "messages": [{"role": "user", "content": "Reply with exactly the single word pong, without punctuation."}], config.get("output_token_parameter", "max_tokens"): tokens, "stream": stage == "stream"}
    if config["endpoint"]["host"] == "api.river.ai" and config["model"].startswith("deepseek-ai/"):
        body["reasoning_effort"] = "none"
    if stage == "stream" and include_usage:
        body["stream_options"] = {"include_usage": True}
    if stage == "forced_tool":
        body["messages"] = [{"role": "user", "content": "Call hostlab_probe_echo exactly once with ok=true. Do not add text."}]
        body["tools"] = [{"type": "function", "function": {"name": TOOL_NAME, "description": "Return a synthetic diagnostic marker. This probe never executes this tool.", "parameters": {"type": "object", "properties": {"ok": {"type": "boolean", "enum": [True]}}, "required": ["ok"], "additionalProperties": False}}}]
        body["tools"], body["tool_choice"] = select_tools(body["tools"], TOOL_NAME, config.get("tool_choice_mode", "named"))
    return body


def _socket_timeout(response, remaining):
    raw = getattr(getattr(response, "fp", None), "raw", None)
    sock = getattr(raw, "_sock", None)
    if sock is not None:
        sock.settimeout(min(15, max(.001, remaining)))


def read_response(response, deadline, started):
    streaming = "text/event-stream" in response.headers.get("Content-Type", "").lower()
    raw = bytearray()
    ttfb = None
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError()
        _socket_timeout(response, remaining)
        chunk = response.read1(8192)
        if time.monotonic() > deadline:
            raise TimeoutError()
        if not chunk:
            break
        if ttfb is None:
            ttfb = round((time.monotonic() - started) * 1000, 3)
        raw.extend(chunk)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("response_bound")
        if streaming and re.search(rb"(?:^|\n)data: ?\[DONE\]\r?\n(?:\r?\n|$)", raw):
            break
    if not streaming:
        data = json.loads(raw)
        if not isinstance(data, dict) or data.get("error"):
            raise ValueError("invalid_envelope")
        choices = data.get("choices")
        if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
            raise ValueError("invalid_choice")
        choice = choices[0]
        message = choice.get("message")
        return message, choice.get("finish_reason"), safe_usage(data.get("usage")), False, ttfb
    content = []
    calls = {}
    usage = {}
    finish = None
    done = False
    for event in re.split(rb"\r?\n\r?\n", raw):
        if len(event) > MAX_EVENT_BYTES:
            raise ValueError("event_bound")
        parts = [line[5:].lstrip(b" ") for line in event.splitlines() if line.startswith(b"data:")]
        if not parts:
            continue
        value = b"\n".join(parts)
        if value.strip() == b"[DONE]":
            done = True
            break
        data = json.loads(value)
        if not isinstance(data, dict) or data.get("error"):
            raise ValueError("invalid_event")
        if isinstance(data.get("usage"), dict):
            usage = safe_usage(data["usage"])
        choices = data.get("choices", [])
        if not isinstance(choices, list) or len(choices) > 1:
            raise ValueError("invalid_choice")
        if not choices:
            continue
        choice = choices[0]
        if not isinstance(choice, dict) or choice.get("index", 0) != 0:
            raise ValueError("invalid_choice")
        if choice.get("finish_reason") is not None:
            finish = choice["finish_reason"]
        delta = choice.get("delta", {})
        if not isinstance(delta, dict):
            raise ValueError("invalid_delta")
        if delta.get("content") is not None:
            if not isinstance(delta["content"], str):
                raise ValueError("invalid_content")
            content.append(delta["content"])
        fragments = delta.get("tool_calls", [])
        if not isinstance(fragments, list) or len(fragments) > 1:
            raise ValueError("invalid_tools")
        for fragment in fragments:
            if not isinstance(fragment, dict) or fragment.get("index") != 0:
                raise ValueError("invalid_tool_index")
            call = calls.setdefault(0, {"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
            function = fragment.get("function", {})
            if not isinstance(function, dict) or fragment.get("type", "function") != "function":
                raise ValueError("invalid_tool")
            for owner, field, value in ((call, "id", fragment.get("id")), (call["function"], "name", function.get("name")), (call["function"], "arguments", function.get("arguments"))):
                if value is not None:
                    if not isinstance(value, str):
                        raise ValueError("invalid_fragment")
                    owner[field] += value
    if not done:
        raise ValueError("stream_incomplete")
    return {"content": "".join(content), "tool_calls": list(calls.values())}, finish, usage, True, ttfb


def validate(stage, message, finish, streaming):
    checks = {"complete_finish": finish == ("tool_calls" if stage == "forced_tool" else "stop"), "stream_matches": streaming == (stage == "stream"), "synthetic_output": False, "tool_executed": False}
    if not isinstance(message, dict):
        return checks
    if stage != "forced_tool":
        content = message.get("content")
        checks["synthetic_output"] = isinstance(content, str) and content.strip().lower() == "pong" and not message.get("tool_calls")
    else:
        calls = message.get("tool_calls")
        if isinstance(calls, list) and len(calls) == 1 and isinstance(calls[0], dict):
            call = calls[0]
            function = call.get("function", {})
            if isinstance(function, dict) and function.get("name") == TOOL_NAME and isinstance(call.get("id"), str) and 0 < len(call["id"]) <= 256 and call.get("type", "function") == "function":
                try:
                    args = json.loads(function.get("arguments", ""))
                    checks["synthetic_output"] = isinstance(args, dict) and set(args) == {"ok"} and args["ok"] is True
                except (ValueError, TypeError):
                    pass
    return checks


def attempt(profile, stage, timeout, include_usage=True):
    started = time.monotonic()
    result = {"stage": stage, "status": "failed", "billing_unknown": True, "usage": {}, "ttfb_ms": None, "finish_reason": None, "validation": {}}
    try:
        config = configuration(profile)
        if credential_shape(config["key"])["control"]:
            return dict(result, status="configuration_failed", billing_unknown=False)
        result["model"] = config["model"]
        headers = {"Authorization": "Bearer " + config["key"], "Content-Type": "application/json", "Accept": "text/event-stream, application/json", "User-Agent": "HostLab-Probe/2"}
        if config["endpoint"]["host"] == "opencode.ai":
            headers["x-opencode-session"] = "hostlab-probe-" + uuid.uuid4().hex[:24]
        request = urllib.request.Request(config["base"] + "/chat/completions", data=json.dumps(payload(config, stage, include_usage)).encode(), headers=headers)
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=min(15, timeout)) as response:
            result["http"] = response.status
            result["headers_ms"] = round((time.monotonic() - started) * 1000, 3)
            result["request_id"] = safe_request_id(response.headers)
            message, finish, usage, streaming, ttfb = read_response(response, started + timeout, started)
        checks = validate(stage, message, finish, streaming)
        safe_finish = finish if finish in {"stop", "tool_calls", "length", "content_filter", "function_call"} else "unrecognized"
        complete = all(checks[key] for key in ("complete_finish", "stream_matches", "synthetic_output"))
        known_usage = any(type(usage.get(key)) is int and usage[key] > 0 for key in ("prompt_tokens", "completion_tokens", "total_tokens", "input_tokens", "output_tokens"))
        result.update(status="complete" if complete else "incomplete", usage=usage, billing_unknown=not known_usage, ttfb_ms=ttfb, finish_reason=safe_finish, validation=checks)
    except urllib.error.HTTPError as exc:
        result["headers_ms"] = round((time.monotonic() - started) * 1000, 3)
        try:
            detail = error_summary(exc.code, exc.read(MAX_ERROR_BYTES), exc.headers)
        except (OSError, ValueError):
            detail = error_summary(exc.code, b"", exc.headers)
        finally:
            exc.close()
        result.update(status="auth_failed" if exc.code in (401, 403) else "capability_unknown" if exc.code in (400, 422) else "http_failed", http=exc.code, retry_after_seconds=_retry_after(exc.headers), **detail)
    except (TimeoutError, urllib.error.URLError, OSError):
        result["status"] = "transport_unknown"
    except (ValueError, TypeError, KeyError, UnicodeError):
        result["status"] = "protocol_unknown"
    result["total_ms"] = round((time.monotonic() - started) * 1000, 3)
    return result


def run_worker(profile, stage, timeout, include_usage):
    started = time.monotonic()
    envelope = json.dumps({"profile": profile, "stage": stage, "timeout": timeout, "include_usage": include_usage}).encode()
    try:
        worker = subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--worker"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except OSError:
        return {"stage": stage, "status": "worker_unavailable", "billing_unknown": False}
    try:
        raw, _ = worker.communicate(envelope, timeout=max(.001, timeout - (time.monotonic() - started)))
    except subprocess.TimeoutExpired:
        worker.kill()
        worker.communicate(timeout=5)
        return {"stage": stage, "status": "deadline_unknown", "billing_unknown": True, "worker_terminated": True, "wall_ms": round((time.monotonic() - started) * 1000, 3)}
    try:
        if worker.returncode or len(raw) > 16384:
            raise ValueError("worker_output_invalid")
        value = json.loads(raw)
        if not isinstance(value, dict) or value.get("stage") != stage:
            raise ValueError("worker_output_invalid")
        value["wall_ms"] = round((time.monotonic() - started) * 1000, 3)
        return value
    except (ValueError, TypeError):
        return {"stage": stage, "status": "worker_unknown", "billing_unknown": True}


def save_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def run(output=None):
    output = OUTPUT if output is None else output
    selection = os.environ.get("HOSTLAB_PROBE_PROFILE", "primary").lower()
    include_usage = os.environ.get("HOSTLAB_PROBE_INCLUDE_USAGE", "true").lower()
    report = {"schema": 2, "mode": "bounded_synthetic_generation", "status": "failed", "new_model_requests": 0, "tool_execution_enabled": False, "source_sent": False, "profiles": []}
    if selection not in {"primary", "backup", "all"} or include_usage not in {"true", "false"}:
        return dict(report, reason="invalid_probe_selection")
    output.mkdir(parents=True, exist_ok=True)
    ledger_path = output / "ledger.json"
    started = time.monotonic()
    deadline = started + TOTAL_TIMEOUT
    ledger = {"schema": 1, "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "total_timeout_seconds": TOTAL_TIMEOUT, "max_requests_per_profile": 3, "attempts": []}
    try:
        with ledger_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(ledger, indent=2) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        return dict(report, reason="existing_ledger_no_automatic_replay")
    for profile in (("primary", "backup") if selection == "all" else (selection,)):
        previous_started = 0
        item = {"profile": profile, "status": "failed", "stages": [], "credential_shape": credential_shape(os.environ.get("AI_API_KEY_" + profile.upper(), ""))}
        report["profiles"].append(item)
        try:
            config = configuration(profile)
            item["model"] = config["model"]
        except ValueError:
            item["reason"] = "configuration_invalid"
            continue
        for stage, tokens in STAGES:
            delay = max(0, previous_started+request_interval(profile)-time.monotonic()) if previous_started else 0
            if deadline-time.monotonic()-5 <= delay:
                item["reason"] = "total_deadline_exceeded"
                break
            time.sleep(delay)
            remaining = deadline - time.monotonic() - 5  # Reserve bounded worker reap time.
            if remaining <= 0:
                item["reason"] = "total_deadline_exceeded"
                break
            claim = {"profile": profile, "stage": stage, "model": config["model"], "max_tokens": tokens, "status": "pending", "billing_unknown": True}
            ledger["attempts"].append(claim)
            save_json(ledger_path, ledger)
            remaining = deadline - time.monotonic() - 5
            if remaining <= 0:
                claim.update(status="not_started_deadline", billing_unknown=False)
                save_json(ledger_path, ledger)
                item["reason"] = "total_deadline_exceeded"
                break
            report["new_model_requests"] += 1
            previous_started = time.monotonic()
            result = run_worker(profile, stage, min(STAGE_TIMEOUT, remaining), include_usage == "true")
            claim.update(status=result["status"], billing_unknown=result.get("billing_unknown", True), result=result)
            save_json(ledger_path, ledger)
            item["stages"].append(result)
            save_json(output / "report.json", report)
            if result["status"] != "complete":
                item["reason"] = "dependent_stage_not_complete"
                break
        if len(item["stages"]) == len(STAGES) and all(stage["status"] == "complete" for stage in item["stages"]):
            item["status"] = "complete"
    report["status"] = "complete" if report["profiles"] and all(item["status"] == "complete" for item in report["profiles"]) else "failed"
    report["runtime_seconds"] = round(time.monotonic() - started, 3)
    report["accounting_scope"] = "claimed single-POST attempts; a worker may fail before sending"
    ledger["status"] = report["status"]
    save_json(ledger_path, ledger)
    return report


def main():
    if sys.argv[1:] == ["--worker"]:
        try:
            value = json.loads(sys.stdin.buffer.read(8193))
            if (value.get("profile") not in {"primary", "backup"} or value.get("stage") not in dict(STAGES)
                    or type(value.get("include_usage")) is not bool or type(value.get("timeout")) not in (int, float) or not 0 < value["timeout"] <= TOTAL_TIMEOUT):
                raise ValueError("invalid_worker_input")
            result = attempt(**value)
        except Exception:
            result = {"status": "worker_unknown", "billing_unknown": True}
        print(json.dumps(result, separators=(",", ":")))
        return 0
    if sys.argv[1:]:
        print(json.dumps({"schema": 2, "status": "failed", "reason": "invalid_invocation"}))
        return 2
    try:
        report = run()
    except Exception:
        report = {"schema": 2, "status": "failed", "reason": "diagnostic_failed", "billing_unknown": True}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    save_json(OUTPUT / "report.json", report)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
