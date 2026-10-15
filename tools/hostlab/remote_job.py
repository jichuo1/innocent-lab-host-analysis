"""Trusted Actions entry point. Inputs are data, never interpolated shell code."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import hostlab
import analyze
import source_snapshot
import snapshot_transport


def run_batch(request, row, repo, revision, *, context_timings=None):
    import_started = time.monotonic()
    import asyncio
    import analysis_batch
    import analysis_plan
    import install_dexsql
    output = hostlab.STATE / "remote-output"
    output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    phases={**(context_timings or {}),"batch_import_ms":(started-import_started)*1000}
    fetch_timings={}
    try:
        apk = analyze.fetch_sample(row, repo, revision, timings=fetch_timings)
        fetch_ms = (time.monotonic() - started) * 1000
        sample = {**row, "source": "huggingface", "repo": repo, "revision": revision}
        analysis_started=time.monotonic()
        report = asyncio.run(analysis_batch.execute(apk, request, roots=[apk.parent], sample=sample))
        phases["analysis_ms"]=(time.monotonic()-analysis_started)*1000
        rc = 0 if report["complete"] else 2
    except Exception as exc:
        fetch_ms = None
        rc = 1
        report = {"complete": False, "scope": "offline_static_only", "error": type(exc).__name__,
                  "message": str(exc)[:1000], "tasks": []}
    (output / "result.txt").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    here = Path(__file__).resolve().parent
    names = ("analysis_plan.py", "analysis_batch.py", "install_dexsql.py", "analyze.py", "hostlab.py",
             "remote_job.py", "prepare_runtime.py", "dexq/server.py", "dexq/dexq_workers.py")
    prepared=hostlab.STATE/"preparation.json"
    preparation=json.loads(prepared.read_text(encoding="utf-8")) if prepared.is_file() and prepared.stat().st_size<=65536 else None
    job = {"operation": "batch", "version_code": row["version_code"], "apk_sha256": row["sha256"],
           "sample_revision": revision, "scope": "offline_static_only", "exit_code": rc,
           "request_sha256": analysis_plan.fingerprint(request), "complete": report["complete"],
           "backend_versions": report.get("backend_versions"),
           "tools": {name: hostlab.digest(here / name) for name in names},
           "runner_revision": os.environ.get("HOSTLAB_RUNNER_REVISION") or os.environ.get("GITHUB_SHA"),
           "workflow_revision": os.environ.get("GITHUB_SHA"), "fetch_ms": fetch_ms,
           "phases":{**phases,**fetch_timings},"preparation":preparation,
           "total_ms": (time.monotonic() - started) * 1000}
    hostlab.write_json(output / "job.json", job)
    print(json.dumps({"operation": "batch", "complete": report["complete"], "exit_code": rc,
                      "tasks": [{"id": t["id"], "status": t["status"]} for t in report["tasks"]]}))
    return rc


def run_validation(argument, row, repo, revision):
    import asyncio
    import shutil
    import uuid
    import verify_backends
    options = json.loads(argument or "{}")
    if not isinstance(options, dict) or set(options) - {"rounds", "jadx"}:
        raise ValueError("unsupported validation options")
    rounds = options.get("rounds", 2)
    if type(rounds) is not int or rounds not in {1,2,3} or type(options.get("jadx", True)) is not bool:
        raise ValueError("invalid validation rounds/JADX flag")
    output = hostlab.STATE / "remote-output"
    output.mkdir(parents=True, exist_ok=True)
    work = hostlab.STATE / "backend-validation" / uuid.uuid4().hex
    rc = 1
    result = {"complete": False, "scope": "offline_static_only"}
    try:
        apk = analyze.fetch_sample(row, repo, revision)
        sample = {**row, "source": "huggingface", "repo": repo, "revision": revision}
        proof = asyncio.run(verify_backends.verify(apk, sample, work, rounds=rounds, jadx=options.get("jadx", True)))
        shutil.copyfile(work / "verification.json", output / "verification.json")
        result.update(complete=True, verification=proof)
        rc = 0
    except Exception as exc:
        result.update(error=type(exc).__name__, message=str(exc)[:1000])
        if (work / "failure.json").is_file():
            shutil.copyfile(work / "failure.json", output / "failure.json")
    (output / "result.txt").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    names = ("verify_backends.py", "analysis_batch.py", "analysis_plan.py", "install_dexsql.py", "remote_job.py")
    hostlab.write_json(output / "job.json", {"operation": "backend_validation", "version_code": row["version_code"],
        "apk_sha256": row["sha256"], "sample_revision": revision, "exit_code": rc,
        "scope": "offline_static_only", "complete": result["complete"],
        "tools": {name: hostlab.digest(Path(__file__).with_name(name)) for name in names}})
    print(json.dumps({"operation": "backend_validation", "complete": result["complete"], "exit_code": rc}))
    return rc


def main():
    entry_started=time.monotonic()
    code = os.environ["HOSTLAB_VERSION"]
    operation = os.environ["HOSTLAB_OPERATION"]
    argument = os.environ.get("HOSTLAB_ARGUMENT", "")
    if not re.fullmatch(r"[1-9][0-9]{0,9}", code) or (len(argument.encode("utf-8")) > 30000 if operation == "batch" else len(argument) > 4096):
        raise RuntimeError("Invalid bounded input")
    batch_request = None
    if operation == "batch":
        import analysis_plan
        batch_request = analysis_plan.validate(json.loads(argument))
        runner_revision = os.environ.get("HOSTLAB_RUNNER_REVISION", "")
        if runner_revision:
            if not re.fullmatch(r"[0-9a-f]{40}", runner_revision):
                raise RuntimeError("Invalid runner revision")
            observed = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            if observed != runner_revision:
                raise RuntimeError("Runner checkout does not match scheduled source")
    raw_max_cell = os.environ.get("HOSTLAB_MAX_CELL_CHARS", "300")
    if not re.fullmatch(r"[0-9]{1,5}", raw_max_cell) or not 1 <= int(raw_max_cell) <= 16000:
        raise RuntimeError("max_cell_chars must be 1..16000")
    max_cell_chars = int(raw_max_cell)
    if operation != "query" and max_cell_chars != 300:
        raise RuntimeError("max_cell_chars is only supported for query")
    if operation == "regenerate_ai":
        import regenerate_report
        regenerate_report.main()
        return 0
    if operation == "source_check":
        context, binding = snapshot_transport.load_for_analysis(os.environ.get("HOSTLAB_MODULE_SOURCE", ""))
        snapshot_transport.cache_snapshot(context, binding)
        output = hostlab.STATE / "remote-output"
        output.mkdir(parents=True, exist_ok=True)
        metadata = source_snapshot.public_context(context, binding)
        hostlab.write_json(output / "job.json", {"operation": operation, "scope": "source_metadata_only",
            "exit_code": 0, "source_snapshot": metadata,
            "tools": {name: hostlab.digest(Path(__file__).with_name(name))
                      for name in ("remote_job.py", "source_snapshot.py", "snapshot_transport.py")}})
        (output / "result.txt").write_text(json.dumps({"source_binding_verified": True,
            "snapshot_sha256": binding["snapshot_sha256"], "source_tree_sha256": context["source_tree_sha256"],
            "file_count": len(context["source_records"]), "origin": binding["origin"]}), encoding="utf-8")
        return 0
    module_source = None
    if operation == "multipath_audit":
        context, binding = snapshot_transport.load_for_analysis(os.environ.get("HOSTLAB_MODULE_SOURCE", ""))
        source_snapshot.validate(context, expected_sha256=binding["snapshot_sha256"])
        snapshot_transport.cache_snapshot(context, binding)
        module_source = source_snapshot.public_context(context, binding)
        module_source["freshness"] = ("dispatch_worktree_snapshot" if binding.get("origin") == "worktree"
                                      else "published_unverified_worktree")
        # The subprocess must use the same immutable source selected before scanning.
        os.environ["HOSTLAB_MODULE_SOURCE"] = json.dumps(binding, separators=(",", ":"))
    os.environ["DEXQ_WORKERS"] = "2"
    repo = "innocent-lab-dev/bilibili-host-apks"
    context_started=time.monotonic()
    _, current_head = hostlab.api_private(repo)
    context_timings={"repo_info_ms":(time.monotonic()-context_started)*1000}
    head = os.environ.get("HOSTLAB_REVISION") or current_head
    sha = os.environ.get("HOSTLAB_SHA") or None
    if not re.fullmatch(r"[0-9a-f]{40}", head) or (sha and not re.fullmatch(r"[0-9a-f]{64}", sha)):
        raise RuntimeError("Invalid immutable sample identity")
    manifest_started=time.monotonic()
    samples = hostlab.manifest(repo, head)["samples"]
    context_timings["manifest_ms"]=(time.monotonic()-manifest_started)*1000
    if operation == "inventory":
        output = hostlab.STATE / "remote-output"
        output.mkdir(parents=True, exist_ok=True)
        keys = ("version_code", "version_name", "sha256", "size", "certificate_sha256")
        inventory = {"schema": 1, "sample_revision": head,
                     "samples": [{k: r[k] for k in keys if k in r}
                                 for r in sorted(samples, key=lambda r: (r["version_code"], r["sha256"]))]}
        hostlab.write_json(output / "inventory.json", inventory)
        hostlab.write_json(output / "job.json", {"operation": operation, "sample_revision": head,
                           "sample_count": len(samples), "exit_code": 0, "scope": "metadata_only"})
        return 0
    row = hostlab.select({"samples": samples}, int(code), sha)
    if operation == "batch":
        context_timings["entry_to_batch_ms"]=(time.monotonic()-entry_started)*1000
        return run_batch(batch_request, row, repo, head, context_timings=context_timings)
    if operation == "backend_validation":
        return run_validation(argument, row, repo, head)
    hostlab.write_json(hostlab.CONFIG, {"repo": repo})
    base = [sys.executable, str(Path(__file__).with_name("hostlab.py"))]
    source = ["--version-code", code, "--sha256", row["sha256"], "--revision", head]
    if operation == "multipath_audit":
        os.environ["HOSTLAB_REVISION"] = head
        os.environ["HOSTLAB_SHA"] = row["sha256"]
        if not os.environ.get("HOSTLAB_BASELINE_SHA"):
            candidates = [r for r in samples if r["version_code"] < row["version_code"] and
                          r.get("certificate_sha256") == row.get("certificate_sha256")]
            if candidates:
                os.environ["HOSTLAB_BASELINE_SHA"] = max(candidates, key=lambda r:r["version_code"])["sha256"]
        command = [sys.executable, str(Path(__file__).with_name("priority_analysis.py"))]
    elif operation == "audit":
        command = base + ["audit"] + source
    elif operation == "decompile":
        command = base + ["decompile"] + source + ["--class", argument]
    elif operation == "query":
        command = base + ["dexq", "query"] + source + ["--sql", argument, "--limit", "100",
                                                     "--max-cell-chars", str(max_cell_chars)]
    elif operation == "decode":
        command = base + ["dexq", "decode"] + source + ["--method", argument]
    elif operation == "string_refs":
        command = base + ["dexq", "refs"] + source + ["--kind", "string", "--target", argument, "--limit", "100"]
    elif operation == "info":
        command = base + ["dexq", "info"] + source
    else:
        raise RuntimeError("Unsupported operation")
    output = hostlab.STATE / "remote-output"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "result.txt").open("w", encoding="utf-8") as stream:
        try:
            rc = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                timeout=1500, check=False).returncode
        except subprocess.TimeoutExpired:
            stream.write("Task timed out\n")
            rc = 124
    tools = analyze.tool_hashes()
    if operation in {"query", "decode", "string_refs", "info"}:
        here = Path(__file__).resolve().parent
        for name in ("dexq/server.py", "dexq/dexq_workers.py", "dexq_cli.py", "remote_job.py"):
            tools[name] = hostlab.digest(here / name)
    job = {"version_code": int(code), "operation": operation,
        "apk_sha256": row["sha256"], "sample_revision": head, "exit_code": rc,
        "scope": "offline_static_only", "tools": tools}
    if operation == "query":
        job["max_cell_chars"] = max_cell_chars
    if module_source is not None:
        job["source_snapshot"] = module_source
    hostlab.write_json(output / "job.json", job)
    return rc


if __name__ == "__main__":
    sys.exit(main())
