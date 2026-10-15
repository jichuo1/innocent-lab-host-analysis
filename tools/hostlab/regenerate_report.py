"""Reuse immutable static evidence for a new AI review; no fake APK or baseline."""
import json
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import hostlab
import source_snapshot
import snapshot_transport


def review_source(data, explicit_binding):
    previous = data.get("source_snapshot") or {}
    if explicit_binding or previous.get("binding"):
        selected = explicit_binding or json.dumps(previous["binding"], separators=(",", ":"))
        context, binding = snapshot_transport.load_for_analysis(selected)
        source_snapshot.validate(context, expected_sha256=binding["snapshot_sha256"])
        snapshot_transport.cache_snapshot(context, binding)
        metadata = source_snapshot.public_context(context, binding)
        metadata["freshness"] = ("historical_static_evidence_new_source" if explicit_binding else "historical")
    else:
        if previous.get("schema", 0) >= 2:
            raise RuntimeError("Historical verified source binding is missing")
        metadata = {k:v for k,v in previous.items() if k not in {"source_records", "files"}}
        metadata.update({"schema": 0, "legacy": True, "freshness": "historical"})
        metadata["source_records"] = [{k:v for k,v in row.items() if k != "source"}
                                      for row in previous.get("source_records", previous.get("files", []))]
        if any("source" in row for row in previous.get("source_records", [])):
            raw = json.dumps(previous, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            digest = hashlib.sha256(raw).hexdigest()
            cache = hostlab.STATE / "source-snapshots" / ("legacy-" + digest) / "context.json"
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(raw)
            metadata["legacy_cache_sha256"] = digest
        digest = metadata.get("legacy_cache_sha256", "")
        cached = (hostlab.STATE / "source-snapshots" / ("legacy-" + digest) / "context.json"
                  if re.fullmatch(r"[0-9a-f]{64}", digest) else None)
        metadata["source_availability"] = ("legacy_private_cache_available" if cached and cached.is_file()
                                           else "legacy_source_unavailable")
        if metadata["source_availability"] == "legacy_source_unavailable":
            note = "历史报告缺少私有源码全文缓存；module_source 不可用，不会替换为最新源码。"
            if note not in data.setdefault("limitations", []):
                data["limitations"].append(note)
    return metadata


def argument(raw):
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > 4096:
        raise RuntimeError("Invalid regeneration argument")
    if re.fullmatch(r"[1-9][0-9]{0,19}", raw):
        value = {"static_run": int(raw)}
    else:
        value = json.loads(raw)
    if (not isinstance(value, dict) or set(value) - {"static_run", "checkpoint_run", "resume_unknown"}
            or type(value.get("static_run")) is not int or not 1 <= value["static_run"] < 10**20
            or "checkpoint_run" in value and (type(value["checkpoint_run"]) is not int or not 1 <= value["checkpoint_run"] < 10**20)
            or type(value.get("resume_unknown", False)) is not bool):
        raise RuntimeError("Expected static_run, optional checkpoint_run and boolean resume_unknown")
    return {**value, "resume_unknown": value.get("resume_unknown", False)}


def gh(args, payload=None):
    result = subprocess.run([os.environ.get("HOSTLAB_GH", "gh"), *args], capture_output=True,
        text=True, encoding="utf-8", timeout=60, check=False)
    if result.returncode:
        raise RuntimeError("Historical artifact metadata request failed")
    return result.stdout


def verified_artifact(run_id):
    import remote_artifacts
    repository = snapshot_transport.ANALYSIS_REPO
    run = json.loads(gh(["api", f"repos/{repository}/actions/runs/{run_id}"]))
    match = re.fullmatch(r"hostlab-([0-9a-f]{32})", run.get("display_title", ""))
    if run.get("id") != run_id or run.get("status") != "completed" or not match:
        raise RuntimeError("Historical run identity is unavailable")
    # AI failure does not invalidate successful frozen static evidence.
    downloaded = remote_artifacts.get(repository, match[1], run, gh, profile="frozen-report-v1")
    return run, downloaded


def one_file(downloaded, name, *, required=True):
    files = [Path(path) for path in downloaded["files"] if Path(path).name == name]
    if (required and len(files) != 1) or (not required and len(files) > 1):
        raise RuntimeError("Missing or ambiguous frozen evidence: " + name)
    return files[0] if files else None


def sample_identity(value):
    if (not isinstance(value, dict) or type(value.get("version_code")) is not int or value["version_code"] <= 0
            or not isinstance(value.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", value["sha256"])
            or not isinstance(value.get("revision"), str) or not re.fullmatch(r"[0-9a-f]{40}", value["revision"])):
        raise RuntimeError("Invalid frozen sample identity")
    return tuple(value[key] for key in ("version_code", "sha256", "revision"))


def frozen_inputs(run, downloaded, version_code):
    paths = {name: one_file(downloaded, name) for name in ("priority-summary.json", "priority-target.json", "priority-report.md", "job.json")}
    data = json.loads(paths["priority-summary.json"].read_text(encoding="utf-8"))
    target = json.loads(paths["priority-target.json"].read_text(encoding="utf-8"))
    job = json.loads(paths["job.json"].read_text(encoding="utf-8"))
    selected = sample_identity(data.get("sample"))
    if (selected[0] != version_code or sample_identity(target.get("sample")) != selected
            or type(job.get("version_code")) is not int or job.get("version_code") != selected[0] or job.get("apk_sha256") != selected[1]
            or job.get("sample_revision") != selected[2] or type(job.get("exit_code")) is not int
            or job["exit_code"] != 0 or job.get("operation") not in {"multipath_audit", "regenerate_ai"}):
        raise RuntimeError("Frozen static job/sample identity mismatch")
    rule = target.get("rule_sha256")
    if not isinstance(rule, str) or not re.fullmatch(r"[0-9a-f]{64}", rule):
        raise RuntimeError("Frozen static rule identity is missing")
    if not isinstance(data.get("page_path_matrix"), dict) or data["page_path_matrix"] != target.get("page_path_matrix"):
        raise RuntimeError("Frozen host page matrix differs from its target evidence")
    if data.get("baseline"):
        paths["priority-baseline.json"] = one_file(downloaded, "priority-baseline.json")
        baseline = json.loads(paths["priority-baseline.json"].read_text(encoding="utf-8"))
        if sample_identity(baseline.get("sample")) != sample_identity(data["baseline"]) or baseline.get("rule_sha256") != rule:
            raise RuntimeError("Frozen baseline identity or rules mismatch")
    records = [{"path": name, "bytes": path.stat().st_size, "sha256": hostlab.digest(path)} for name, path in sorted(paths.items())]
    matrix_hash = hashlib.sha256(source_snapshot.serialize(data["page_path_matrix"])).hexdigest()
    manifest = {"schema": 1, "source_run": {key: run[key] for key in ("id", "run_attempt", "head_sha")},
        "artifact": downloaded["artifact"], "sample": {key: data["sample"][key] for key in ("version_code", "sha256", "revision")},
        "baseline": {key: data["baseline"][key] for key in ("version_code", "sha256", "revision")} if data.get("baseline") else None,
        "rule_sha256": rule, "page_path_matrix_sha256": matrix_hash, "input_files": records,
        "immutable_restored_files": [record for record in records if record["path"] in {"priority-target.json", "priority-baseline.json"}]}
    return data, target, job, paths, manifest


def copy_verified(source, target):
    expected = (source.stat().st_size, hostlab.digest(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".restore-", suffix=".tmp", delete=False) as stream:
        temp = Path(stream.name)
    try:
        shutil.copyfile(source, temp)
        if (temp.stat().st_size, hostlab.digest(temp)) != expected:
            raise RuntimeError("Frozen evidence changed while restoring")
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)


def restore_reports(downloaded, samples):
    root = Path(downloaded["root"])
    identities = {(str(sample["version_code"]), sample["sha256"][:16]): sample_identity(sample) for sample in samples}
    files = {Path(path).relative_to(root).as_posix(): Path(path) for path in downloaded["files"]}
    for name, path in sorted(files.items()):
        parts = Path(name).parts
        if (len(parts) != 5 or parts[0] != "reports" or (parts[1], parts[2]) not in identities
                or not re.fullmatch(r"[0-9]{8}T[0-9]{6,12}Z", parts[3])
                or parts[4] not in {"summary.json", "features.tsv", "class.java"}):
            continue
        record_path = path.parent / "summary.json"
        if record_path.relative_to(root).as_posix() not in files:
            raise RuntimeError("Frozen report metadata is missing")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if sample_identity(record.get("sample")) != identities[(parts[1], parts[2])]:
            raise RuntimeError("Frozen report sample mismatch")
        if parts[4] == "class.java" and (record.get("command") != "decompile" or record.get("exit_code") != 0
                or record.get("source_written") is not True or not isinstance(record.get("class"), str)):
            raise RuntimeError("Frozen Java report identity is missing")
        copy_verified(path, hostlab.STATE.joinpath(*parts))


def refreshed_report(text, metadata, status):
    text = re.split(r"(?m)^# AI (?:适配分析|分析未完成)\s*$", text, maxsplit=1)[0].rstrip() + "\n"
    text = re.sub(r"(?m)^分析结果：.*$", "分析结果：" + status, text)
    section = "## 未归类的源码多路径候选\n\n" + "\n".join(
        "- " + path for path in metadata.get("unmapped_multi_path_candidates", [])) + "\n\n"
    pattern = r"(?ms)^## 未归类的源码多路径候选\s*\n.*?(?=^## |\Z)"
    return re.sub(pattern, lambda _: section, text) if re.search(pattern, text) else text + "\n" + section


def main():
    started = time.monotonic()
    options = argument(os.environ["HOSTLAB_ARGUMENT"])
    source_run = options["static_run"]
    run, downloaded = verified_artifact(source_run)
    data, target, job, paths, manifest = frozen_inputs(run, downloaded, int(os.environ["HOSTLAB_VERSION"]))
    original_matrix = source_snapshot.serialize(data["page_path_matrix"])
    previous = {"source_run": manifest["source_run"], "analysis_status": data.get("analysis_status"),
        "review_reasons": data.get("review_reasons"), "ai_status": data.get("ai_status"),
        "static_job_performance": {key: job[key] for key in
            ("operation", "preparation", "phases", "elapsed_ms", "elapsed_seconds", "command", "tools") if key in job},
        "source_snapshot": {key: val for key, val in (data.get("source_snapshot") or {}).items()
                            if key in {"schema", "binding", "repository_head", "source_tree_sha256", "captured_at", "freshness"}}}
    explicit = os.environ.get("HOSTLAB_MODULE_SOURCE", "")
    module_source = review_source(data, explicit)
    import priority_analysis
    outcome = priority_analysis.verdict(data["changes"], target, module_source, data.get("resource_changes"), bool(data.get("baseline")))
    data.pop("ai_review", None)
    original_static_run = data.get("static_evidence_run")
    data.update(ai_status="pending", regenerated_from_run=source_run,
        static_evidence_run=original_static_run if type(original_static_run) is int and original_static_run > 0 else source_run,
        source_rebound_for_review=bool(explicit), source_snapshot=module_source, previous_provenance=previous,
        ai_no_apk_access=True, ai_resume_unknown=options["resume_unknown"],
        analysis_status=outcome["status"], review_reasons=outcome["reasons"])
    destination = hostlab.STATE / "remote-output"
    destination.mkdir(parents=True, exist_ok=True)
    raw_manifest = source_snapshot.serialize(manifest)
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    data["static_manifest_sha256"] = manifest_hash
    data["static_artifact_cache"] = {key: downloaded[key] for key in ("root", "cache_hit", "integrity") if key in downloaded}
    if options.get("checkpoint_run"):
        _, checkpoint = verified_artifact(options["checkpoint_run"])
        checkpoint_manifest = one_file(checkpoint, "static-manifest.json")
        checkpoint_summary = json.loads(one_file(checkpoint, "priority-summary.json").read_text(encoding="utf-8"))
        if (hostlab.digest(checkpoint_manifest) != manifest_hash
                or checkpoint_summary.get("static_manifest_sha256") != manifest_hash
                or (checkpoint_summary.get("source_snapshot") or {}).get("binding") != module_source.get("binding")):
            raise RuntimeError("Checkpoint static/source binding differs; start a new generation explicitly")
        import ai_checkpoint
        ai_checkpoint.restore_checkpoint(destination, checkpoint["files"])
        data["checkpoint_from_run"] = options["checkpoint_run"]
    for record in manifest["immutable_restored_files"]:
        copy_verified(paths[record["path"]], destination / record["path"])
    restore_reports(downloaded, [data["sample"], *([data["baseline"]] if data.get("baseline") else [])])
    (destination / "priority-report.md").write_text(refreshed_report(paths["priority-report.md"].read_text(encoding="utf-8"),
        module_source, outcome["status"]), encoding="utf-8")
    # Original scan commands and timings belong to the frozen run, never this run.
    job = {key: job[key] for key in ("version_code", "version_name", "apk_sha256", "sample_revision", "baseline_sha256") if key in job}
    job.update(regenerated_from_run=source_run, static_evidence_run=data["static_evidence_run"], operation="regenerate_ai",
        scope="verified_static_restore_and_ai_only", exit_code=0, apk_analysis_rerun=False,
        runner_revision=os.environ.get("HOSTLAB_RUNNER_REVISION") or os.environ.get("GITHUB_SHA"),
        source_snapshot=module_source, source_rebound_for_review=bool(explicit), static_manifest_sha256=manifest_hash,
        previous_provenance=previous, ai_no_apk_access=True,
        regeneration_tools={name: hostlab.digest(Path(__file__).with_name(name)) for name in (
            "regenerate_report.py", "snapshot_transport.py", "source_snapshot.py", "priority_analysis.py")})
    for record in manifest["immutable_restored_files"]:
        path = destination / record["path"]
        if path.stat().st_size != record["bytes"] or hostlab.digest(path) != record["sha256"]:
            raise RuntimeError("Restored static manifest does not match original bytes")
    if source_snapshot.serialize(data["page_path_matrix"]) != original_matrix:
        raise RuntimeError("Frozen host page matrix changed during source rebinding")
    (destination / "static-manifest.json").write_bytes(raw_manifest)
    preparation = hostlab.STATE / "preparation.json"
    if preparation.is_file() and not preparation.is_symlink() and preparation.stat().st_size <= 1024*1024:
        current = json.loads(preparation.read_text(encoding="utf-8"))
        job["preparation"] = {key: current[key] for key in
            ("fingerprint", "cache_hit", "built", "repaired", "python", "requirements", "elapsed_ms") if key in current}
    job["phases"] = {"restore_static_and_source_ms": (time.monotonic()-started)*1000}
    hostlab.write_json(destination / "priority-summary.json", data)
    hostlab.write_json(destination / "job.json", job)
    print("Verified frozen evidence restored; APK access disabled for AI regeneration")


if __name__ == "__main__":
    main()
