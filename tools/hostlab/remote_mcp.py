"""Local MCP gateway to private GitHub Actions. No APK download on this computer."""
import json
import base64
import os
from pathlib import Path
import re
import subprocess
import uuid
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
import hostlab

REPO = "jichuo1/innocent-lab-host-analysis"
WORKFLOW = "host-analysis.yml"
mcp = MCPServer(name="hostlab-remote", instructions="Run bounded APK analysis in GitHub Actions. For cross-version hook-point or structure investigations use plan_version_matrix/submit_version_matrix, advance its durable queue, then collect version_matrix_result pages. For one sample prefer plan_analysis then submit_analysis: related queries reuse input and prepared backends. Raw SQL keeps its declared sqlite/dexsql dialect. Legacy submit_job stays compatible. Reuse returned IDs; never replay an unknown dispatch. APKs stay on the runner. Static candidates do not establish working runtime hooks.")


def gh(args, payload=None):
    result = subprocess.run([os.environ.get("HOSTLAB_GH", "gh"), *args], input=json.dumps(payload) if payload is not None else None,
                            text=True, encoding="utf-8", capture_output=True, timeout=60)
    if result.returncode:
        raise ToolError("GitHub operation failed; check gh login and private analysis repository access")
    return result.stdout


def runs():
    return json.loads(gh(["api", f"repos/{REPO}/actions/workflows/{WORKFLOW}/runs?per_page=50"]))["workflow_runs"]


def source_freshness(summary):
    """Compare metadata with this caller's working tree without rewriting the historical report."""
    import source_snapshot
    result = source_snapshot.compare(summary.get("source_snapshot"), hostlab.ROOT)
    return result


def repository_report(request_id):
    if not re.fullmatch(r"[0-9a-f]{32}",request_id):
        raise ToolError("Invalid request ID")
    try:
        payload=json.loads(gh(["api",f"repos/{REPO}/contents/index.json?ref=reports"]))
        index=json.loads(base64.b64decode(payload["content"]))
    except Exception:
        return None
    rows=[r for r in index.get("reports",[]) if r.get("request_id")==request_id]
    if not rows:
        return None
    entry=max(rows,key=lambda r:r["created_at"])
    path=entry["path"]
    if not re.fullmatch(r"(?:samples/[0-9]+/[0-9a-f]{64}/runs|failures)/[0-9]+-a[0-9]+/report\.md",path):
        raise ToolError("Unexpected report path")
    out=hostlab.STATE/"remote-results"/entry["report_id"]/"repository"
    out.mkdir(parents=True,exist_ok=True)
    files=[]
    texts=[]
    for suffix in ("report.md","summary.json"):
        file_path=path.rsplit("/",1)[0]+"/"+suffix
        try:
            blob=json.loads(gh(["api",f"repos/{REPO}/contents/{file_path}?ref=reports"]))
            raw=base64.b64decode(blob["content"])
        except Exception:
            continue
        target=out/suffix
        target.write_bytes(raw)
        files.append(str(target))
        texts.append(raw.decode("utf-8",errors="replace")[:16000])
    summary_file = out / "summary.json"
    freshness = source_freshness(json.loads(summary_file.read_text(encoding="utf-8"))) if summary_file.exists() else {"status": "unavailable"}
    return {"report_url":f"https://github.com/{REPO}/blob/reports/{path}","release_url":entry.get("release_url"),
            "files":files,"text":"\n".join(texts)[:24000],"source":"durable_reports_branch", "source_freshness": freshness}


def lookup(request_id):
    if not re.fullmatch(r"[0-9a-f]{32}", request_id):
        raise ToolError("Invalid request ID")
    mapping = hostlab.STATE / "remote-job-map" / (request_id + ".json")
    if mapping.exists():
        run_id = int(json.loads(mapping.read_text(encoding="utf-8"))["run_id"])
        return json.loads(gh(["api", f"repos/{REPO}/actions/runs/{run_id}"]))
    run = next((r for r in runs() if r["display_title"] == "hostlab-" + request_id), None)
    if run is not None:
        hostlab.write_json(mapping, {"run_id": run["id"]})
    return run


