"""Bounded multi-sample wire contract; each member retains its own batch identity."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import re

import analysis_plan

MAX_SAMPLES = 4
MAX_ADAPTIVE_SAMPLES = 12
MAX_REQUEST_BYTES = 30000


def validate(value):
    if len(json.dumps(value, ensure_ascii=False).encode("utf-8")) > MAX_REQUEST_BYTES:
        raise ValueError("runner group exceeds bounded input")
    if not isinstance(value, dict) or type(value.get("schema")) is not int or value["schema"] not in {1, 2}:
        raise ValueError("invalid runner group schema")
    adaptive = value["schema"] == 2
    if set(value) != ({"schema", "request", "samples", "execution"} if adaptive else {"schema", "request", "samples"}):
        raise ValueError("invalid runner group fields")
    if adaptive and (not isinstance(value["execution"], dict) or set(value["execution"]) != {"mode", "prefetch_max"}
                     or value["execution"].get("mode") != "adaptive-v1"
                     or type(value["execution"].get("prefetch_max")) is not int or value["execution"]["prefetch_max"] != 2):
        raise ValueError("invalid runner group execution policy")
    rows = value["samples"]
    limit = MAX_ADAPTIVE_SAMPLES if adaptive else MAX_SAMPLES
    if not isinstance(rows, list) or not 1 <= len(rows) <= limit:
        raise ValueError("runner group needs 1.." + str(limit) + " pinned samples")
    samples = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"version_code", "apk_sha256", "sample_revision"}:
            raise ValueError("invalid runner group sample")
        analysis_plan.integer(row["version_code"], 1, 9999999999, "version_code")
        for name, length in (("apk_sha256", 64), ("sample_revision", 40)):
            if not isinstance(row[name], str) or not re.fullmatch("[0-9a-f]{" + str(length) + "}", row[name]):
                raise ValueError("invalid runner group " + name)
        if row in samples:
            raise ValueError("duplicate runner group sample")
        samples.append(dict(row))
    request = analysis_plan.validate(value["request"])
    if "resume" in request:
        raise ValueError("checkpoint resume uses a single pinned sample batch")
    return {"schema": value["schema"], "request": request, "samples": samples,
            **({"execution": dict(value["execution"])} if adaptive else {})}


def execution_fingerprint(payload):
    if payload["schema"] == 1:
        return None
    return hashlib.sha256(json.dumps(payload["execution"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def collect(payload, downloaded, runner_revision):
    """Read only verified artifact files. Failure is retryable without another runner."""
    payload = validate(payload)
    files = [Path(p) for p in downloaded["files"]]
    indices = [p for p in files if p.name == "group.json"]
    if len(indices) != 1 or indices[0].stat().st_size > 65536:
        raise ValueError("missing or ambiguous runner group receipt")
    root = indices[0].parent
    receipt = json.loads(indices[0].read_text(encoding="utf-8"))
    fingerprint = analysis_plan.fingerprint(payload["request"])
    rows = receipt.get("samples")
    if (receipt.get("schema") != 1 or receipt.get("runner_revision") != runner_revision
            or receipt.get("request_sha256") != fingerprint or not isinstance(rows, list)
            or len(rows) != len(payload["samples"])):
        raise ValueError("runner group receipt identity mismatch")
    execution_sha = execution_fingerprint(payload)
    if execution_sha and receipt.get("execution") != payload["execution"]:
        raise ValueError("runner group execution policy mismatch")
    members = []
    for index, (row, sample) in enumerate(zip(rows, payload["samples"])):
        if (not isinstance(row, dict) or type(row.get("index")) is not int or row["index"] != index or row.get("sample") != sample
                or row.get("status") not in {"complete", "failed", "not_started"}):
            raise ValueError("runner group member identity mismatch")
        names = {root / "samples" / str(index) / name for name in ("job.json", "result.txt")}
        present = names.intersection(files)
        status = row["status"]
        if status == "not_started":
            # A process interruption between writing a member and its checkpoint is recoverable.
            # Both member files must validate before promoting the checkpoint to complete.
            status = "skipped"
        if present:
            if present != names or any(p.stat().st_size > 2 * 1024 * 1024 for p in present):
                raise ValueError("incomplete or oversized runner group member")
            metadata = json.loads((root / "samples" / str(index) / "job.json").read_text(encoding="utf-8"))
            result = json.loads((root / "samples" / str(index) / "result.txt").read_text(encoding="utf-8"))
            if (metadata.get("operation") != "batch" or metadata.get("version_code") != sample["version_code"]
                    or metadata.get("apk_sha256") != sample["apk_sha256"]
                    or metadata.get("sample_revision") != sample["sample_revision"]
                    or metadata.get("runner_revision") != runner_revision
                    or metadata.get("request_sha256") != fingerprint
                    or type(metadata.get("group_index")) is not int or metadata["group_index"] != index):
                raise ValueError("runner group member metadata mismatch")
            if execution_sha and metadata.get("execution_sha256") != execution_sha:
                raise ValueError("runner group member execution policy mismatch")
            complete = result.get("complete") is True and metadata.get("complete") is True and metadata.get("exit_code") == 0
            if complete:
                observed = result.get("sample", {})
                if (result.get("source_unchanged") is not True or observed.get("sha256") != sample["apk_sha256"]
                        or observed.get("version_code") != sample["version_code"]
                        or observed.get("revision") != sample["sample_revision"]):
                    raise ValueError("runner group source proof mismatch")
            if status == "complete" and not complete:
                raise ValueError("runner group checkpoint contradicts member result")
            if row["status"] == "not_started":
                status = "complete" if complete else "failed"
        elif status == "complete":
            raise ValueError("runner group complete member files are missing")
        members.append({"index": index, "sample": sample, "status": status,
                        "files": sorted(str(p) for p in present),
                        **({"reason": "disk_capacity" if row.get("reason") == "disk_capacity" else
                            "group_admission_deadline" if receipt.get("deadline_exhausted") is True else
                            "runner_interrupted_before_member"} if status == "skipped" else {})})
    return {"members": members, "complete": all(m["status"] == "complete" for m in members)}
