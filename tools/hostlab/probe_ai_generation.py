"""One-shot generation probe for the two configured AI endpoints.

Endpoints are hardcoded constants; only the API keys come from the environment.
Output contains status codes and redacted error excerpts, never key material.
"""
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request
import uuid

OUTPUT = Path("runtime/hostlab/probe")
ENDPOINTS = {
    "primary": ("https://opencode.ai/zen/go/v1/chat/completions", "glm-5.3-flash"),
    "backup": ("https://api.experientiallabs.ai/v1/chat/completions", "glm-5.3-flash"),
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def redact(text):
    for name in ("AI_API_KEY_PRIMARY", "AI_API_KEY_BACKUP"):
        value = os.environ.get(name)
        if value:
            text = text.replace(value, "[REDACTED]")
    return text


def probe(profile, max_tokens):
    key = os.environ.get("AI_API_KEY_" + profile.upper(), "")
    if not key:
        return {"profile": profile, "status": "configuration_incomplete"}
    url, model = ENDPOINTS[profile]
    payload = {"model": model, "messages": [{"role": "user", "content": "Reply with the single word: pong"}],
               "max_tokens": max_tokens, "stream": False}
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json",
               "User-Agent": "HostLab-Probe/1"}
    if profile == "primary":
        # OpenCode Go requires a stable x-opencode-session ID for routing and prompt caching.
        headers["x-opencode-session"] = "hostlab-probe-" + uuid.uuid4().hex[:24]
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    started = time.monotonic()
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=90) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
        seconds = round(time.monotonic() - started, 2)
        if len(raw) > 2 * 1024 * 1024:
            return {"profile": profile, "status": "response_exceeds_bound", "seconds": seconds}
        try:
            data = json.loads(redact(raw.decode("utf-8")))
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content")
            return {"profile": profile, "status": "completed", "seconds": seconds,
                    "reply_present": bool(content)}
        except ValueError:
            return {"profile": profile, "status": "malformed_json", "seconds": seconds}
    except urllib.error.HTTPError as exc:
        excerpt = ""
        try:
            excerpt = redact(exc.read(1000).decode("utf-8", errors="replace"))[:300]
        except Exception:
            pass
        return {"profile": profile, "status": "http_error", "code": exc.code,
                "seconds": round(time.monotonic() - started, 2), "body_excerpt": excerpt}
    except Exception as exc:
        return {"profile": profile, "status": "transport_error", "error": type(exc).__name__,
                "seconds": round(time.monotonic() - started, 2)}


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = {"schema": 1, "probes": []}
    for profile in ("primary", "backup"):
        for attempt, tokens in ((1, 16384), (2, 32768), (3, 49152)):
            result["probes"].append({"attempt": attempt, "max_tokens": tokens, **probe(profile, tokens)})
    (OUTPUT / "report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
