"""Cloud-only poll: new samples trigger pinned multi-path analysis and bounded AI review."""
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
import urllib.error
import urllib.request
import hostlab
import snapshot_transport

REPO = "jichuo1/innocent-lab-host-analysis"
STATE_PATH = ".hostlab/intake-state.json"
BRANCH = "intake-state"


def api(path, data=None, method=None):
    request = urllib.request.Request("https://api.github.com/repos/" + REPO + "/" + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json", "X-GitHub-Api-Version": "2022-11-28"},
        method=method or ("POST" if data is not None else "GET"))
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        return json.loads(body) if body else None


def choose_new(state, rows):
    seen = set(state.get("seen", []))
    fresh = [r for r in rows if r["sha256"] not in seen]
    eligible = sorted(fresh, key=lambda r:(r["version_code"], r["sha256"]))
    return fresh, eligible


def main():
    repo = "innocent-lab-dev/bilibili-host-apks"
    _, revision = hostlab.api_private(repo)
    rows = hostlab.manifest(repo, revision)["samples"]
    try:
        file = api("contents/" + STATE_PATH + "?ref=" + BRANCH)
        state = json.loads(base64.b64decode(file["content"]))
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        head = api("git/ref/heads/main")["object"]["sha"]
        try:
            api("git/refs", {"ref": "refs/heads/" + BRANCH, "sha": head})
        except urllib.error.HTTPError as create_error:
            if create_error.code != 422:
                raise
        from pathlib import Path
        bootstrap_path = Path(__file__).with_name("bootstrap-samples.json")
        bootstrap = json.loads(bootstrap_path.read_text(encoding="utf-8")) if bootstrap_path.exists() else []
        state = {"schema": 1, "seen": sorted(set([r["sha256"] for r in rows] + bootstrap)),
                 "watermark": max((r["version_code"] for r in rows), default=0), "jobs": {},
                 "mode": "static_plus_bounded_ai_review", "initialized_revision": revision}
        file = None
    old_state = json.dumps(state, sort_keys=True)
    fresh, eligible = choose_new(state, rows)
    # This cloud poller can see only the published source, never the caller's worktree.
    module_source = snapshot_transport.resolve_published() if eligible else None
    existing_runs = api("actions/workflows/host-analysis.yml/runs?per_page=100")["workflow_runs"]
    for key, job in state["jobs"].items():
        run = next((r for r in existing_runs if r["display_title"] == "hostlab-" + key), None)
        if run:
            job.update({"run_id": run["id"], "status": run["status"], "conclusion": run["conclusion"], "url": run["html_url"]})
    dispatched = []
    for row in sorted(eligible, key=lambda r:r["version_code"])[:2]:
        key = hashlib.sha256((row["sha256"] + ":multipath-ai-v1").encode()).hexdigest()[:32]
        # Deterministic title also closes the dispatch-success/state-write-failure window.
        existing = next((r for r in existing_runs if r["display_title"] == "hostlab-" + key), None)
        if key not in state["jobs"] and existing:
            state["jobs"][key] = {"sample": row["sha256"], "version_code": row["version_code"],
                                  "run_id": existing["id"], "status": existing["status"], "conclusion": existing["conclusion"]}
        if key not in state["jobs"] and existing is None:
            bases = [r for r in rows if r["version_code"] < row["version_code"] and
                     r.get("certificate_sha256") == row.get("certificate_sha256")]
            baseline = max(bases, key=lambda r:r["version_code"])["sha256"] if bases else ""
            api("actions/workflows/host-analysis.yml/dispatches", {"ref": "main", "inputs": {
                "request_id": key, "version_code": str(row["version_code"]), "operation": "multipath_audit",
                "source_revision": revision, "apk_sha256": row["sha256"], "baseline_sha256": baseline,
                "module_source": json.dumps(module_source, separators=(",", ":"))}})
            state["jobs"][key] = {"sample": row["sha256"], "version_code": row["version_code"], "status": "submitted",
                                  "module_source": module_source, "source_freshness": "published_unverified_worktree"}
            dispatched.append(row["version_code"])
        state["seen"].append(row["sha256"])
    deferred = {r["sha256"] for r in eligible[2:]}
    state["seen"] = sorted(set(state["seen"]) | {r["sha256"] for r in fresh if r["sha256"] not in deferred and r not in eligible})
    if eligible:
        state["watermark"] = max(state["watermark"], max(r["version_code"] for r in eligible[:2]))
    state["mode"] = "static_plus_bounded_ai_review"
    state["source_freshness"] = "published_unverified_worktree"
    if module_source is not None:
        state["module_source"] = module_source
    if file is None or json.dumps(state, sort_keys=True) != old_state:
        payload = {"message": "chore(intake): update sample analysis state", "branch": BRANCH,
                   "content": base64.b64encode(json.dumps(state, indent=2).encode()).decode()}
        if file:
            payload["sha"] = file["sha"]
        api("contents/" + STATE_PATH, payload, method="PUT")
    print(json.dumps({"published": len(rows), "dispatched": dispatched, "ai": "enabled_for_new_reports"}))


if __name__ == "__main__":
    main()
