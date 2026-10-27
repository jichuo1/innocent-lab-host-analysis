"""One durable caller-side POST; transport ambiguity is never retried here."""
from __future__ import annotations

import json
import re
import time

import hostlab

API_VERSION = "2026-03-10"
# Bounded markers of an API answer that decided the request never ran. Anything else
# stays an unknown transport outcome and is never replayed automatically.
REJECTION_MARKERS = ("unexpected inputs provided", "not found (http 404)", "invalid input",
                     "workflow does not have", "(http 400)", "(http 422)")


def rejection_marker(detail):
    head = detail.lower()[:500] if isinstance(detail, str) else ""
    return next((marker for marker in REJECTION_MARKERS if marker in head), None)


def dispatch(repository, workflow, inputs, gh):
    """Caller must persist request_id before invoking this mutative operation."""
    request_id = inputs.get("request_id")
    if not isinstance(request_id, str) or not re.fullmatch(r"[0-9a-f]{32}", request_id):
        raise ValueError("dispatch requires a previously persisted request ID")
    started = time.monotonic()
    metrics = {"api_version": API_VERSION, "started_at": time.time(), "response_kind": "transport_unknown"}
    result = {"request_id": request_id, "status": "dispatch_unknown", "dispatched": None,
              "dispatch": metrics,
              "next_action": "job_status(request_id); dispatch outcome unknown, do not submit again"}
    try:
        response = gh(["api", "--method", "POST", "--header", "X-GitHub-Api-Version: " + API_VERSION,
            f"repos/{repository}/actions/workflows/{workflow}/dispatches", "--input", "-"],
            {"ref": "main", "inputs": inputs})
    except Exception as exc:
        metrics["error_type"] = type(exc).__name__
        marker = rejection_marker(str(exc))
        if marker is not None:
            # The API decided this request never ran, so a corrected one may be sent.
            metrics["response_kind"] = "rejected"
            metrics["rejected_by"] = marker
            result.update(status="rejected", dispatched=False, reason="dispatch_rejected",
                          next_action="the workflow refused this request; correct it or update the "
                                      "runner, then submit again")
    else:
        if isinstance(response, str) and not response.strip():
            result.update(status="submitted", dispatched=True)
            result.pop("next_action", None)
            metrics["response_kind"] = "legacy_empty"
        else:
            try:
                value = json.loads(response)
                run_id = value.get("workflow_run_id") if isinstance(value, dict) else None
                if type(run_id) is not int or run_id <= 0:
                    raise ValueError("invalid workflow run ID")
                result.update(status="submitted", dispatched=True, run_id=run_id)
                result.pop("next_action", None)
                metrics["response_kind"] = "workflow_run_id"
                try:
                    hostlab.write_json(hostlab.STATE / "remote-job-map" / (request_id + ".json"), {"run_id": run_id})
                    metrics["mapping_persisted"] = True
                except OSError:
                    # The returned ID also persists in the caller receipt; no second POST.
                    metrics["mapping_persisted"] = False
            except (ValueError, TypeError):
                metrics["response_kind"] = "invalid_response_unknown"
    metrics.update(finished_at=time.time(), elapsed_ms=(time.monotonic()-started)*1000)
    return result
