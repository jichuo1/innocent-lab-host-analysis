"""Deterministic bounded placement; validated profiles are performance hints only."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import time
import uuid

import analysis_plan
import hostlab
import remote_schedule

PLANNER_VERSION = "constraint-lpt-v1"
MAX_PROFILE_ROWS = 256
MAX_PROFILE_BYTES = 1024 * 1024
MAX_NATIVE_GROUP = 12
MAX_OTHER_GROUP = 4
MAX_KNOWN_GROUP_BYTES = 4 * 1024 * 1024 * 1024
EXECUTION = {"mode": "adaptive-v1", "prefetch_max": 2}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def directory():
    return hostlab.STATE.absolute() / "scheduling-profiles"


def regular_path(path, *, missing=False):
    """Only a direct regular child of the dedicated cache directory can be read."""
    root = directory()
    path = Path(path).absolute()
    if path.parent != root or not re.fullmatch(r"(?:[0-9a-f]{40}-[0-9a-f]{64}|frozen-[A-Za-z0-9_-]{1,100})\.json", path.name):
        raise ValueError("profile path must be a direct scheduling-profiles file")
    for ancestor in reversed((root, *root.parents)):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            continue
        if (not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode)
                or getattr(info, "st_file_attributes", 0) & 0x400):
            raise ValueError("linked scheduling profile directory")
    try:
        info = path.lstat()
    except FileNotFoundError:
        if missing:
            return path
        raise ValueError("scheduling profile is missing") from None
    if (not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)
            or getattr(info, "st_file_attributes", 0) & 0x400 or info.st_nlink != 1):
        raise ValueError("scheduling profile must be a regular unlinked file")
    if info.st_size > MAX_PROFILE_BYTES:
        raise ValueError("scheduling profile exceeds its byte budget")
    return path


def number(value, limit):
    return type(value) in {int, float} and math.isfinite(value) and 0 <= value <= limit


def read_profile(path):
    with path.open("rb") as stream:
        raw = stream.read(MAX_PROFILE_BYTES + 1)
    if len(raw) > MAX_PROFILE_BYTES:
        raise ValueError("scheduling profile exceeds its byte budget")
    return raw


def profile_rows(value, revision, request_hash):
    if (not isinstance(value, dict) or type(value.get("schema")) is not int or value["schema"] != 1
            or value.get("runner_revision") != revision or value.get("request_sha256") != request_hash
            or not isinstance(value.get("rows"), list) or len(value["rows"]) > MAX_PROFILE_ROWS):
        raise ValueError("scheduling profile identity mismatch")
    rows = {}
    for row in value["rows"]:
        if (not isinstance(row, dict) or not isinstance(row.get("apk_sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", row["apk_sha256"])
                or type(row.get("size_bytes")) is not int or not 1 <= row["size_bytes"] <= 1024**3
                or not number(row.get("fetch_ms"), 3600000)
                or not number(row.get("analysis_ms"), 600000)
                or not number(row.get("observed_at"), 10**12)):
            raise ValueError("invalid scheduling profile row")
        if row["apk_sha256"] in rows:
            raise ValueError("duplicate scheduling profile row")
        rows[row["apk_sha256"]] = dict(row)
    return rows


def snapshot(samples, request, revision):
    request_hash = analysis_plan.fingerprint(request)
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("invalid scheduling profile revision")
    frozen = os.environ.get("HOSTLAB_SCHEDULING_PROFILE", "")
    filename = revision + "-" + request_hash + ".json"
    source = {"kind": "missing", "name": filename, "sha256": None}
    rows = {}
    try:
        selected = Path(frozen) if frozen else directory() / filename
        if frozen and (not selected.is_absolute() or not selected.name.startswith("frozen-")):
            raise ValueError("frozen profile must be an absolute frozen-* scheduling profile")
        selected = regular_path(selected, missing=not frozen)
        if selected.exists():
            raw = read_profile(selected)
            rows = profile_rows(json.loads(raw), revision, request_hash)
            source = {"kind": "frozen" if frozen else "live", "name": selected.name,
                      "sha256": hashlib.sha256(raw).hexdigest()}
    except (OSError, ValueError, TypeError):
        if frozen:
            raise ValueError("configured frozen scheduling profile is invalid") from None
        source["kind"] = "unavailable"
    return {"schema": 1, "runner_revision": revision, "request_sha256": request_hash,
            "profile_source": source,
            "rows": [{"index": i, "apk_sha256": sample["apk_sha256"],
                      "size_bytes": rows.get(sample["apk_sha256"], {}).get("size_bytes"),
                      "fetch_ms": rows.get(sample["apk_sha256"], {}).get("fetch_ms"),
                      "analysis_ms": rows.get(sample["apk_sha256"], {}).get("analysis_ms")}
                     for i, sample in enumerate(samples)]}


def prediction(rows):
    if not rows:
        return 0.0
    fetch = [r["fetch_ms"] / 1000 for r in rows if r["fetch_ms"] is not None]
    analysis = [r["analysis_ms"] / 1000 for r in rows if r["analysis_ms"] is not None]
    return max(sum(analysis), sum(fetch) / 2) + max(fetch, default=0) / 2


def layout(samples, request, max_parallel, deadline_seconds, cost_snapshot):
    """Constrained LPT, with count-first placement for unprofiled samples."""
    normalized = analysis_plan.validate(request)
    strict_native = normalized["backend"] == "dexsql" and all(
        g["backend"] == "dexsql" for g in analysis_plan.plan(normalized)["groups"])
    cap = MAX_NATIVE_GROUP if strict_native else MAX_OTHER_GROUP
    costs = cost_snapshot["rows"]
    estimate_limit = min(3300, deadline_seconds)
    bins = [[] for _ in range(min(max_parallel, len(samples)))]

    def fitting(indices, index):
        indices = indices + [index]
        if len(indices) > cap:
            return False
        known = [costs[i] for i in indices]
        if sum(row["size_bytes"] or 0 for row in known) > MAX_KNOWN_GROUP_BYTES:
            return False
        payload = {"schema": 2, "request": normalized,
                   "samples": [samples[i] for i in indices], "execution": EXECUTION}
        import runner_group
        if len(json.dumps(payload, ensure_ascii=False).encode()) > runner_group.MAX_REQUEST_BYTES:
            return False
        # A profile is advisory. An over-estimate must not discard a singleton.
        return len(indices) == 1 or prediction(known) <= estimate_limit

    order = sorted(range(len(samples)), key=lambda i: (
        costs[i]["fetch_ms"] is None,
        -max(costs[i]["analysis_ms"] or 0, (costs[i]["fetch_ms"] or 0) / 2), i))
    for index in order:
        available = [j for j, indices in enumerate(bins) if fitting(indices, index)]
        if not available:
            if not fitting([], index):
                raise ValueError("sample cannot fit bounded adaptive runner payload")
            bins.append([])
            available = [len(bins)-1]
        if costs[index]["fetch_ms"] is None:
            chosen = min(available, key=lambda j: (len(bins[j]), prediction([costs[i] for i in bins[j]]), j))
        else:
            chosen = min(available, key=lambda j: (prediction([costs[i] for i in bins[j] + [index]]), len(bins[j]), j))
        bins[chosen].append(index)
    groups = [{"sample_indices": indices, "predicted_processing_seconds": prediction([costs[i] for i in indices]),
               "known_input_bytes": sum(costs[i]["size_bytes"] or 0 for i in indices),
               "unprofiled_samples": sum(costs[i]["fetch_ms"] is None for i in indices),
               "prediction_exceeds_deadline": prediction([costs[i] for i in indices]) > estimate_limit}
              for indices in bins if indices]
    return {"planner_version": PLANNER_VERSION, "execution": dict(EXECUTION),
            "max_group_samples": cap, "max_known_group_bytes": MAX_KNOWN_GROUP_BYTES,
            "prediction_limit_seconds": estimate_limit, "initial_runners": min(max_parallel, len(samples)),
            "cost_snapshot": cost_snapshot, "cost_snapshot_sha256": digest(cost_snapshot),
            "groups": groups, "physical_job_count": len(groups),
            "estimated_waves": (len(groups) + max_parallel - 1) // max_parallel,
            "profiled_samples": sum(r["fetch_ms"] is not None for r in costs),
            "scope": "performance_hints_only_not_identity_or_execution_acceptance"}


def build(samples, request, revision, max_parallel, deadline_seconds):
    return layout(samples, request, max_parallel, deadline_seconds, snapshot(samples, request, revision))


def projection(samples, request, max_parallel, deadline_seconds):
    """Planning has no network/cache reads; exact profiles bind only at create."""
    empty = {"schema": 1, "runner_revision": None,
             "request_sha256": analysis_plan.fingerprint(request),
             "profile_source": {"kind": "cold_projection", "name": None, "sha256": None},
             "rows": [{"index": i, "apk_sha256": sample["apk_sha256"], "size_bytes": None,
                       "fetch_ms": None, "analysis_ms": None} for i, sample in enumerate(samples)]}
    return layout(samples, request, max_parallel, deadline_seconds, empty)


def validate_plan(plan, samples, request, revision, max_parallel, deadline_seconds):
    if not isinstance(plan, dict):
        raise ValueError("invalid adaptive plan")
    saved = plan.get("cost_snapshot", {})
    if (not isinstance(saved, dict) or type(saved.get("schema")) is not int or saved["schema"] != 1 or saved.get("runner_revision") != revision
            or saved.get("request_sha256") != analysis_plan.fingerprint(request)
            or not isinstance(saved.get("rows"), list) or len(saved["rows"]) != len(samples)):
        raise ValueError("adaptive cost snapshot identity changed")
    for index, (row, sample) in enumerate(zip(saved["rows"], samples)):
        if (not isinstance(row, dict) or type(row.get("index")) is not int or row["index"] != index
                or row.get("apk_sha256") != sample["apk_sha256"]):
            raise ValueError("adaptive sample cost binding changed")
        known = row.get("fetch_ms") is not None
        if known:
            profile_rows({"schema": 1, "runner_revision": revision, "request_sha256": saved["request_sha256"],
                "rows": [{"apk_sha256": row["apk_sha256"], "size_bytes": row.get("size_bytes"),
                          "fetch_ms": row["fetch_ms"], "analysis_ms": row.get("analysis_ms"), "observed_at": 0}]},
                         revision, saved["request_sha256"])
        elif row.get("size_bytes") is not None or row.get("analysis_ms") is not None:
            raise ValueError("partial adaptive cost row")
    if plan != layout(samples, request, max_parallel, deadline_seconds, saved):
        raise ValueError("adaptive topology or cost plan changed")


def observe(payload, downloaded, runner_revision):
    """Cache only independently verified completed evidence; failures never affect results."""
    try:
        import runner_group
        collected = runner_group.collect(payload, downloaded, runner_revision)
        request_hash = analysis_plan.fingerprint(payload["request"])
        observations = []
        for member in collected["members"]:
            if member["status"] != "complete":
                continue
            files = {Path(p).name: Path(p) for p in member["files"]}
            result = json.loads(files["result.txt"].read_text(encoding="utf-8"))
            metadata = json.loads(files["job.json"].read_text(encoding="utf-8"))
            if result.get("source_unchanged") is not True:
                continue
            row = {"apk_sha256": member["sample"]["apk_sha256"], "size_bytes": result["sample"].get("size"),
                   "fetch_ms": metadata.get("fetch_ms"), "analysis_ms": metadata.get("phases", {}).get("analysis_ms"),
                   "observed_at": time.time()}
            try:
                profile_rows({"schema": 1, "runner_revision": runner_revision,
                              "request_sha256": request_hash, "rows": [row]}, runner_revision, request_hash)
                observations.append(row)
            except (ValueError, TypeError):
                continue
        if not observations:
            return {"stored": 0}
        root = directory()
        target = regular_path(root / (runner_revision + "-" + request_hash + ".json"), missing=True)
        root.mkdir(parents=True, exist_ok=True)
        lock_path = root / "profile.lock"
        try:
            info = lock_path.lstat()
            if not stat.S_ISREG(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400 or info.st_nlink != 1:
                return {"stored": 0}
        except FileNotFoundError:
            pass
        lock = None
        deadline = time.monotonic() + 1
        while lock is None:
            lock = remote_schedule.admission_lock(lock_path)
            if lock is None:
                if time.monotonic() >= deadline:
                    return {"stored": 0}
                time.sleep(0.01)
        try:
            regular_path(target, missing=True)
            rows = {}
            if target.exists():
                try:
                    rows = profile_rows(json.loads(read_profile(target)), runner_revision, request_hash)
                except (OSError, ValueError, TypeError):
                    pass
            rows.update({row["apk_sha256"]: row for row in observations})
            bounded = sorted(rows.values(), key=lambda r: (-r["observed_at"], r["apk_sha256"]))[:MAX_PROFILE_ROWS]
            value = {"schema": 1, "runner_revision": runner_revision, "request_sha256": request_hash, "rows": bounded}
            if len(json.dumps(value).encode()) > MAX_PROFILE_BYTES:
                return {"stored": 0}
            stage = root / (".profile-" + uuid.uuid4().hex + ".tmp")
            try:
                with stage.open("x", encoding="utf-8") as stream:
                    json.dump(value, stream, ensure_ascii=False, indent=2)
                    stream.write("\n")
                if stage.stat().st_size > MAX_PROFILE_BYTES:
                    return {"stored": 0}
                os.replace(stage, target)
            finally:
                stage.unlink(missing_ok=True)
            return {"stored": len(observations)}
        finally:
            lock.close()
    except Exception:
        return {"stored": 0}
