"""Sealed bounded batch checkpoints and authenticated Actions result import."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

import analysis_plan
import hostlab

CONTRACT = 1
MAX_BYTES = 4 * 1024 * 1024
STABLE_TOOLS = ("hostlab.py", "analyze.py", "install_dexsql.py", "dexq/server.py", "dexq/dexq_workers.py")
LEGACY = {"analysis_plan.py": "870dc125afb0094643b7b225c521fd81dbd13900dba066f3c214ac93f113492f",
          "analysis_batch.py": "e215cf8de0b3e03d76d2051557ad564a557c6e52f891b97ba9f6c8619614401b",
          "remote_job.py": "36313eb8bd7791d9966acbf0ccd4504def165c27ec701b9f16b428ea9db51a03"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def checksum(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def work_request(request):
    return {key: value for key, value in analysis_plan.validate(request).items() if key != "resume"}


def work_hash(request):
    return analysis_plan.fingerprint(work_request(request))


def save(path, report, request, tools, *, sealed=False):
    payload = {"schema": 1, "batch_contract": CONTRACT, "request": work_request(request),
               "work_sha256": work_hash(request), "tools": tools,
               "sealed": sealed and report.get("source_unchanged") is True, "report": report}
    if len(canonical(payload)) > MAX_BYTES:
        raise ValueError("checkpoint_byte_budget")
    hostlab.write_json(Path(path), {"payload": payload, "sha256": checksum(payload)})


def read_json(path):
    path = Path(path)
    if not path.is_file() or not 0 < path.stat().st_size <= MAX_BYTES:
        raise ValueError("checkpoint_missing_or_oversized")
    return json.loads(path.read_text(encoding="utf-8"))


def validate(report, job, request, sample, tools, native, *, checkpoint=None):
    if not isinstance(report, dict) or not isinstance(job, dict):
        raise ValueError("invalid_checkpoint_record")
    expected_sample = {"version_code": sample["version_code"], "sha256": sample["sha256"], "revision": sample["revision"]}
    if (job.get("operation") != "batch" or job.get("version_code") != expected_sample["version_code"]
            or job.get("apk_sha256") != expected_sample["sha256"] or job.get("sample_revision") != expected_sample["revision"]
            or job.get("request_sha256") != work_hash(request) or report.get("source_unchanged") is not True
            or report.get("scope") != "offline_static_only"):
        raise ValueError("checkpoint_sample_request_or_source_mismatch")
    if any(report.get("sample", {}).get(k) != v for k, v in expected_sample.items()):
        raise ValueError("checkpoint_report_sample_mismatch")
    prior_tools = job.get("tools", {})
    if any(not tools.get(name) or prior_tools.get(name) != tools[name] for name in STABLE_TOOLS):
        raise ValueError("checkpoint_engine_tools_changed")
    legacy = all(prior_tools.get(name) == digest for name, digest in LEGACY.items())
    if not legacy and job.get("batch_contract") != CONTRACT:
        raise ValueError("checkpoint_contract_incompatible")
    if checkpoint is not None:
        payload = checkpoint.get("payload", {})
        if (checkpoint.get("sha256") != checksum(payload) or payload.get("schema") != 1
                or payload.get("sealed") is not True or payload.get("batch_contract") != CONTRACT
                or payload.get("work_sha256") != work_hash(request)
                or checksum(payload.get("report")) != checksum(report) or payload.get("tools") != prior_tools
                or payload.get("request") != work_request(request)):
            raise ValueError("checkpoint_seal_or_digest_mismatch")
    elif not legacy:
        raise ValueError("sealed_checkpoint_required")
    before = report.get("backend_versions", {}).get("dexsql", {})
    if any(before.get(k) != native.get(k) for k in ("version", "sha256")) or not native.get("available"):
        raise ValueError("checkpoint_native_backend_changed")
    tasks = report.get("tasks")
    wanted = {task["id"]: task for task in analysis_plan.validate(request)["tasks"]}
    if not isinstance(tasks, list) or len(tasks) > len(wanted) or len({t.get("id") for t in tasks}) != len(tasks):
        raise ValueError("checkpoint_task_set_mismatch")
    import analysis_paging
    total = 0
    for task in tasks:
        if task.get("id") not in wanted or task.get("status") not in {"complete", "partial", "error", "skipped"}:
            raise ValueError("checkpoint_task_identity_mismatch")
        spec = wanted[task["id"]]
        if task["status"] in {"complete", "partial"}:
            result = task.get("result")
            if not isinstance(result, dict) or result.get("partial") is not (task["status"] == "partial"):
                raise ValueError("checkpoint_task_completion_inconsistent")
            if spec["operation"] == "query" and task["backend"] == "dexsql":
                if "typed_result" in result:
                    page = analysis_paging.statement(result)
                    if not analysis_paging.sql_matches(page, spec["sql"]) or page["offset"] != spec["offset"]:
                        raise ValueError("checkpoint_query_identity_mismatch")
                elif result.get("rows") or task["status"] == "complete":
                    raise ValueError("checkpoint_query_page_missing")
            elif task["status"] == "partial":
                raise ValueError("checkpoint_partial_operation_not_resumable")
            total += analysis_paging.size(result)
    if total > 1024 * 1024:
        raise ValueError("checkpoint_result_budget")
    return copy.deepcopy(report)


def gh(args, *, timeout=30):
    return subprocess.check_output([os.environ.get("HOSTLAB_GH", "gh"), *args], stderr=subprocess.PIPE, timeout=timeout).decode("utf-8")


def load_actions(request, sample, tools, native):
    binding = request.get("resume")
    if binding is None:
        return None
    repository = os.environ.get("GITHUB_REPOSITORY", "jichuo1/innocent-lab-host-analysis")
    if repository != "jichuo1/innocent-lab-host-analysis":
        raise ValueError("checkpoint_repository_not_allowed")
    deadline = time.monotonic() + min(90, request["timeout_seconds"])
    def remaining():
        value = deadline - time.monotonic()
        if value <= 0:
            raise ValueError("checkpoint_import_deadline")
        return min(30, value)
    def retry(read):
        for attempt in range(3):
            try:
                return read()
            except (subprocess.SubprocessError, OSError):
                if attempt == 2:
                    raise ValueError("checkpoint_read_failed") from None
                time.sleep(min(.2 * 2**attempt, remaining()))
    def api(args):
        return retry(lambda: gh(args, timeout=remaining()))
    def download(endpoint, target):
        def read():
            with target.open("wb") as stream:
                subprocess.run([os.environ.get("HOSTLAB_GH", "gh"), "api", endpoint], stdout=stream,
                               stderr=subprocess.PIPE, timeout=remaining(), check=True)
        retry(read)
    import remote_artifacts
    run = json.loads(api(["api", f"repos/{repository}/actions/runs/{binding['run_id']}"]))
    if run.get("run_attempt") != binding["attempt"]:
        raise ValueError("checkpoint_run_attempt_changed")
    archive = remote_artifacts.get(repository, binding["request_id"], run, api, downloader=download)
    root = Path(archive["root"])
    job = read_json(root / "remote-output/job.json")
    report = read_json(root / "remote-output/result.txt")
    if (job.get("workflow_revision") != run["head_sha"]
            or not re.fullmatch(r"[0-9a-f]{40}", job.get("runner_revision", ""))):
        raise ValueError("checkpoint_producer_identity_mismatch")
    checkpoint_path = root / "remote-output/checkpoint.json"
    checkpoint = read_json(checkpoint_path) if checkpoint_path.exists() else None
    report = validate(report, job, request, sample, tools, native, checkpoint=checkpoint)
    report["resume_origin"] = {**binding, "runner_revision": job["runner_revision"],
        "artifact_id": archive["artifact"]["id"], "artifact_digest": archive["artifact"]["digest"],
        "work_sha256": work_hash(request), "result_sha256": hostlab.digest(root / "remote-output/result.txt"),
        "reused_complete_tasks": sum(t["status"] == "complete" for t in report["tasks"])}
    return report


def summary(path, report, *, error=None):
    if not path:
        return
    counts = {status: sum(t.get("status") == status for t in report.get("tasks", []))
              for status in ("complete", "partial", "error", "skipped")}
    lines = ["\n### Bounded dexq batch", "", f"- Complete: **{report.get('complete', False)}**; tasks: `{counts}`.",
             "- Completeness requires every task, admitted page, physical DEX inventory and final APK SHA-256 verification."]
    if report.get("sample"):
        sample = report["sample"]
        lines.append(f"- Sample: `{sample.get('version_code', '?')}`; APK `{sample.get('sha256', '')[:12]}`; revision `{sample.get('revision', '')}`.")
    if report.get("resume_origin"):
        origin = report["resume_origin"]
        lines.append(f"- Resume: run `{origin['run_id']}`, attempt `{origin['attempt']}`; verified archive `{origin['artifact_id']}`; reused complete tasks `{origin['reused_complete_tasks']}`.")
    lines += ["", "| Task | Status | Rows / total | Reused / fetched | Next offset | Reason |", "| --- | --- | --- | --- | --- | --- |"]
    for task in report.get("tasks", []):
        p = task.get("result", {}).get("pagination", {})
        reason = p.get("stop_reason", task.get("reason", "complete" if task.get("status") == "complete" else task.get("error", "incomplete")))
        # IDs and reason codes are internal bounded identifiers, never SQL or exception bodies.
        reason = re.sub(r"[^A-Za-z0-9_:.-]", "_", str(reason))[:100]
        lines.append(f"| `{task['id']}` | {task['status']} | {p.get('rows', '-')} / {p.get('total_rows', '-')} | {p.get('reused_rows', '-')} / {p.get('fetched_rows', '-')} | {p.get('next_offset', '-')} | `{reason}` |")
    if error:
        code = str(error) if re.fullmatch(r"(?:checkpoint|query|verified_resume)_[a-z_]{1,90}", str(error)) else type(error).__name__
        lines.append(f"\n- Recovery rejected: `{code}`. No completed work is replayed on an invalid checkpoint.")
    lines += ["", "- Evidence: `remote-output/result.txt`, `job.json`, `checkpoint.json`. Partial results remain incomplete; resume uses the original exact sample and work request.", ""]
    with Path(path).open("a", encoding="utf-8") as stream:
        stream.write("\n".join(lines))