@mcp.tool()
def plan_version_matrix(samples: list[dict], request: dict, max_parallel: int = 4,
                        reuse_completed: bool = True, deadline_seconds: int = 1800) -> str:
    """Plan the same feature investigation over 1..40 exact APKs. Each sample needs version_code, apk_sha256 and sample_revision from inventory.json. One immutable tool commit binds the whole matrix; max_parallel is 1..4. Set reuse_completed=false for a fresh load test. No Actions dispatch here."""
    import version_matrix
    try:
        return json.dumps(version_matrix.plan(samples,request,max_parallel,reuse_completed,deadline_seconds),ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool()
def submit_version_matrix(samples: list[dict], request: dict, max_parallel: int = 4,
                          reuse_completed: bool = True, deadline_seconds: int = 1800,
                          idempotency_key: str = "") -> str:
    """Create a durable multi-version queue and dispatch at most two initial batches. Inventory pins are mandatory. Use advance_version_matrix repeatedly to fill/replenish up to 4 slots; queued_local entries are retained under capacity pressure. No background execution occurs after the call. An explicit key resumes the same matrix. Unknown dispatches and paid failures are never replayed automatically."""
    import version_matrix
    try:
        created=version_matrix.create(samples,request,gh,repository=REPO,max_parallel=max_parallel,
            reuse_completed=reuse_completed,deadline_seconds=deadline_seconds,idempotency_key=idempotency_key)
        if "matrix_id" not in created:
            return json.dumps(created)
        return json.dumps(version_matrix.advance(created["matrix_id"],gh,lookup,runs,repository=REPO,workflow=WORKFLOW),ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool()
def advance_version_matrix(matrix_id: str) -> str:
    """Refresh accepted jobs and dispatch at most two queued versions under the captured tool revision and 1..4-slot budget. Call only while you intend the matrix to progress. capacity_full leaves versions queued, never lost; a deadline stops new dispatches without cancelling accepted work."""
    import version_matrix
    try:
        return json.dumps(version_matrix.advance(matrix_id,gh,lookup,runs,repository=REPO,workflow=WORKFLOW),ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool()
def version_matrix_status(matrix_id: str) -> str:
    """Refresh matrix job states without submitting additional work."""
    import version_matrix
    try:
        return json.dumps(version_matrix.advance(matrix_id,gh,lookup,runs,repository=REPO,workflow=WORKFLOW,dispatch=False),ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool()
def version_matrix_result(matrix_id: str, offset: int = 0, limit: int = 8, download_parallel: int = 4) -> str:
    """Collect a finished matrix with 1..4 download workers and a verified artifact cache. Partial collection reports collection_errors: retry this same matrix/page without new Actions. Candidate identities and structure hashes preserve exact sample/tool bindings. Large previews point to an immutable local comparison snapshot. Static results do not prove working runtime hooks."""
    import version_matrix
    try:
        return json.dumps(version_matrix.compare(matrix_id,job_result,offset,limit,
            download_parallel=download_parallel,collect=matrix_artifact),ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


def matrix_artifact(entry):
    """Use the matrix's completed run snapshot; old matrices resolve it once per cache access."""
    import remote_artifacts
    run = entry.get("result_run")
    if not run or not {"head_sha", "display_title", "run_attempt"} <= run.keys():
        run = lookup(entry["request_id"])
    if run is None:
        raise remote_artifacts.ArtifactError("result_run_unavailable")
    return json.dumps(remote_artifacts.get(REPO, entry["request_id"], run, gh), ensure_ascii=False)


@mcp.tool()
def plan_analysis(request: dict) -> str:
    """Plan up to 16 related tasks without dispatching. Request: {backend:auto|sqlite|dexsql,tasks:[{id,operation,...}]}. query requires sql and dialect; locate requires kind/name; refs requires kind/target and methods|sites detail; decode requires a full method descriptor; info reads Manifest. Auto preserves raw SQL dialect and reference-site semantics, prefers native references, and reuses warm SQLite structure indexes on the runner. This is a plan, not execution evidence."""
    import remote_schedule
    try:
        return json.dumps(remote_schedule.describe(request), ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool()
def submit_analysis(version_code: int, request: dict, apk_sha256: str = "", sample_revision: str = "",
                    idempotency_key: str = "") -> str:
    """Schedule one bounded analysis batch. Related tasks share one APK fetch and one session per backend. Optional APK SHA and immutable sample revision must be supplied together and enable completed-result reuse for deterministic semantic tasks for 24h. Arbitrary SQL is not cached after completion. Equal active submissions are reused. An idempotency key explicitly binds retries, including failures. Unknown dispatch is never replayed: use returned request_id with job_status/job_result. capacity_full/scheduler_busy do not dispatch. Uses Actions minutes."""
    import remote_schedule
    try:
        result = remote_schedule.submit(version_code, request, gh, lookup, runs, repository=REPO,
                                        workflow=WORKFLOW, apk_sha256=apk_sha256,
                                        sample_revision=sample_revision, idempotency_key=idempotency_key)
        return json.dumps(result, ensure_ascii=False)
    except ValueError as exc:
        raise ToolError(str(exc)) from None


@mcp.tool()
def submit_job(version_code: int, operation: str, argument: str = "", max_cell_chars: int = 300,
               source_mode: str = "auto") -> str:
    """Submit multipath_audit, audit, decompile (class), query (SELECT SQL), decode (method), string_refs (string), or info. Uses Actions minutes; returns immediately.

    query supports max_cell_chars=1..16000 (default 300). Larger cells remain in the index;
    use length()/substr() with file_id and a stable row key for longer values.
    """
    if version_code <= 0 or version_code > 9999999999 or operation not in {"inventory", "audit", "decompile", "query", "decode", "string_refs", "info", "multipath_audit", "regenerate_ai", "source_check"} or len(argument) > 4096:
        raise ToolError("Invalid bounded operation parameters")
    if not 1 <= max_cell_chars <= 16000 or (operation != "query" and max_cell_chars != 300):
        raise ToolError("max_cell_chars must be 1..16000 and only varies for query")
    if source_mode not in {"auto", "worktree", "published", "historical"}:
        raise ToolError("Unsupported source_mode")
    if source_mode != "auto" and operation not in {"multipath_audit", "regenerate_ai", "source_check"}:
        raise ToolError("source_mode applies only to complete analysis")
    if operation in {"multipath_audit", "source_check"} and source_mode == "historical":
        raise ToolError("New analysis cannot silently use historical source")
    request = uuid.uuid4().hex
    inputs = {"request_id": request, "version_code": str(version_code),
              "operation": operation, "argument": argument}
    # Omit the default so an older workflow can still serve legacy clients.
    if max_cell_chars != 300:
        inputs["max_cell_chars"] = str(max_cell_chars)
    binding = None
    if operation in {"multipath_audit", "source_check"} or operation == "regenerate_ai" and source_mode not in {"auto", "historical"}:
        import snapshot_transport
        try:
            binding = snapshot_transport.prepare(hostlab.ROOT, gh, mode=source_mode)
        except Exception:
            raise ToolError("Source snapshot preparation failed; analysis was not dispatched") from None
        inputs["module_source"] = json.dumps(binding, separators=(",", ":"), sort_keys=True)
    hostlab.write_json(hostlab.STATE / "remote-requests" / (request + ".json"), {
        "request_id": request, "version_code": version_code, "operation": operation,
        "source_mode": source_mode, "module_source": binding})
    gh(["api", "--method", "POST", f"repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches", "--input", "-"],
       {"ref": "main", "inputs": inputs})
    return json.dumps({"request_id": request, "status": "submitted", "repository": REPO,
                       "module_source": binding})


@mcp.tool()
def job_status(request_id: str) -> str:
    """Get queue/running/completion state for a submitted request. Does not wait."""
    run = lookup(request_id)
    if run is None:
        return json.dumps({"status": "dispatch_pending", "request_id": request_id})
    import remote_schedule
    remote_schedule.observe(request_id, run)
    return json.dumps({k: run[k] for k in ("id", "status", "conclusion", "html_url", "head_sha")})


@mcp.tool()
def list_jobs() -> str:
    """List the latest ten analysis runs."""
    return json.dumps([{k: r[k] for k in ("id", "display_title", "status", "conclusion", "html_url")} for r in runs()[:10]])


@mcp.tool()
def job_result(request_id: str, result_offset: int = 0) -> str:
    """Download result artifacts and return bounded text plus local file paths. No APK or DEX.

    result.txt is paged in 8000-character chunks (Unicode characters, zero-based offset).
    Pass result_page.next_offset back as result_offset until it is null. Reading pages
    reuses the downloaded artifact; it does not submit another Actions analysis job.
    """
    if not 0 <= result_offset <= 2147483647:
        raise ToolError("result_offset must be 0..2147483647")
    durable=repository_report(request_id)
    if durable:
        if result_offset:
            raise ToolError("result_offset applies only to result.txt; use the returned report files")
        return json.dumps(durable,ensure_ascii=False)
    run = lookup(request_id)
    if run is None or run["status"] != "completed":
        raise ToolError("Job has not completed")
    import remote_artifacts
    try:
        collected = remote_artifacts.get(REPO, request_id, run, gh)
    except (ValueError, OSError) as exc:
        raise ToolError(str(exc) if isinstance(exc, remote_artifacts.ArtifactError) else "artifact_collection_failed") from None
    files = sorted((Path(p) for p in collected["files"]),
                   key=lambda p: (p.name != "result.txt", str(p)))
    out = Path(collected["root"])
    if sum(p.name == "result.txt" for p in files) > 1:
        raise ToolError("Multiple result.txt files; cannot choose an unambiguous page source")
    text = []
    result_page = None
    preview_truncated = False
    for p in files:
        if p.name in {"inventory.json", "job.json", "result.txt", "summary.json", "class.java", "priority-report.md"}:
            content = p.read_text(encoding="utf-8", errors="replace")
            if p.name == "result.txt":
                page = content[result_offset:result_offset + 8000]
                end = min(result_offset + len(page), len(content))
                result_page = {"file": str(p.relative_to(out)), "offset": result_offset,
                               "chars": len(page), "total_chars": len(content),
                               "next_offset": end if end < len(content) else None}
                preview_truncated |= end < len(content)
            else:
                page = content[:8000]
                preview_truncated |= len(content) > 8000
            text.append(str(p.relative_to(out)) + "\n" + page)
    if result_offset and result_page is None:
        raise ToolError("No result.txt to page; use the returned report files at offset 0")
    combined = "\n".join(text)
    preview_truncated |= len(combined) > 24000
    summaries = [p for p in files if p.name == "priority-summary.json"]
    freshness = source_freshness(json.loads(summaries[0].read_text(encoding="utf-8"))) if len(summaries) == 1 else None
    return json.dumps({"run": run["html_url"], "files": [str(p) for p in files],
                       "text": combined[:24000], "text_truncated": preview_truncated,
                       "result_page": result_page, "source_freshness": freshness,
                       "collection": {key:collected[key] for key in ("cache_hit", "artifact", "integrity", "elapsed_ms", "run_attempt")}}, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
