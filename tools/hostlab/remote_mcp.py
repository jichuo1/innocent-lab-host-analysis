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
mcp = MCPServer(name="hostlab-remote", instructions="Run APK analysis in private GitHub Actions. Submit returns a request ID; check status later, then retrieve results. APKs stay on the runner. Full multi-path reports include AI suggestions and durable reports-branch links; none establish runtime acceptance.")


def gh(args, payload=None):
    result = subprocess.run([os.environ.get("HOSTLAB_GH", "gh"), *args], input=json.dumps(payload) if payload is not None else None,
                            text=True, encoding="utf-8", capture_output=True, timeout=60)
    if result.returncode:
        raise ToolError("GitHub operation failed; check gh login and private analysis repository access")
    return result.stdout


def runs():
    return json.loads(gh(["api", f"repos/{REPO}/actions/workflows/{WORKFLOW}/runs?per_page=50"]))["workflow_runs"]


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
    return {"report_url":f"https://github.com/{REPO}/blob/reports/{path}","release_url":entry.get("release_url"),
            "files":files,"text":"\n".join(texts)[:24000],"source":"durable_reports_branch"}


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
def submit_job(version_code: int, operation: str, argument: str = "") -> str:
    """Submit multipath_audit (all registered pages, pinned prior baseline), audit, decompile (class), query (SELECT SQL), decode (method), string_refs (string), or info. Uses Actions minutes; returns immediately."""
    if version_code <= 0 or version_code > 9999999999 or operation not in {"inventory", "audit", "decompile", "query", "decode", "string_refs", "info", "multipath_audit", "regenerate_ai"} or len(argument) > 4096:
        raise ToolError("Invalid bounded operation parameters")
    request = uuid.uuid4().hex
    gh(["api", "--method", "POST", f"repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches", "--input", "-"],
       {"ref": "main", "inputs": {"request_id": request, "version_code": str(version_code),
                                    "operation": operation, "argument": argument}})
    return json.dumps({"request_id": request, "status": "submitted", "repository": REPO})


@mcp.tool()
def job_status(request_id: str) -> str:
    """Get queue/running/completion state for a submitted request. Does not wait."""
    run = lookup(request_id)
    if run is None:
        return json.dumps({"status": "dispatch_pending", "request_id": request_id})
    return json.dumps({k: run[k] for k in ("id", "status", "conclusion", "html_url", "head_sha")})


@mcp.tool()
def list_jobs() -> str:
    """List the latest ten analysis runs."""
    return json.dumps([{k: r[k] for k in ("id", "display_title", "status", "conclusion", "html_url")} for r in runs()[:10]])


@mcp.tool()
def job_result(request_id: str) -> str:
    """Download only result artifacts and return bounded text plus local file paths. No APK or DEX."""
    durable=repository_report(request_id)
    if durable:
        return json.dumps(durable,ensure_ascii=False)
    run = lookup(request_id)
    if run is None or run["status"] != "completed":
        raise ToolError("Job has not completed")
    out = hostlab.STATE / "remote-results" / str(run["id"])
    if not (out / ".downloaded").exists():
        out.mkdir(parents=True, exist_ok=True)
        try:
            gh(["run", "download", str(run["id"]), "--repo", REPO, "--name", "host-analysis-" + str(run["id"]), "--dir", str(out)])
            (out / ".downloaded").touch()
        except Exception:
            raise ToolError("Results unavailable; check workflow logs or expired artifact")
    files = [p for p in out.rglob("*") if p.is_file() and p.name != ".downloaded"]
    text = []
    for p in files:
        if p.name in {"inventory.json", "job.json", "result.txt", "summary.json", "class.java", "priority-report.md"}:
            text.append(str(p.relative_to(out)) + "\n" + p.read_text(encoding="utf-8", errors="replace")[:8000])
    return json.dumps({"run": run["html_url"], "files": [str(p) for p in files], "text": "\n".join(text)[:24000]}, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
