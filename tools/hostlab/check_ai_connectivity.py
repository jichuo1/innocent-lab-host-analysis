"""Catalog diagnostics with public fixed outcomes; never emit credentials or bodies."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

MAX_ERROR_BYTES = 4096
MAX_CATALOG_BYTES = 1024 * 1024
KNOWN_CODES = frozenset({"invalid_api_key", "invalid_key", "invalid_token", "authentication_error", "token_expired", "api_key_expired", "expired_api_key", "revoked_api_key", "permission_denied", "access_denied", "model_access_denied", "insufficient_permissions", "invalid_request_error", "unsupported_parameter", "model_not_found", "insufficient_quota"})


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def credential_shape(key):
    return {"present": bool(key), "padding": key != key.strip(),
            "control": any(unicodedata.category(c) in {"Cc", "Cf"} for c in key),
            "bearer_prefix": key.lstrip().lower().startswith("bearer "),
            "quoted": key.strip().startswith(('"', "'", "“", "‘")) or key.strip().endswith(('"', "'", "”", "’")),
            "river_example_prefix": key.strip().startswith("rv_")}


def _secrets():
    return tuple({value for name in ("AI_API_KEY_PRIMARY", "AI_API_KEY_BACKUP")
                  for value in (os.environ.get(name, ""), os.environ.get(name, "").strip()) if value})


def safe_request_id(headers):
    value = headers.get("x-request-id", "") if headers else ""
    if (not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", value)
            or any(secret in value for secret in _secrets())
            or re.search(r"(?:rv_|sk-|sk_|gh[pousr]_)", value)):
        return None
    return value


def error_summary(status, raw, headers=None):
    """Inspect <=4 KiB in memory; only enumerated labels may escape."""
    code = None
    text = ""
    try:
        data = json.loads(raw[:MAX_ERROR_BYTES])
        row = data.get("error", data) if isinstance(data, dict) else {}
        if isinstance(row, dict):
            value = row.get("code", row.get("type"))
            if isinstance(value, str) and value in KNOWN_CODES:
                code = value
            if isinstance(row.get("message"), str):
                text = row["message"].lower()
    except (ValueError, UnicodeError):
        pass
    category = "unclassified"
    if status in (401, 403):
        if code in {"token_expired", "api_key_expired", "expired_api_key", "revoked_api_key"} or "expired" in text or "revoked" in text:
            category = "expired_or_revoked"
        elif code in {"permission_denied", "access_denied", "model_access_denied", "insufficient_permissions"} or any(token in text for token in ("model access", "account access", "not permitted", "permission denied", "not authorized for", "no access")):
            category = "account_or_model_access"
        elif code in {"invalid_api_key", "invalid_key", "invalid_token"} or any(token in text for token in ("invalid api key", "invalid api-key", "invalid key", "invalid token", "incorrect api key")):
            category = "invalid_key"
    return {"classification": category, "code": code, "request_id": safe_request_id(headers)}


def configuration(profile):
    import ai_transport
    name = str(profile).upper()
    if name not in {"PRIMARY", "BACKUP"}:
        raise ValueError("invalid_profile")
    key = os.environ.get("AI_API_KEY_" + name, "")
    base = os.environ.get("AI_" + name + "_BASE_URL", "").strip().rstrip("/")
    model = os.environ.get("AI_" + name + "_MODEL", "").strip()
    if not key or not base or not model:
        raise ValueError("configuration_incomplete")
    try:
        base = ai_transport.chat_base_url(base)
        token_parameter = ai_transport.output_token_parameter(profile, base)
    except ai_transport.ApiError:
        raise ValueError("invalid_configuration") from None
    try:
        parsed = urllib.parse.urlsplit(base)
        valid = (parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password
                 and not parsed.query and not parsed.fragment and parsed.port in (None, 443)
                 and re.fullmatch(r"[A-Za-z0-9/_.~-]{0,256}", parsed.path)
                 and re.fullmatch(r"[A-Za-z0-9._:/-]{1,150}", model)
                 and not any(secret in base or secret in model for secret in _secrets()))
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("invalid_configuration")
    try:
        mode = ai_transport.tool_choice_mode(profile)
    except ai_transport.ApiError:
        raise ValueError("invalid_configuration") from None
    return {"key": key, "base": base, "model": model, "output_token_parameter": token_parameter, "tool_choice_mode": mode,
            "endpoint": {"scheme": "https", "host": parsed.hostname, "path": parsed.path}}


def request(url, key=None):
    headers = {"Accept": "application/json", "User-Agent": "HostLab-Connectivity/2"}
    if key is not None:
        if credential_shape(key)["control"]:
            return {"status": "unsafe_credential", "http": None}, None
        headers["Authorization"] = "Bearer " + key
    started = time.monotonic()
    try:
        with urllib.request.build_opener(NoRedirect()).open(urllib.request.Request(url, headers=headers), timeout=15) as response:
            raw = response.read(MAX_CATALOG_BYTES + 1)
            summary = {"status": "received", "http": response.status, "seconds": round(time.monotonic() - started, 3), "request_id": safe_request_id(response.headers)}
            if len(raw) > MAX_CATALOG_BYTES:
                return dict(summary, status="response_exceeds_bound"), None
            return summary, json.loads(raw)
    except urllib.error.HTTPError as exc:
        try:
            detail = error_summary(exc.code, exc.read(MAX_ERROR_BYTES), exc.headers)
        except (OSError, ValueError):
            detail = error_summary(exc.code, b"", exc.headers)
        finally:
            exc.close()
        return {"status": "http_error", "http": exc.code, "seconds": round(time.monotonic() - started, 3), **detail}, None
    except (TimeoutError, urllib.error.URLError, OSError):
        return {"status": "transport_unknown", "http": None, "seconds": round(time.monotonic() - started, 3)}, None
    except (ValueError, UnicodeError):
        return {"status": "invalid_response", "http": None, "seconds": round(time.monotonic() - started, 3)}, None


def _catalog(summary, body, model):
    ids = body.get("data", body.get("models", [])) if isinstance(body, dict) else []
    ids = [row.get("id", row.get("slug")) if isinstance(row, dict) else row for row in ids] if isinstance(ids, list) else []
    return {"accessible": summary.get("http") == 200 and isinstance(body, dict),
            "model_found": model in ids, "model_count": len(ids)}


def check(profile):
    shape = credential_shape(os.environ.get("AI_API_KEY_" + str(profile).upper(), ""))
    result = {"profile": str(profile).lower(), "credential_shape": shape, "generation_tested": False}
    try:
        config = configuration(profile)
    except ValueError as exc:
        return dict(result, status=str(exc))
    result.update(endpoint=config["endpoint"], configured_model=config["model"])
    raw, body = request(config["base"] + "/models", config["key"])
    anonymous, _ = request(config["base"] + "/models")
    catalog = _catalog(raw, body, config["model"])
    result.update(status="catalog_only", authenticated_request=raw, anonymous_request=anonymous,
                  catalog_accessible=catalog["accessible"], model_found=catalog["model_found"], catalog_model_count=catalog["model_count"],
                  key_validation="authenticated_catalog_access" if catalog["accessible"] and anonymous.get("http") in (401, 403) else "not_proven_by_catalog")
    if shape["padding"] and config["key"].strip() and not credential_shape(config["key"].strip())["control"]:
        summary, body = request(config["base"] + "/models", config["key"].strip())
        result["padding_variant"] = {"variant": "trimmed_catalog_only", "canonical_key_used_for_generation": False,
                                     "request": summary, **_catalog(summary, body, config["model"])}
    return result


def bounded_check(profile, timeout=50):
    try:
        worker = subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), "--worker", profile], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        try:
            raw, _ = worker.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            worker.kill()
            worker.communicate(timeout=5)
            return {"profile": profile, "status": "deadline_exceeded", "generation_tested": False}
        if worker.returncode or len(raw) > 16384:
            raise ValueError("worker_failed")
        return json.loads(raw)
    except (OSError, ValueError):
        return {"profile": profile, "status": "diagnostic_failed", "generation_tested": False}


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--worker" and sys.argv[2] in {"primary", "backup"}:
        print(json.dumps(check(sys.argv[2]), separators=(",", ":")))
        return 0
    if sys.argv[1:]:
        print(json.dumps({"schema": 2, "status": "invalid_invocation"}))
        return 2
    results = [bounded_check(profile) for profile in ("primary", "backup")]
    report = {"schema": 2, "mode": "catalog_only_no_generation_request", "profiles": results}
    output = Path(__file__).resolve().parents[2] / "runtime/hostlab/connectivity"
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all(r.get("catalog_accessible") and r.get("model_found") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
