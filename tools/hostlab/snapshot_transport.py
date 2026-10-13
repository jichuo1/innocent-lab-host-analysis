"""Private immutable source payloads; public GitHub state contains metadata only."""
import base64
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import subprocess
import os
import tempfile

import hostlab
import source_snapshot

SOURCE_REPO = "innocent-lab-dev/bilibili-host-apks"
ANALYSIS_REPO = "jichuo1/innocent-lab-host-analysis"
POINTER_BRANCH = "source-state"
POINTER_PATH = ".hostlab/source-snapshot-latest.json"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def _gh(args, payload=None):
    process = subprocess.run([os.environ.get("HOSTLAB_GH", "gh"), *args],
        input=json.dumps(payload) if payload is not None else None,
        text=True, encoding="utf-8", capture_output=True, timeout=60)
    if process.returncode:
        raise RuntimeError("Source metadata GitHub operation failed")
    return process.stdout


def _api(path, gh=None, payload=None):
    args = ["api", f"repos/{ANALYSIS_REPO}/{path}"]
    if payload is not None:
        args += ["--method", "POST", "--input", "-"]
    text = (gh or _gh)(args, payload)
    return json.loads(text) if text.strip() else None


def checked_binding(value):
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise RuntimeError("Unsupported module source binding")
    sha = value.get("snapshot_sha256", "")
    if not isinstance(sha, str) or not HEX64.fullmatch(sha):
        raise RuntimeError("Invalid source payload hash")
    if not isinstance(value.get("revision"), str) or not HEX40.fullmatch(value["revision"]):
        raise RuntimeError("Source revision must be immutable")
    if value.get("repo") != SOURCE_REPO or value.get("path") != f"source-snapshots/{sha}/context.json":
        raise RuntimeError("Invalid private source location")
    if not HEX64.fullmatch(value.get("source_tree_sha256", "")) or not HEX40.fullmatch(value.get("repository_head", "")):
        raise RuntimeError("Invalid source tree identity")
    if value.get("origin") not in {"worktree", "published", "published_job_start"}:
        raise RuntimeError("Invalid source origin")
    for key in ("captured_at", "verified_at"):
        try:
            timestamp = datetime.fromisoformat(value[key].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                raise ValueError()
        except (KeyError, TypeError, ValueError):
            raise RuntimeError("Invalid source timestamp") from None
    # Only allowlisted metadata travels through workflow_dispatch or public state.
    keys = ("schema", "repo", "revision", "path", "snapshot_sha256", "source_tree_sha256",
            "repository_head", "captured_at", "verified_at", "origin", "working_tree_dirty",
            "file_count", "selection_version")
    return {key: value[key] for key in keys if key in value}


def cache_snapshot(ctx, binding):
    binding = checked_binding(binding)
    source_snapshot.validate(ctx, binding["snapshot_sha256"])
    if ctx["source_tree_sha256"] != binding["source_tree_sha256"] or ctx["repository_head"] != binding["repository_head"]:
        raise RuntimeError("Source payload and binding disagree")
    if ctx["captured_at"] != binding["captured_at"]:
        raise RuntimeError("Source capture timestamp mismatch")
    path = hostlab.STATE / "source-snapshots" / binding["snapshot_sha256"] / "context.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".context-", suffix=".tmp", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(source_snapshot.serialize(ctx))
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def load_pinned(binding, *, force_remote=False):
    binding = checked_binding(binding)
    cached = hostlab.STATE / "source-snapshots" / binding["snapshot_sha256"] / "context.json"
    if cached.exists() and not force_remote:
        ctx = json.loads(cached.read_text(encoding="utf-8"))
        source_snapshot.validate(ctx, binding["snapshot_sha256"])
        cache_snapshot(ctx, binding)
        return ctx
    hostlab.api_private(SOURCE_REPO)
    from huggingface_hub import hf_hub_download
    try:
        fetched = hf_hub_download(repo_id=SOURCE_REPO, repo_type="dataset", filename=binding["path"],
            revision=binding["revision"], token=True)
        ctx = json.loads(Path(fetched).read_text(encoding="utf-8"))
    except Exception:
        raise RuntimeError("Pinned private source snapshot unavailable") from None
    cache_snapshot(ctx, binding)
    return ctx


def resolve_published(gh=None):
    # Pin the pointer commit before reading it; never read a moving branch twice.
    commit = _api(f"git/ref/heads/{POINTER_BRANCH}", gh)["object"]["sha"]
    if not HEX40.fullmatch(commit):
        raise RuntimeError("Invalid published source metadata revision")
    blob = _api(f"contents/{POINTER_PATH}?ref={commit}", gh)
    binding = checked_binding(json.loads(base64.b64decode(blob["content"])))
    binding["origin"] = "published"
    return binding


def _publish_pointer(binding, gh=None):
    try:
        _api(f"git/ref/heads/{POINTER_BRANCH}", gh)
    except Exception:
        head = _api("git/ref/heads/main", gh)["object"]["sha"]
        try:
            _api("git/refs", gh, {"ref": f"refs/heads/{POINTER_BRANCH}", "sha": head})
        except Exception:
            _api(f"git/ref/heads/{POINTER_BRANCH}", gh)  # Concurrent creation may have won.
    for attempt in range(3):
        previous = None
        try:
            previous = _api(f"contents/{POINTER_PATH}?ref={POINTER_BRANCH}", gh)
        except Exception:
            pass
        if previous:
            current = checked_binding(json.loads(base64.b64decode(previous["content"])))
            if datetime.fromisoformat(current["verified_at"]) > datetime.fromisoformat(binding["verified_at"]):
                return  # A delayed publisher must not move latest behind a newer capture.
        payload = {"branch": POINTER_BRANCH,
            "message": f"chore(snapshot): record source {binding['source_tree_sha256'][:12]}",
            "content": base64.b64encode(source_snapshot.serialize(binding)).decode("ascii")}
        if previous:
            payload["sha"] = previous["sha"]
        args = ["api", "--method", "PUT", f"repos/{ANALYSIS_REPO}/contents/{POINTER_PATH}", "--input", "-"]
        try:
            (gh or _gh)(args, payload)
            published = _api(f"contents/{POINTER_PATH}?ref={POINTER_BRANCH}", gh)
            actual = checked_binding(json.loads(base64.b64decode(published["content"])))
            # Newer concurrent publication is acceptable; our request still pins its own private revision.
            if actual["snapshot_sha256"] != binding["snapshot_sha256"] and datetime.fromisoformat(actual["verified_at"]) <= datetime.fromisoformat(binding["verified_at"]):
                raise RuntimeError("Source metadata readback mismatch")
            return
        except Exception:
            if attempt == 2:
                raise RuntimeError("Source metadata publication failed") from None


def publish(ctx, gh=None):
    source_snapshot.validate(ctx)
    raw = source_snapshot.serialize(ctx)
    sha = hashlib.sha256(raw).hexdigest()
    path = f"source-snapshots/{sha}/context.json"
    api, head = hostlab.api_private(SOURCE_REPO)
    from huggingface_hub import CommitOperationAdd
    try:
        committed = api.create_commit(repo_id=SOURCE_REPO, repo_type="dataset", parent_commit=head,
            commit_message=f"Publish immutable module source {ctx['source_tree_sha256'][:12]}",
            operations=[CommitOperationAdd(path_in_repo=path, path_or_fileobj=raw)])
        revision = committed.oid
    except Exception:
        raise RuntimeError("Private source snapshot upload failed") from None
    binding = checked_binding({"schema": 1, "repo": SOURCE_REPO, "revision": revision, "path": path,
        "snapshot_sha256": sha, "source_tree_sha256": ctx["source_tree_sha256"],
        "repository_head": ctx["repository_head"], "captured_at": ctx["captured_at"],
        "verified_at": datetime.now(timezone.utc).isoformat(), "origin": "worktree",
        "working_tree_dirty": ctx["working_tree_dirty"], "file_count": len(ctx["source_records"]),
        "selection_version": ctx["selection_version"]})
    # Read the just-created immutable remote payload before publishing metadata or dispatching.
    downloaded = load_pinned(binding, force_remote=True)
    if source_snapshot.serialize(downloaded) != raw:
        raise RuntimeError("Private source payload readback mismatch")
    _publish_pointer(binding, gh)
    return binding


def prepare(root, gh=None, mode="auto"):
    root = Path(root)
    if mode == "published":
        return resolve_published(gh)
    if mode not in {"auto", "worktree"}:
        raise RuntimeError("Unsupported source mode")
    if (root / "Bilibili_Innocent_Lab/app/src/main/java").is_dir():
        ctx = source_snapshot.capture(root)
        binding = publish(ctx, gh)
        if source_snapshot.compare(source_snapshot.public_context(ctx), root)["status"] != "current":
            raise RuntimeError("Working tree changed before analysis dispatch; capture again")
        return binding
    if mode == "worktree":
        raise RuntimeError("Production working tree unavailable")
    return resolve_published(gh)


def load_for_analysis(binding_json=None):
    if binding_json:
        if len(binding_json) > 4096:
            raise RuntimeError("Module source binding too large")
        binding = checked_binding(json.loads(binding_json))
    else:
        binding = resolve_published()
        binding["origin"] = "published_job_start"
    return load_pinned(binding), binding
