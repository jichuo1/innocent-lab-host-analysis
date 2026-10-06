"""Catalog-only connectivity test. Never print secret values or response bodies."""
import difflib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url, key=None):
    headers = {"Accept": "application/json", "User-Agent": "HostLab-Connectivity/1"}
    if key:
        headers["Authorization"] = "Bearer " + key
    start = time.monotonic()
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(urllib.request.Request(url, headers=headers), timeout=30) as response:
            data = response.read(4 * 1024 * 1024 + 1)
            if len(data) > 4 * 1024 * 1024:
                return {"http": response.status, "error": "response_exceeds_bound"}, None
            parsed = json.loads(data)
            return {"http": response.status, "seconds": round(time.monotonic()-start, 3)}, parsed
    except urllib.error.HTTPError as exc:
        return {"http": exc.code, "seconds": round(time.monotonic()-start, 3)}, None
    except Exception as exc:
        return {"error": type(exc).__name__, "seconds": round(time.monotonic()-start, 3)}, None


def check(profile):
    key = os.environ.get("AI_API_KEY_" + profile, "")
    configured = os.environ.get("AI_" + profile + "_BASE_URL", "").rstrip("/")
    model = os.environ.get("AI_" + profile + "_MODEL", "")
    if not key or not configured or not model:
        return {"profile": profile.lower(), "status": "configuration_incomplete"}
    base = configured
    for suffix in ("/chat/completions", "/responses", "/messages"):
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    parsed = urllib.parse.urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        return {"profile": profile.lower(), "status": "invalid_base_url"}
    url = base + "/models"
    authenticated, body = request(url, key)
    anonymous, _ = request(url)
    ids = []
    if isinstance(body, dict):
        rows = body.get("data", body.get("models", []))
        if isinstance(rows, list):
            for row in rows:
                value = row.get("id", row.get("slug", "")) if isinstance(row, dict) else row
                if isinstance(value, str) and len(value) < 150 and re.fullmatch(r"[A-Za-z0-9._:/-]+", value) and key not in value:
                    ids.append(value)
    accessible = authenticated.get("http") == 200 and isinstance(body, dict)
    return {"profile": profile.lower(), "configured_base": configured, "normalized_base": base,
            "configured_model": model, "authenticated_request": authenticated, "anonymous_request": anonymous,
            "catalog_accessible": accessible, "model_found": model in ids, "catalog_model_count": len(ids),
            "similar_model_ids": difflib.get_close_matches(model, ids, n=4, cutoff=0.35),
            "key_validation": "authenticated_catalog_access" if accessible and anonymous.get("http") in (401,403) else "not_proven_by_catalog",
            "generation_tested": False}


if __name__ == "__main__":
    results = [check("PRIMARY"), check("BACKUP")]
    output = Path(__file__).resolve().parents[2] / "runtime/hostlab/connectivity"
    output.mkdir(parents=True, exist_ok=True)
    report = {"mode": "catalog_only_no_generation_request", "profiles": results}
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if all(r.get("catalog_accessible") and r.get("model_found") for r in results) else 1)
