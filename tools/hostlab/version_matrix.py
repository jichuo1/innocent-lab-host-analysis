"""Durable, caller-driven bounded multi-version analysis. No background paid work."""
from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import threading
import time
import uuid

import analysis_plan
import hostlab
import remote_schedule

MAX_SAMPLES = 40
TERMINAL = {"complete", "failed", "skipped"}
COLLECTION_SLOTS = threading.BoundedSemaphore(4)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def definition(samples, request, max_parallel=4, reuse_completed=True, deadline_seconds=1800, runner_batch_size=1,
               execution_policy="fixed"):
    if not isinstance(samples, list) or not 1 <= len(samples) <= MAX_SAMPLES:
        raise ValueError("matrix needs 1..40 pinned samples")
    if type(reuse_completed) is not bool:
        raise ValueError("reuse_completed must be boolean")
    normalized = []
    seen = set()
    for row in samples:
        if not isinstance(row, dict) or set(row) != {"version_code", "apk_sha256", "sample_revision"}:
            raise ValueError("sample requires only version_code/apk_sha256/sample_revision from inventory")
        analysis_plan.integer(row["version_code"], 1, 9999999999, "version_code")
        if not isinstance(row["apk_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", row["apk_sha256"]):
            raise ValueError("invalid matrix APK SHA-256")
        if not isinstance(row["sample_revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", row["sample_revision"]):
            raise ValueError("invalid matrix sample revision")
        identity = digest(row)
        if identity not in seen:
            seen.add(identity)
            normalized.append(dict(row))
    runner_batch_size = analysis_plan.integer(runner_batch_size, 1, 4, "runner_batch_size")
    if not isinstance(execution_policy, str) or execution_policy not in {"fixed", "adaptive"}:
        raise ValueError("execution_policy must be fixed or adaptive")
    if execution_policy == "adaptive" and runner_batch_size != 1:
        raise ValueError("adaptive execution cannot also set a fixed runner_batch_size")
    spec = {"samples": normalized, "request": analysis_plan.validate(request),
            "max_parallel": analysis_plan.integer(max_parallel, 1, 4, "max_parallel"),
            "reuse_completed": reuse_completed,
            "deadline_seconds": analysis_plan.integer(deadline_seconds, 1, 7200, "deadline_seconds")}
    # Keep the exact schema/hash of existing one-sample matrices.
    if execution_policy == "adaptive":
        spec["execution_policy"] = "adaptive"
    elif runner_batch_size > 1:
        spec["runner_batch_size"] = runner_batch_size
        import runner_group
        for start in range(0, len(normalized), runner_batch_size):
            runner_group.validate({"schema": 1, "request": spec["request"],
                                   "samples": normalized[start:start + runner_batch_size]})
    return spec


def plan(samples, request, max_parallel=4, reuse_completed=True, deadline_seconds=1800, runner_batch_size=1,
         execution_policy="fixed"):
    spec = definition(samples, request, max_parallel, reuse_completed, deadline_seconds, runner_batch_size, execution_policy)
    adaptive = None
    if execution_policy == "adaptive":
        import adaptive_schedule
        adaptive = adaptive_schedule.projection(spec["samples"], spec["request"], max_parallel, deadline_seconds)
    return {"schema": 1, "definition_sha256": digest(spec), "samples": spec["samples"],
            "sample_count": len(spec["samples"]), "duplicate_samples_removed": len(samples)-len(spec["samples"]),
            "max_parallel": spec["max_parallel"], "reuse_completed": spec["reuse_completed"],
            "runner_batch_size": runner_batch_size,
            "execution_policy": execution_policy,
            "physical_job_count": adaptive["physical_job_count"] if adaptive else (len(spec["samples"]) + runner_batch_size - 1) // runner_batch_size,
            "deadline_seconds": spec["deadline_seconds"], "batch_plan": analysis_plan.plan(spec["request"]),
            "tool_revision": "one_immutable_commit_for_the_entire_matrix",
            "advance_dispatch_budget": 4 if adaptive else 2, "execution": "caller_driven_no_background_dispatch",
            **({"adaptive_plan": adaptive,
                "profile_binding": "cold projection only; exact tooling/profile snapshot binds at create"} if adaptive else {}),
            "scope": "offline_static_only"}


def directory():
    return hostlab.STATE / "version-matrices"


def path(matrix_id):
    if not isinstance(matrix_id, str) or not re.fullmatch(r"[0-9a-f]{32}", matrix_id):
        raise ValueError("invalid matrix ID")
    return directory() / (matrix_id + ".json")


def dispatch_key(value, index):
    spec=value["definition"]
    semantic=all(t["operation"]!="query" for t in spec["request"]["tasks"])
    identity={"sample":spec["samples"][index],"request":spec["request"],
              "revision":value["runner_revision"],"epoch":int(value["created_at"]//86400)}
    return ("vmcache_"+digest(identity)[:48] if spec["reuse_completed"] and semantic
            else "vm_"+value["matrix_id"]+"_"+str(index))


def binding_hash(value):
    return digest({k:value[k] for k in ("matrix_id","definition_sha256","runner_revision","created_at")})


def group_dispatch_key(value, index, indices):
    spec = value["definition"]
    identity = {"samples": [spec["samples"][i] for i in indices], "request": spec["request"],
                "revision": value["runner_revision"], "epoch": int(value["created_at"] // 86400)}
    if spec.get("execution_policy") == "adaptive":
        identity["execution"] = spec["adaptive_plan"]["execution"]
    semantic = all(t["operation"] != "query" for t in spec["request"]["tasks"])
    return ("vmgroup_" + digest(identity)[:48] if spec["reuse_completed"] and semantic
            else "vg_" + value["matrix_id"] + "_" + str(index))


def group_payload(matrix, group):
    import runner_group
    spec = matrix["definition"]
    payload = {"schema": 1, "request": spec["request"],
               "samples": [spec["samples"][i] for i in group["sample_indices"]]}
    if spec.get("execution_policy") == "adaptive":
        payload.update(schema=2, execution=spec["adaptive_plan"]["execution"])
    return runner_group.validate(payload)


def load(matrix_id):
    value = json.loads(path(matrix_id).read_text(encoding="utf-8"))
    if value["definition_sha256"] != digest(value["definition"]):
        raise ValueError("matrix immutable definition changed")
    if not re.fullmatch(r"[0-9a-f]{40}", value["runner_revision"]):
        raise ValueError("matrix runner revision is invalid")
    if value["matrix_id"]!=matrix_id or value.get("binding_sha256")!=binding_hash(value):
        raise ValueError("matrix immutable tool binding changed")
    if len(value["entries"])!=len(value["definition"]["samples"]):
        raise ValueError("matrix sample queue changed")
    for i,entry in enumerate(value["entries"]):
        if entry["sample"]!=value["definition"]["samples"][i] or entry["dispatch_key"]!=dispatch_key(value,i):
            raise ValueError("matrix sample or retry binding changed")
    spec = value["definition"]
    size = spec.get("runner_batch_size", 1)
    if spec.get("execution_policy") == "adaptive":
        import adaptive_schedule
        if size != 1 or value.get("schema") != 3:
            raise ValueError("adaptive matrix schema changed")
        adaptive_schedule.validate_plan(spec.get("adaptive_plan", {}), spec["samples"], spec["request"],
            value["runner_revision"], spec["max_parallel"], spec["deadline_seconds"])
        expected = [g["sample_indices"] for g in spec["adaptive_plan"]["groups"]]
    elif size > 1:
        analysis_plan.integer(size, 2, 4, "runner_batch_size")
        expected = [list(range(start, min(start + size, len(value["entries"]))))
                    for start in range(0, len(value["entries"]), size)]
        if value.get("schema") != 2:
            raise ValueError("matrix physical group schema changed")
    else:
        expected = None
    if expected is not None:
        groups = value.get("groups", [])
        if len(groups) != len(expected):
            raise ValueError("matrix physical group queue changed")
        for index, (group, indices) in enumerate(zip(groups, expected)):
            if (group.get("group_id") != "g" + str(index) or group.get("sample_indices") != indices
                    or group.get("dispatch_key") != group_dispatch_key(value, index, indices)):
                raise ValueError("matrix physical group binding changed")
            for member, sample_index in enumerate(indices):
                entry = value["entries"][sample_index]
                if entry.get("group_id") != group["group_id"] or entry.get("group_index") != member:
                    raise ValueError("matrix member group binding changed")
                if entry.get("matrix_id") != matrix_id:
                    raise ValueError("matrix member source binding changed")
                if entry.get("request_id") != group.get("request_id"):
                    raise ValueError("matrix physical request binding changed")
    elif "groups" in value:
        raise ValueError("single-sample matrix has unexpected physical groups")
    return value


def summary(matrix):
    counts = Counter(e["status"] for e in matrix["entries"])
    finished = all(e["status"] in TERMINAL for e in matrix["entries"])
    units = matrix.get("groups", matrix["entries"])
    physical_inflight = len({e["request_id"] for e in units if e.get("request_id")
        and e["status"] not in TERMINAL | {"awaiting_results"}})
    awaiting = any(e["status"] == "awaiting_results" for e in matrix["entries"])
    return {"matrix_id": matrix["matrix_id"], "runner_revision": matrix["runner_revision"],
            "definition_sha256": matrix["definition_sha256"], "sample_count": len(matrix["entries"]),
            "counts": dict(counts), "finished": finished, "complete": counts["complete"] == len(matrix["entries"]),
            "peak_inflight": matrix["peak_inflight"], "max_parallel": matrix["definition"]["max_parallel"],
            "physical_inflight": physical_inflight,
            "runner_batch_size": matrix["definition"].get("runner_batch_size", 1),
            "execution_policy": matrix["definition"].get("execution_policy", "fixed"),
            **({"planned_group_sizes": [len(g["sample_indices"]) for g in matrix["groups"]],
                "adaptive_profile": matrix["definition"]["adaptive_plan"]["cost_snapshot"]["profile_source"]}
               if matrix["definition"].get("execution_policy") == "adaptive" else {}),
            "physical_job_count": len(units),
            "created_at": matrix["created_at"], "deadline_at": matrix["deadline_at"],
            "entries": [{k:v for k,v in e.items() if k != "dispatch_key"} for e in matrix["entries"]],
            "next_action": "version_matrix_result" if finished else "advance_version_matrix",
            **({"next_action_detail": "Retry advance_version_matrix to collect the same accepted jobs. "
                "If results cannot be recovered, recover_version_matrix(include_unverified_results=true) "
                "explicitly authorizes another execution only for completed jobs with unverified results; "
                "earlier successful work may run again."} if awaiting else {}),
            "poll_errors": matrix.get("poll_errors", []), "scope": "offline_static_only"}


def create(samples, request, gh, *, repository, max_parallel=4, reuse_completed=True,
           deadline_seconds=1800, idempotency_key="", runner_batch_size=1, _runner_revision=None,
           execution_policy="fixed"):
    spec = definition(samples, request, max_parallel, reuse_completed, deadline_seconds, runner_batch_size, execution_policy)
    if idempotency_key and not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", idempotency_key):
        raise ValueError("invalid matrix idempotency key")
    root = directory()
    root.mkdir(parents=True, exist_ok=True)
    lock = remote_schedule.admission_lock(root / "create.lock")
    if lock is None:
        return {"status": "scheduler_busy", "created": False}
    try:
        binding = root / ("key-" + digest(idempotency_key) + ".binding") if idempotency_key else None
        if binding and binding.exists():
            old = load(binding.read_text(encoding="ascii"))
            prior_input = {key: val for key, val in old["definition"].items() if key != "adaptive_plan"}
            if digest(prior_input) != digest(spec):
                raise ValueError("matrix key is already bound to a different request")
            if _runner_revision is not None and old["runner_revision"] != _runner_revision:
                raise ValueError("matrix recovery tool binding changed")
            return {**summary(old), "created": False, "reused": True}
        revision = _runner_revision or json.loads(gh(["api", f"repos/{repository}/git/ref/heads/main"]))["object"]["sha"]
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("invalid matrix tool revision")
        if execution_policy == "adaptive":
            import adaptive_schedule
            spec["adaptive_plan"] = adaptive_schedule.build(spec["samples"], spec["request"], revision,
                max_parallel, deadline_seconds)
        created = time.time()
        matrix_id = uuid.uuid4().hex
        value = {"schema":1,"matrix_id":matrix_id,"definition":spec,"definition_sha256":digest(spec),
                 "runner_revision":revision,"created_at":created,"deadline_at":created+deadline_seconds,
                 "peak_inflight":0,"entries":[]}
        value["binding_sha256"]=binding_hash(value)
        entries = []
        for index,sample in enumerate(spec["samples"]):
            # Persist a retry key before dispatch: even a crash after a fast completion cannot replay it.
            entries.append({"sample_id": "s" + str(index), "sample": sample, "status": "queued_local",
                            "request_id": None, "dispatch_key": dispatch_key(value,index)})
        value["entries"]=entries
        if runner_batch_size > 1 or execution_policy == "adaptive":
            value["schema"] = 3 if execution_policy == "adaptive" else 2
            value["groups"] = []
            topology = ([g["sample_indices"] for g in spec["adaptive_plan"]["groups"]] if execution_policy == "adaptive"
                        else [list(range(start, min(start + runner_batch_size, len(entries))))
                              for start in range(0, len(entries), runner_batch_size)])
            for index, indices in enumerate(topology):
                group = {"group_id": "g" + str(index), "sample_indices": indices,
                         "dispatch_key": group_dispatch_key(value, index, indices),
                         "status": "queued_local", "request_id": None}
                value["groups"].append(group)
                for member, sample_index in enumerate(indices):
                    entries[sample_index].update(group_id=group["group_id"], group_index=member, matrix_id=matrix_id)
        hostlab.write_json(path(matrix_id), value)
        if binding:
            binding.write_text(matrix_id, encoding="ascii")
        return {**summary(value), "created": True, "reused": False}
    finally:
        lock.close()


def recover(matrix_id, gh, *, repository, idempotency_key="", include_unverified_results=False):
    """Default to confirmed failures; only explicit opt-in may repeat unverified completed work."""
    original = load(matrix_id)
    if type(include_unverified_results) is not bool:
        raise ValueError("include_unverified_results must be boolean")
    if idempotency_key and not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", idempotency_key):
        raise ValueError("invalid matrix recovery idempotency key")
    samples = [e["sample"] for e in original["entries"] if e["status"] in {"failed", "skipped"}
        or include_unverified_results and e["status"] == "awaiting_results" and e.get("request_id")
        and e.get("result_run", {}).get("status") == "completed"]
    if not samples:
        raise ValueError("matrix has no eligible confirmed failures or opted-in unverified completed results")
    spec = original["definition"]
    identity = {"matrix_id": matrix_id, "key": idempotency_key}
    if include_unverified_results:
        identity["include_unverified_results"] = True
    key = "vmrecover_" + digest(identity)[:48]
    return create(samples, spec["request"], gh, repository=repository,
        max_parallel=spec["max_parallel"], reuse_completed=False,
        deadline_seconds=spec["deadline_seconds"], idempotency_key=key,
        runner_batch_size=spec.get("runner_batch_size", 1), _runner_revision=original["runner_revision"],
        execution_policy=spec.get("execution_policy", "fixed"))


def advance(matrix_id, gh, lookup, runs, *, repository, workflow, dispatch=True, collect_group=None):
    target = path(matrix_id)
    if not target.exists():
        raise ValueError("unknown matrix ID")
    lock = remote_schedule.admission_lock(target.with_suffix(".lock"))
    if lock is None:
        return {"matrix_id": matrix_id, "status": "scheduler_busy"}
    try:
        matrix = load(matrix_id)
        matrix["poll_errors"] = []
        try:
            recent = runs()
        except Exception as exc:
            matrix["poll_errors"]=[{"error":type(exc).__name__,"phase":"queue_snapshot"}]
            hostlab.write_json(target,matrix)
            return summary(matrix)
        observed={r.get("display_title","").removeprefix("hostlab-"):r for r in recent}
        if "groups" in matrix:
            return advance_groups(matrix, target, gh, lookup, recent, observed,
                repository=repository, workflow=workflow, dispatch=dispatch, collect_group=collect_group)
        for entry in matrix["entries"]:
            if entry["status"] in TERMINAL or not entry["request_id"]:
                continue
            try:
                run = observed.get(entry["request_id"]) or lookup(entry["request_id"])
            except Exception as exc:
                matrix["poll_errors"].append({"sample_id":entry["sample_id"], "error":type(exc).__name__})
                continue
            if run is not None:
                hostlab.write_json(hostlab.STATE/"remote-job-map"/(entry["request_id"]+".json"),{"run_id":run["id"]})
                entry.update(run_id=run["id"], run_url=run["html_url"], conclusion=run.get("conclusion"))
                if run["status"] == "completed":
                    entry["result_run"] = {key: run[key] for key in (
                        "id", "status", "conclusion", "html_url", "head_sha", "run_attempt", "display_title", "run_started_at") if key in run}
                entry["status"] = ("complete" if run.get("conclusion") == "success" else "failed") if run["status"] == "completed" else run["status"]
                remote_schedule.observe(entry["request_id"], run)
        active = sum(e["status"] not in TERMINAL and bool(e["request_id"]) for e in matrix["entries"])
        if time.time() >= matrix["deadline_at"]:
            for entry in matrix["entries"]:
                if entry["status"] == "queued_local":
                    entry.update(status="skipped", reason="matrix_submission_deadline")
        elif dispatch:
            budget = min(2, matrix["definition"]["max_parallel"] - active)
            for entry in matrix["entries"]:
                if budget <= 0:
                    break
                if entry["status"] != "queued_local":
                    continue
                sample = entry["sample"]
                try:
                    result = remote_schedule.submit(sample["version_code"], matrix["definition"]["request"],
                        gh, lookup, lambda:recent, repository=repository, workflow=workflow,
                        apk_sha256=sample["apk_sha256"], sample_revision=sample["sample_revision"],
                        idempotency_key=entry["dispatch_key"], runner_revision=matrix["runner_revision"],
                        reuse_completed=matrix["definition"]["reuse_completed"])
                except Exception as exc:
                    # A pre-dispatch read may fail; persisted per-entry keys protect ambiguous writes.
                    matrix["poll_errors"].append({"sample_id":entry["sample_id"], "error":type(exc).__name__})
                    break
                if result.get("request_id"):
                    entry.update(request_id=result["request_id"], status=result["status"],
                                 reused=result.get("reused",False), accepted_at=time.time())
                    if result["status"] == "completed":
                        entry["status"] = "complete" if result.get("conclusion") == "success" else "failed"
                    else:
                        active += 1
                    budget -= 1
                    hostlab.write_json(target, matrix)
                else:
                    entry["deferred_reason"] = result["status"]
                    break
        matrix["peak_inflight"] = max(matrix["peak_inflight"], active)
        hostlab.write_json(target, matrix)
        return summary(matrix)
    finally:
        lock.close()


def advance_groups(matrix, target, gh, lookup, recent, observed, *, repository, workflow,
                   dispatch, collect_group):
    """Refresh physical jobs, then resolve every member from verified group results."""
    pending_results = []
    for group in matrix["groups"]:
        if group["status"] in TERMINAL or not group["request_id"]:
            continue
        members = [matrix["entries"][i] for i in group["sample_indices"]]
        try:
            run = group.get("result_run") if group["status"] == "awaiting_results" else None
            run = run or observed.get(group["request_id"]) or lookup(group["request_id"])
        except Exception as exc:
            matrix["poll_errors"].append({"group_id": group["group_id"], "error": type(exc).__name__})
            continue
        if run is None:
            continue
        hostlab.write_json(hostlab.STATE / "remote-job-map" / (group["request_id"] + ".json"), {"run_id": run["id"]})
        details = {"run_id": run["id"], "run_url": run["html_url"], "conclusion": run.get("conclusion")}
        group.update(details)
        remote_schedule.observe(group["request_id"], run)
        if run["status"] != "completed":
            group["status"] = run["status"]
            for entry in members:
                entry.update(details, status=run["status"])
            continue
        snapshot = {key: run[key] for key in (
            "id", "status", "conclusion", "html_url", "head_sha", "run_attempt", "display_title", "run_started_at") if key in run}
        group.update(status="awaiting_results", result_run=snapshot)
        for entry in members:
            entry.update(details, status="awaiting_results", result_run=snapshot)
        pending_results.append((group, members, snapshot, group_payload(matrix, group)))

    if pending_results:
        # Persist accepted run snapshots before any network collection. Worker threads
        # only collect; validation, matrix state changes and publication stay here.
        hostlab.write_json(target, matrix)
        def collect_finished(item):
            if collect_group is None:
                raise ValueError("group_result_collector_unavailable")
            group, _, snapshot, payload = item
            return collect_group({**group, "runner_revision": matrix["runner_revision"]}, payload, snapshot)

        with ThreadPoolExecutor(max_workers=min(4, len(pending_results)), thread_name_prefix="hostlab-group-collect") as pool:
            futures = [pool.submit(collect_finished, item) for item in pending_results]
            for (group, members, _, _), future in zip(pending_results, futures):
                # Failed/cancelled jobs can contain successful earlier members.
                # Collection failures retain their request and never cause paid replay.
                try:
                    collected = future.result()
                    rows = collected["members"]
                    if (not isinstance(rows, list) or len(rows) != len(members)
                            or sorted(row.get("index", -1) for row in rows) != list(range(len(members)))):
                        raise ValueError("group result members changed")
                    by_index = {row["index"]: row for row in rows}
                    for index, entry in enumerate(members):
                        row = by_index[index]
                        if row.get("sample") != entry["sample"] or row.get("status") not in TERMINAL:
                            raise ValueError("group result member identity changed")
                    for index, entry in enumerate(members):
                        row = by_index[index]
                        entry["status"] = row["status"]
                        if row.get("reason"):
                            entry["reason"] = row["reason"]
                    group["status"] = "complete" if all(e["status"] == "complete" for e in members) else "failed"
                    group.pop("collection_error", None)
                except Exception as exc:
                    import remote_artifacts
                    code = str(exc) if isinstance(exc, remote_artifacts.ArtifactError) else type(exc).__name__
                    group["collection_error"] = code
                    matrix["poll_errors"].append({"group_id": group["group_id"], "phase": "group_results",
                                                  "error": code})
                hostlab.write_json(target, matrix)

    active = sum(g["status"] not in TERMINAL | {"awaiting_results"} and bool(g["request_id"])
                 for g in matrix["groups"])
    if time.time() >= matrix["deadline_at"]:
        for group in matrix["groups"]:
            if group["status"] == "queued_local":
                group.update(status="skipped", reason="matrix_submission_deadline")
                for index in group["sample_indices"]:
                    matrix["entries"][index].update(status="skipped", reason="matrix_submission_deadline")
    elif dispatch:
        dispatch_limit = 4 if matrix["definition"].get("execution_policy") == "adaptive" else 2
        budget = min(dispatch_limit, matrix["definition"]["max_parallel"] - active)
        for group in matrix["groups"]:
            if budget <= 0:
                break
            if group["status"] != "queued_local":
                continue
            payload = group_payload(matrix, group)
            try:
                options = {"execution": payload["execution"]} if "execution" in payload else {}
                result = remote_schedule.submit_group(payload["samples"], payload["request"], gh, lookup, lambda: recent,
                    repository=repository, workflow=workflow, idempotency_key=group["dispatch_key"],
                    runner_revision=matrix["runner_revision"], reuse_completed=matrix["definition"]["reuse_completed"], **options)
            except Exception as exc:
                matrix["poll_errors"].append({"group_id": group["group_id"], "error": type(exc).__name__})
                break
            if not result.get("request_id"):
                group["deferred_reason"] = result["status"]
                break
            status = "awaiting_results" if result["status"] == "completed" else result["status"]
            accepted = {"request_id": result["request_id"], "status": status,
                        "reused": result.get("reused", False), "accepted_at": time.time()}
            group.update(accepted)
            for index in group["sample_indices"]:
                matrix["entries"][index].update(accepted)
            if status != "awaiting_results":
                active += 1
            budget -= 1
            hostlab.write_json(target, matrix)
    matrix["peak_inflight"] = max(matrix["peak_inflight"], active)
    hostlab.write_json(target, matrix)
    return summary(matrix)


def attributes(output):
    """Exclude DEX layout from semantic row hashes; retain bounded field-layout previews."""
    columns=output.get("columns",[])
    if "descriptor" not in columns:
        return {},{}
    hashes={};previews={}
    for row in output.get("rows",[]):
        values=dict(zip(columns,row))
        descriptor=values.pop("descriptor")
        values.pop("file_id",None)
        if not isinstance(descriptor,str):
            continue
        hashes.setdefault(descriptor,[]).append(digest(values))
        if len(previews)<10 or descriptor in previews:
            previews[descriptor]={key:({"chars":len(value),"sha256":digest(value),"preview":value[:160],"preview_truncated":True}
                if isinstance(value,str) and len(value)>300 else value) for key,value in values.items()}
    return {key:sorted(value) for key,value in hashes.items()},previews


def compare(matrix_id, job_result, offset=0, limit=8, *, download_parallel=4, collect=None):
    """Bound concurrent callers as well as each caller's download workers."""
    if not COLLECTION_SLOTS.acquire(timeout=60):
        raise ValueError("collection_busy_retry_same_matrix")
    try:
        return _compare(matrix_id,job_result,offset,limit,download_parallel=download_parallel,collect=collect)
    finally:
        COLLECTION_SLOTS.release()


def collect_entries(sequence, job_result, collect, download_parallel):
    def fetch(entry):
        if entry["status"] != "complete":
            return None, None
        try:
            value = collect(entry) if collect else job_result(entry["request_id"])
            return json.loads(value), None
        except Exception as exc:
            import remote_artifacts
            return None, str(exc) if isinstance(exc, remote_artifacts.ArtifactError) else type(exc).__name__
    with ThreadPoolExecutor(max_workers=download_parallel, thread_name_prefix="hostlab-collect") as pool:
        return list(pool.map(fetch, sequence))


def prefetch(matrix_id, collect, offset=0, limit=8, *, download_parallel=4):
    """Collect completed page entries while later versions run; never dispatch or compare."""
    analysis_plan.integer(offset,0,MAX_SAMPLES,"offset")
    analysis_plan.integer(limit,1,8,"limit")
    analysis_plan.integer(download_parallel,1,4,"download_parallel")
    if not COLLECTION_SLOTS.acquire(timeout=60):
        raise ValueError("collection_busy_retry_same_matrix")
    try:
        matrix=load(matrix_id)
        selected=matrix["entries"][offset:offset+limit]
        fetched=collect_entries(selected,None,collect,download_parallel)
        rows=[];errors=[]
        for entry,(value,error) in zip(selected,fetched):
            row={"sample_id":entry["sample_id"],"version_code":entry["sample"]["version_code"],"status":entry["status"],
                 "collection_status":"pending" if entry["status"] not in TERMINAL else "skipped"}
            if error:
                row.update(collection_status="error",collection_error=error)
                errors.append({"sample_id":entry["sample_id"],"error":error})
            elif value is not None:
                row.update(collection_status="complete",collection={key:value[key] for key in (
                    "cache_hit","artifact","integrity","elapsed_ms","run_attempt") if key in value})
            rows.append(row)
        return {"matrix_id":matrix_id,"prefetch_only":True,"offset":offset,
            "next_offset":offset+limit if offset+limit<len(matrix["entries"]) else None,
            "matrix_finished":summary(matrix)["finished"],"entries":rows,"collection_errors":errors,
            "scope":"verified_artifact_prefetch_only_no_candidate_comparison_or_dispatch"}
    finally:
        COLLECTION_SLOTS.release()


def _compare(matrix_id, job_result, offset=0, limit=8, *, download_parallel=4, collect=None):
    """Download only completed bounded results and compare descriptors, not DEX positions."""
    matrix = load(matrix_id)
    if not all(e["status"] in TERMINAL for e in matrix["entries"]):
        raise ValueError("matrix has unfinished entries; advance/status before collecting")
    analysis_plan.integer(offset,0,MAX_SAMPLES,"offset")
    analysis_plan.integer(limit,1,8,"limit")
    analysis_plan.integer(download_parallel,1,4,"download_parallel")
    versions = []
    baseline = None
    baseline_attributes={}
    all_complete = all(e["status"]=="complete" for e in matrix["entries"])
    selected=matrix["entries"][offset:offset+limit]
    baseline_entry=next((e for e in matrix["entries"] if e["status"]=="complete"),None)
    sequence=([baseline_entry] if baseline_entry and baseline_entry not in selected else [])+selected
    downloads = collect_entries(sequence,job_result,collect,download_parallel)
    collection_errors = []
    for entry, (downloaded, error) in zip(sequence, downloads):
        row = {"sample_id":entry["sample_id"], "sample":entry["sample"], "request_id":entry["request_id"],
               "status":entry["status"], "run_url":entry.get("run_url"), "tasks":{}}
        if entry["status"] != "complete":
            all_complete = False
            versions.append(row)
            continue
        if error:
            all_complete = False
            row.update(collection_status="error", collection_error=error)
            collection_errors.append({"sample_id":entry["sample_id"], "error":error})
            if entry in selected:
                versions.append(row)
            continue
        row.update(collection_status="complete", collection={key:downloaded[key] for key in (
            "cache_hit", "artifact", "integrity", "elapsed_ms", "run_attempt") if key in downloaded})
        files = [Path(p) for p in downloaded["files"]]
        result_files = [p for p in files if p.name == "result.txt"]
        job_files = [p for p in files if p.name == "job.json"]
        if len(result_files) != 1 or len(job_files) != 1 or result_files[0].stat().st_size > 2*1024*1024:
            raise ValueError("ambiguous or oversized matrix result")
        result = json.loads(result_files[0].read_text(encoding="utf-8"))
        metadata = json.loads(job_files[0].read_text(encoding="utf-8"))
        sample = entry["sample"]
        if (metadata.get("operation") != "batch" or metadata.get("apk_sha256") != sample["apk_sha256"]
                or metadata.get("version_code") != sample["version_code"]
                or metadata.get("sample_revision") != sample["sample_revision"]
                or metadata.get("runner_revision") != matrix["runner_revision"]
                or metadata.get("request_sha256") != analysis_plan.fingerprint(matrix["definition"]["request"])):
            raise ValueError("matrix result identity does not match its immutable submission")
        row.update(complete=result.get("complete",False), fetch_ms=metadata.get("fetch_ms"),
                   total_ms=metadata.get("total_ms"), files=[str(p) for p in files])
        all_complete &= bool(row["complete"])
        for task in result["tasks"]:
            output = task.get("result",{})
            summary_task = {"status":task["status"], "backend":task["backend"], "elapsed_ms":task.get("elapsed_ms"),
                            "reused_from":task.get("reused_from"), "partial":output.get("partial",False)}
            attribute_hashes,preview=attributes(output)
            if attribute_hashes:
                summary_task.update(attribute_hashes=attribute_hashes,attributes=preview,
                                    attributes_preview_truncated=len(attribute_hashes)>10)
                previous=baseline_attributes.get(task["id"],{})
                changed=[name for name,hashes in attribute_hashes.items() if name in previous and previous[name]!=hashes]
                summary_task["changed_attributes_vs_first_version"]={"descriptors":changed[:20],"preview_truncated":len(changed)>20}
            if "smali" in output:
                summary_task.update(smali_sha256=digest(output["smali"]),code_units=output.get("code_units"))
            identities = output.get("identities")
            if identities is None and "descriptor" in output.get("columns",[]):
                column = output["columns"].index("descriptor")
                identities = [{"descriptor":r[column]} for r in output.get("rows",[]) if isinstance(r[column],str)]
                summary_task["candidate_source"] = "explicit_descriptor_query_column"
            if identities is not None:
                bag = Counter(r["descriptor"] for r in identities)
                summary_task.update(rows=len(identities), distinct=len(bag), identity_sha256=digest(sorted(bag.items())),
                                    descriptors=dict(sorted(bag.items())[:50]), preview_truncated=len(bag)>50)
                if baseline is not None and task["id"] in baseline:
                    older = Counter(baseline[task["id"]])
                    added,removed=bag-older,older-bag
                    summary_task["vs_first_version"] = {"added":dict(added.most_common(20)),
                        "removed":dict(removed.most_common(20)),"preview_truncated":len(added)>20 or len(removed)>20}
            row["tasks"][task["id"]] = summary_task
        if baseline is None and entry == baseline_entry:
            baseline = {}
            for task in result["tasks"]:
                output=task.get("result",{})
                baseline_attributes[task["id"]]=attributes(output)[0]
                if "identities" in output:
                    baseline[task["id"]]=Counter(r["descriptor"] for r in output["identities"])
                elif "descriptor" in output.get("columns",[]):
                    column=output["columns"].index("descriptor")
                    baseline[task["id"]]=Counter(r[column] for r in output.get("rows",[]) if isinstance(r[column],str))
        if entry in selected:
            versions.append(row)
    report = {"schema":1,"matrix_id":matrix_id,"runner_revision":matrix["runner_revision"],
              "definition_sha256":matrix["definition_sha256"],"all_analysis_complete":all_complete,
              "max_parallel":matrix["definition"]["max_parallel"],"peak_inflight":matrix["peak_inflight"],
              "reuse_completed":matrix["definition"]["reuse_completed"],"versions":versions,
              "offset":offset,"next_offset":offset+limit if offset+limit<len(matrix["entries"]) else None,
              "sample_count":len(matrix["entries"]),
              "baseline_sample":baseline_entry["sample"] if baseline_entry else None,
              "baseline_rule":"first_successful_input_sample",
              "baseline_collection_complete":baseline is not None,
              "collection_errors":collection_errors,"download_parallel":download_parallel,
              "scope":"offline_static_only","runtime_compatibility_verified":False}
    # Each caller receives an immutable snapshot; concurrent reads cannot overwrite its result.
    destination = directory() / (matrix_id + "-comparison-"+str(offset)+"-"+uuid.uuid4().hex+".json")
    hostlab.write_json(destination,report)
    rendered = json.dumps(report,ensure_ascii=False)
    if len(rendered.encode()) > 24000:
        return {"matrix_id":matrix_id,"all_analysis_complete":all_complete,"file":str(destination),
                "preview_truncated":True,"sample_count":len(matrix["entries"]),"next_offset":report["next_offset"],
                "collection_errors":collection_errors,"download_parallel":download_parallel,"versions":[{"sample":r["sample"],"status":r["status"],
                    "collection_status":r.get("collection_status"),"collection":r.get("collection"),
                    "tasks":{k:{key:value for key,value in v.items() if key not in {"descriptors","vs_first_version","attributes","attribute_hashes","changed_attributes_vs_first_version"}}
                             for k,v in list(r["tasks"].items())[:8]}} for r in versions[:8]]}
    return {**report,"file":str(destination),"preview_truncated":False}
