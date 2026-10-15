"""Caller-side bounded batch scheduling. Unknown dispatch outcomes are never replayed."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import time
import uuid

import analysis_plan
import hostlab


def admission_lock(path):
    """OS releases this nonblocking lock even if the caller crashes."""
    stream = path.open("a+b")
    stream.seek(0, 2)
    if stream.tell() == 0:
        stream.write(b" ")
        stream.flush()
    stream.seek(0)
    try:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        stream.close()
        return None
    return stream


def reconcile(receipt, run):
    updated = {**receipt, "status": run["status"], "conclusion": run.get("conclusion")}
    if run.get("id") is not None:
        updated["run_id"] = run["id"]
    return updated


def describe(request):
    request = analysis_plan.validate(request)
    result = analysis_plan.plan(request)
    result.update({"environment": "remote_runner", "availability": "verified_on_runner_before_use",
                   "legacy_commands_default": "sqlite", "jadx_path": "unchanged",
                   "max_tasks": analysis_plan.MAX_TASKS, "max_request_bytes": analysis_plan.MAX_REQUEST_BYTES,
                   "completed_reuse": "requires_exact_apk_sha_and_sample_revision", "unknown_dispatch": "look_up_existing_request_do_not_replay"})
    return result


def submit(version_code, request, gh, lookup, runs, *, repository, workflow,
           apk_sha256="", sample_revision="", idempotency_key="", runner_revision=None,
           reuse_completed=True):
    request = analysis_plan.validate(request)
    analysis_plan.integer(version_code, 1, 9999999999, "version_code")
    if bool(apk_sha256) != bool(sample_revision):
        raise ValueError("provide both immutable APK SHA-256 and sample revision, or neither")
    if apk_sha256 and not re.fullmatch(r"[0-9a-f]{64}", apk_sha256):
        raise ValueError("invalid APK SHA-256")
    if sample_revision and not re.fullmatch(r"[0-9a-f]{40}", sample_revision):
        raise ValueError("invalid sample revision")
    if idempotency_key and not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", idempotency_key):
        raise ValueError("invalid idempotency key")
    head = runner_revision or json.loads(gh(["api", f"repos/{repository}/git/ref/heads/main"]))["object"]["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("invalid runner source revision")
    identity = {"version_code": version_code, "request": request, "apk_sha256": apk_sha256,
                "sample_revision": sample_revision, "runner_revision": head, "key": idempotency_key}
    inputs = {"version_code": str(version_code), "operation": "batch",
              "argument": json.dumps(request, separators=(",", ":"), ensure_ascii=False)}
    if apk_sha256:
        inputs.update(apk_sha256=apk_sha256, source_revision=sample_revision)
    return _submit(identity, inputs, describe(request), gh, lookup, runs, repository=repository,
                   workflow=workflow, idempotency_key=idempotency_key, head=head,
                   reuse_completed=reuse_completed and bool(apk_sha256)
                   and all(task["operation"] != "query" for task in request["tasks"]))


def submit_group(samples, request, gh, lookup, runs, *, repository, workflow,
                 idempotency_key="", runner_revision=None, reuse_completed=True, execution=None):
    import runner_group
    payload = runner_group.validate({"schema": 2 if execution is not None else 1, "samples": samples, "request": request,
                                    **({"execution": execution} if execution is not None else {})})
    head = runner_revision or json.loads(gh(["api", f"repos/{repository}/git/ref/heads/main"]))["object"]["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("invalid runner source revision")
    if idempotency_key and not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", idempotency_key):
        raise ValueError("invalid idempotency key")
    identity = {"operation": "batch_group", "samples": payload["samples"], "request": payload["request"],
                "runner_revision": head, "key": idempotency_key,
                **({"execution": execution} if execution is not None else {})}
    inputs = {"version_code": str(payload["samples"][0]["version_code"]), "operation": "batch_group",
              "argument": json.dumps(payload, separators=(",", ":"), ensure_ascii=False)}
    return _submit(identity, inputs, {**describe(payload["request"]), "runner_batch_size": len(samples)},
                   gh, lookup, runs, repository=repository, workflow=workflow,
                   idempotency_key=idempotency_key, head=head,
                   reuse_completed=reuse_completed and all(t["operation"] != "query" for t in payload["request"]["tasks"]))


def _submit(identity, inputs, plan, gh, lookup, runs, *, repository, workflow,
            idempotency_key, head, reuse_completed):
    """One durable admission protocol for single and grouped runner submissions."""
    payload_hash = hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    key = hashlib.sha256(("idempotency:" + idempotency_key).encode()).hexdigest() if idempotency_key else payload_hash
    directory = hostlab.STATE / "analysis-schedule"
    directory.mkdir(parents=True, exist_ok=True)
    record_path, lock_path = directory / (key + ".json"), directory / "admission.lock"
    lock = admission_lock(lock_path)
    if lock is None:
        return {"status": "scheduler_busy", "dispatched": False, "request_sha256": key}
    try:
        if record_path.exists():
            old = json.loads(record_path.read_text(encoding="utf-8"))
            if old["request_sha256"] != payload_hash:
                raise ValueError("idempotency key is already bound to a different immutable request")
            run = lookup(old["request_id"])
            if run is not None:
                old = reconcile(old, run)
                hostlab.write_json(record_path, old)
            if run is None or run.get("status") != "completed":
                return {**old, "reused": True, "dispatched": False,
                        "status": run.get("status") if run else old["status"]}
            if idempotency_key or reuse_completed and run.get("conclusion") == "success" and time.time() - old["created_at"] < 86400:
                return {**old, "reused": True, "dispatched": False, "status": "completed", "conclusion": run.get("conclusion")}
        recent = runs()
        observed = {r.get("display_title", "").removeprefix("hostlab-"):r for r in recent}
        active = {key for key,r in observed.items() if r.get("status") != "completed"}
        for path in directory.glob("*.json"):
            receipt = json.loads(path.read_text(encoding="utf-8"))
            if receipt["request_id"] in observed:
                updated = reconcile(receipt, observed[receipt["request_id"]])
                if updated != receipt:
                    hostlab.write_json(path, updated)
            elif receipt["status"] in {"dispatch_unknown", "submitted", "queued", "in_progress", "waiting", "pending", "requested"}:
                active.add(receipt["request_id"])
        if len(active) >= 4:
            return {"status": "capacity_full", "dispatched": False, "active_jobs": len(active), "limit": 4}
        request_id = uuid.uuid4().hex
        record = {"request_id": request_id, "request_sha256": payload_hash, "status": "dispatch_unknown",
                  "created_at": time.time(), "runner_revision": head, "plan": plan,
                  **{k: v for k, v in identity.items() if k not in {"request", "key", "runner_revision"}}}
        # Write before the network request: a client/network crash must not cause automatic paid replay.
        hostlab.write_json(record_path, record)
        hostlab.write_json(hostlab.STATE / "remote-requests" / (request_id + ".json"), record)
        inputs = {**inputs, "request_id": request_id, "runner_revision": head}
        try:
            response = gh(["api", "--method", "POST", f"repos/{repository}/actions/workflows/{workflow}/dispatches", "--input", "-"],
                          {"ref": "main", "inputs": inputs})
        except Exception:
            return {**record, "dispatched": None, "reused": False,
                    "next_action": "job_status(request_id); dispatch outcome unknown, do not submit again"}
        if response.strip():
            try:
                dispatched = json.loads(response)
                if dispatched.get("workflow_run_id"):
                    hostlab.write_json(hostlab.STATE / "remote-job-map" / (request_id + ".json"), {"run_id": dispatched["workflow_run_id"]})
            except (ValueError, TypeError):
                return {**record, "dispatched": None, "reused": False, "next_action": "job_status(request_id)"}
        record["status"] = "submitted"
        hostlab.write_json(record_path, record)
        return {**record, "dispatched": True, "reused": False, "repository": repository}
    finally:
        lock.close()


def observe(request_id, run):
    """Update only known receipts after an authenticated status read."""
    directory = hostlab.STATE / "analysis-schedule"
    if not directory.is_dir():
        return
    lock = admission_lock(directory / "admission.lock")
    if lock is None:
        return
    try:
        for path in directory.glob("*.json"):
            receipt = json.loads(path.read_text(encoding="utf-8"))
            if receipt["request_id"] == request_id:
                hostlab.write_json(path, reconcile(receipt, run))
    finally:
        lock.close()
