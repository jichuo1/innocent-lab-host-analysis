"""Durable, caller-driven bounded multi-version analysis. No background paid work."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import time
import uuid

import analysis_plan
import hostlab
import remote_schedule

MAX_SAMPLES = 40
TERMINAL = {"complete", "failed", "skipped"}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def definition(samples, request, max_parallel=4, reuse_completed=True, deadline_seconds=1800):
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
    return {"samples": normalized, "request": analysis_plan.validate(request),
            "max_parallel": analysis_plan.integer(max_parallel, 1, 4, "max_parallel"),
            "reuse_completed": reuse_completed,
            "deadline_seconds": analysis_plan.integer(deadline_seconds, 1, 7200, "deadline_seconds")}


def plan(samples, request, max_parallel=4, reuse_completed=True, deadline_seconds=1800):
    spec = definition(samples, request, max_parallel, reuse_completed, deadline_seconds)
    return {"schema": 1, "definition_sha256": digest(spec), "samples": spec["samples"],
            "sample_count": len(spec["samples"]), "duplicate_samples_removed": len(samples)-len(spec["samples"]),
            "max_parallel": spec["max_parallel"], "reuse_completed": spec["reuse_completed"],
            "deadline_seconds": spec["deadline_seconds"], "batch_plan": analysis_plan.plan(spec["request"]),
            "tool_revision": "one_immutable_commit_for_the_entire_matrix",
            "advance_dispatch_budget": 2, "execution": "caller_driven_no_background_dispatch",
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
    return value


def summary(matrix):
    counts = Counter(e["status"] for e in matrix["entries"])
    finished = all(e["status"] in TERMINAL for e in matrix["entries"])
    return {"matrix_id": matrix["matrix_id"], "runner_revision": matrix["runner_revision"],
            "definition_sha256": matrix["definition_sha256"], "sample_count": len(matrix["entries"]),
            "counts": dict(counts), "finished": finished, "complete": counts["complete"] == len(matrix["entries"]),
            "peak_inflight": matrix["peak_inflight"], "max_parallel": matrix["definition"]["max_parallel"],
            "created_at": matrix["created_at"], "deadline_at": matrix["deadline_at"],
            "entries": [{k:v for k,v in e.items() if k != "dispatch_key"} for e in matrix["entries"]],
            "next_action": "version_matrix_result" if finished else "advance_version_matrix",
            "poll_errors": matrix.get("poll_errors", []), "scope": "offline_static_only"}


def create(samples, request, gh, *, repository, max_parallel=4, reuse_completed=True,
           deadline_seconds=1800, idempotency_key=""):
    spec = definition(samples, request, max_parallel, reuse_completed, deadline_seconds)
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
            if old["definition_sha256"] != digest(spec):
                raise ValueError("matrix key is already bound to a different request")
            return {**summary(old), "created": False, "reused": True}
        revision = json.loads(gh(["api", f"repos/{repository}/git/ref/heads/main"]))["object"]["sha"]
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("invalid matrix tool revision")
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
        hostlab.write_json(path(matrix_id), value)
        if binding:
            binding.write_text(matrix_id, encoding="ascii")
        return {**summary(value), "created": True, "reused": False}
    finally:
        lock.close()


def advance(matrix_id, gh, lookup, runs, *, repository, workflow, dispatch=True):
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


def compare(matrix_id, job_result, offset=0, limit=8):
    """Download only completed bounded results and compare descriptors, not DEX positions."""
    matrix = load(matrix_id)
    if not all(e["status"] in TERMINAL for e in matrix["entries"]):
        raise ValueError("matrix has unfinished entries; advance/status before collecting")
    analysis_plan.integer(offset,0,MAX_SAMPLES,"offset")
    analysis_plan.integer(limit,1,8,"limit")
    versions = []
    baseline = None
    baseline_attributes={}
    all_complete = all(e["status"]=="complete" for e in matrix["entries"])
    selected=matrix["entries"][offset:offset+limit]
    baseline_entry=next((e for e in matrix["entries"] if e["status"]=="complete"),None)
    sequence=([baseline_entry] if baseline_entry and baseline_entry not in selected else [])+selected
    for entry in sequence:
        row = {"sample_id":entry["sample_id"], "sample":entry["sample"], "request_id":entry["request_id"],
               "status":entry["status"], "run_url":entry.get("run_url"), "tasks":{}}
        if entry["status"] != "complete":
            all_complete = False
            versions.append(row)
            continue
        downloaded = json.loads(job_result(entry["request_id"]))
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
        if baseline is None:
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
              "scope":"offline_static_only","runtime_compatibility_verified":False}
    destination = directory() / (matrix_id + "-comparison-"+str(offset)+".json")
    hostlab.write_json(destination,report)
    rendered = json.dumps(report,ensure_ascii=False)
    if len(rendered.encode()) > 24000:
        return {"matrix_id":matrix_id,"all_analysis_complete":all_complete,"file":str(destination),
                "preview_truncated":True,"sample_count":len(matrix["entries"]),"next_offset":report["next_offset"],"versions":[{"sample":r["sample"],"status":r["status"],
                    "tasks":{k:{key:value for key,value in v.items() if key not in {"descriptors","vs_first_version","attributes","attribute_hashes","changed_attributes_vs_first_version"}}
                             for k,v in list(r["tasks"].items())[:8]}} for r in versions[:8]]}
    return {**report,"file":str(destination),"preview_truncated":False}
