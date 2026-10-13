"""Bounded, immutable production evidence from the actual working-tree bytes."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess

SCHEMA = 2
SELECTION_VERSION = 1
MAX_FILES = 2048
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
SOURCE_PREFIX = "Bilibili_Innocent_Lab/app/src/main/java/"
FIXED_PATHS = (
    "Bilibili_Innocent_Lab/gradle.properties",
    "Bilibili_Innocent_Lab/gradle/libs.versions.toml",
    "Bilibili_Innocent_Lab/app/src/main/resources/META-INF/xposed/java_init.list",
    "Bilibili_Innocent_Lab/app/src/main/resources/META-INF/xposed/module.prop",
    "Bilibili_Innocent_Lab/app/src/main/resources/META-INF/xposed/scope.list",
)
PAGES = ("comment", "dynamic", "home", "search", "detail", "pgc", "player", "danmaku", "story", "mine")
MARKERS = re.compile(r"\b(?:Compose|Kotlin|legacy|Legacy|Moss|V2|Theseus|fallback|兜底|新框架|旧框架|多路径)\b")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:(?:RSA|EC|DSA|OPENSSH|ENCRYPTED) )?PRIVATE KEY-----")
CREDENTIAL = re.compile(r"(?<![A-Za-z0-9_])(?:hf_[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{36,}|"
                        r"github_pat_[A-Za-z0-9_]{60,}|sk-[A-Za-z0-9_-]{32,})(?![A-Za-z0-9_])")
ASSIGNMENT = re.compile(r"\b(?!KEY_)[A-Za-z0-9_]*(?:API_KEY|TOKEN|PASSWORD)\s*(?:=|:)\s*"
                        r"[\"']([^\"'\r\n]{24,})[\"']", re.IGNORECASE)
CLAIM = "Frozen working-tree source evidence; not verified installer or runtime coverage"


def _json_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def serialize(ctx):
    """Canonical JSON bytes; source BOM and CRLF characters remain unchanged."""
    return _json_bytes(ctx)


def _placeholder(value):
    value = value.lower().strip()
    for prefix in ("github_pat_", "hf_", "ghp_", "sk-proj-", "sk-"):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    plain = value.replace("_", "").replace("-", "")
    return (bool(plain) and set(plain) <= {"x", "0", "*"}) or value.startswith(
        ("your_", "replace_", "example_", "placeholder_", "dummy_", "test_token_", "test_key_", "test_password_"))


def _secret_gate(path, text):
    reason = None
    if PRIVATE_KEY.search(text):
        reason = "private_key"
    elif any(not _placeholder(match.group()) for match in CREDENTIAL.finditer(text)):
        reason = "credential_token"
    # Preference key constants and interpolated values do not contain fixed credentials.
    elif any(not _placeholder(match.group(1)) and not re.search(r"\$(?:\{|[A-Za-z_])", match.group(1))
             for match in ASSIGNMENT.finditer(text)):
        reason = "credential_assignment"
    if reason:
        raise ValueError("Source secret gate rejected " + path + ": " + reason)


def _scope(path):
    if (not isinstance(path, str) or not path or len(path) > 1024 or "\\" in path or ":" in path or
            any(ord(char) < 32 for char in path)):
        return False
    pure = PurePosixPath(path)
    if pure.is_absolute() or any(p in {"", ".", ".."} for p in path.split("/")):
        return False
    return path in FIXED_PATHS or (path.startswith(SOURCE_PREFIX) and pure.suffix in {".kt", ".java"})


def _tree_identity(head, records):
    manifest = [{k: r[k] for k in ("path", "sha256", "bytes")} for r in records]
    return hashlib.sha256(_json_bytes({"repository_head": head,
        "selection_version": SELECTION_VERSION, "source_records": manifest})).hexdigest()


def _validate(ctx, with_source):
    if not isinstance(ctx, dict) or type(ctx.get("schema")) is not int or ctx["schema"] != SCHEMA:
        raise ValueError("Unsupported source snapshot schema")
    if type(ctx.get("selection_version")) is not int or ctx["selection_version"] != SELECTION_VERSION:
        raise ValueError("Unsupported source selection version")
    head = ctx.get("repository_head")
    if not isinstance(head, str) or not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("Invalid source repository HEAD")
    if type(ctx.get("working_tree_dirty")) is not bool:
        raise ValueError("Invalid source working-tree state")
    captured = ctx.get("captured_at")
    try:
        if not isinstance(captured, str) or not captured.endswith("Z"):
            raise ValueError()
        datetime.fromisoformat(captured[:-1] + "+00:00")
    except ValueError:
        raise ValueError("Invalid UTC source capture time") from None
    records = ctx.get("source_records")
    if not isinstance(records, list) or not 1 <= len(records) <= MAX_FILES:
        raise ValueError("Source snapshot is empty or exceeds file count limit")
    paths = []
    total = 0
    for record in records:
        if not isinstance(record, dict) or not _scope(record.get("path")):
            raise ValueError("Source path is outside the production allowlist")
        paths.append(record["path"])
        size = record.get("bytes")
        sha = record.get("sha256")
        if type(size) is not int or not 0 <= size <= MAX_FILE_BYTES:
            raise ValueError("Source file exceeds byte limit")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
            raise ValueError("Invalid source file SHA-256")
        for name in ("pages", "markers"):
            items = record.get(name)
            if not isinstance(items, list) or len(items) > 32 or any(
                    not isinstance(item, str) or len(item) > 64 for item in items):
                raise ValueError("Invalid source annotations")
            if items != sorted(set(items)) or (name == "pages" and any(item not in PAGES for item in items)):
                raise ValueError("Invalid source annotations")
        if with_source:
            source = record.get("source")
            if not isinstance(source, str):
                raise ValueError("Missing frozen source text")
            if len(source) > MAX_FILE_BYTES:
                raise ValueError("Source file exceeds byte limit")
            try:
                raw = source.encode("utf-8")
            except UnicodeError:
                raise ValueError("Invalid UTF-8 frozen source") from None
            if len(raw) != size or hashlib.sha256(raw).hexdigest() != sha:
                raise ValueError("Frozen source bytes do not match the file manifest")
            _secret_gate(record["path"], source)
        total += size
        if total > MAX_TOTAL_BYTES:
            raise ValueError("Source snapshot exceeds total byte limit")
    if paths != sorted(set(paths)):
        raise ValueError("Source manifest paths must be unique and sorted")
    if not any(path.startswith(SOURCE_PREFIX) for path in paths):
        raise ValueError("Source snapshot has no production source files")
    if ctx.get("source_tree_sha256") != _tree_identity(head, records):
        raise ValueError("Source tree identity does not match the manifest")
    return ctx


def validate(ctx, expected_sha256=None):
    """Validate schema, bounded source bytes and optional canonical payload digest."""
    _validate(ctx, True)
    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
            raise ValueError("Invalid expected source snapshot SHA-256")
        if hashlib.sha256(serialize(ctx)).hexdigest() != expected_sha256:
            raise ValueError("Source snapshot payload SHA-256 mismatch")
    return ctx


def _git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                            check=False, timeout=30)
    if result.returncode:
        raise ValueError("Source root is not an accessible Git working tree")
    return result.stdout


def _head(root):
    head = _git(root, "rev-parse", "HEAD").decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("Invalid source repository HEAD")
    return head


def _linked(path):
    info = path.lstat()
    return (path.is_symlink() or bool(getattr(info, "st_file_attributes", 0) &
                                    getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)))


def _root(root):
    root = Path(root).absolute()
    if _linked(root) or not root.is_dir():
        raise ValueError("Source root must be an ordinary directory")
    return root.resolve(strict=True)


def _checked(root, path):
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if _linked(current):
            raise ValueError("Source links or junctions are not allowed")
    if not path.resolve(strict=True).is_relative_to(root):
        raise ValueError("Source path escapes the repository root")
    return path


def _paths(root):
    source = root / SOURCE_PREFIX
    _checked(root, source)
    if not source.is_dir():
        raise ValueError("Production source directory is unavailable")
    selected = []
    def failed(_error):
        raise ValueError("Production source directory is unreadable")
    for parent, directories, files in os.walk(source, followlinks=False, onerror=failed):
        base = Path(parent)
        for name in directories:
            _checked(root, base / name)
        for name in files:
            path = base / name
            if path.suffix in {".kt", ".java"}:
                selected.append(_checked(root, path))
    if not selected:
        raise ValueError("Production source directory is empty")
    for relative in FIXED_PATHS:
        path = root / relative
        # Missing fixed files remain absent from the complete selected manifest.
        if path.exists() or path.is_symlink():
            selected.append(_checked(root, path))
    selected.sort(key=lambda path: path.relative_to(root).as_posix())
    if len(selected) > MAX_FILES:
        raise ValueError("Source snapshot exceeds file count limit")
    return selected


def _read_records(root):
    records = []
    total = 0
    for path in _paths(root):
        _checked(root, path)
        if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("Source file is unavailable or exceeds byte limit")
        with path.open("rb") as stream:
            raw = stream.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            raise ValueError("Source file exceeds byte limit")
        total += len(raw)
        if total > MAX_TOTAL_BYTES:
            raise ValueError("Source snapshot exceeds total byte limit")
        try:
            text = raw.decode("utf-8")
        except UnicodeError:
            raise ValueError("Production source is not UTF-8") from None
        _secret_gate(path.relative_to(root).as_posix(), text)
        pages = [page for page in PAGES if page in path.name.lower()]
        if "Home" in path.name or "Bottom" in path.name:
            pages += ["home"]
        if "Vertical" in path.name:
            pages += ["story", "detail"]
        if "Interactive" in path.name:
            pages += ["player", "danmaku"]
        records.append({"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(),
                        "bytes": len(raw), "pages": sorted(set(pages)),
                        "markers": sorted(set(MARKERS.findall(text))), "source": text})
    return records


def capture(root, max_attempts=3):
    """Capture two matching reads of the selected files and repository HEAD."""
    if type(max_attempts) is not int or not 1 <= max_attempts <= 10:
        raise ValueError("Source capture attempts must be 1..10")
    root = _root(root)
    for _attempt in range(max_attempts):
        try:
            head = _head(root)
            before = _read_records(root)
            dirty = bool(_git(root, "status", "--porcelain", "-z"))
            after = _read_records(root)
            if head != _head(root) or before != after:
                continue
            ctx = {"schema": SCHEMA, "selection_version": SELECTION_VERSION,
                   "captured_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                   "repository_head": head, "working_tree_dirty": dirty,
                   "source_tree_sha256": _tree_identity(head, before), "source_records": before,
                   "unmapped_multi_path_candidates": [r["path"] for r in before if not r["pages"] and len(r["markers"]) >= 2],
                   "claim": CLAIM}
            return validate(ctx)
        except (FileNotFoundError, PermissionError):
            continue
    raise ValueError("Source working tree changed during bounded capture")


def public_context(ctx, binding=None):
    """Project only approved metadata and file manifests, never source text."""
    _validate(ctx, False)
    if any("source" in record for record in ctx["source_records"]):
        _validate(ctx, True)
    value = {name: ctx[name] for name in ("schema", "selection_version", "captured_at", "repository_head",
                                         "working_tree_dirty", "source_tree_sha256")}
    value["source_records"] = [{name: record[name] for name in ("path", "sha256", "bytes", "pages", "markers")}
                               for record in ctx["source_records"]]
    value["claim"] = CLAIM
    value["unmapped_multi_path_candidates"] = [record["path"] for record in value["source_records"]
        if not record["pages"] and len(record["markers"]) >= 2]
    if binding is not None:
        allowed = ("schema", "repo", "revision", "path", "snapshot_sha256", "source_tree_sha256",
                   "repository_head", "captured_at", "verified_at", "origin", "working_tree_dirty",
                   "file_count", "selection_version")
        value["binding"] = {name: binding[name] for name in allowed if name in binding}
    return value


def compare(manifest, root):
    """Compare a public manifest with local bytes; return no source content."""
    result = {"status": "legacy", "changed": [], "added": [], "removed": []}
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        return result
    try:
        _validate(manifest, False)
        current = capture(root)
    except (OSError, ValueError, subprocess.SubprocessError):
        result["status"] = "unavailable"
        return result
    before = {r["path"]: (r["sha256"], r["bytes"]) for r in manifest["source_records"]}
    after = {r["path"]: (r["sha256"], r["bytes"]) for r in current["source_records"]}
    result.update({"changed": sorted(path for path in before.keys() & after.keys() if before[path] != after[path]),
                   "added": sorted(after.keys() - before.keys()), "removed": sorted(before.keys() - after.keys()),
                   "head_changed": manifest["repository_head"] != current["repository_head"],
                   "source_tree_sha256": current["source_tree_sha256"],
                   "status": "current" if manifest["source_tree_sha256"] == current["source_tree_sha256"] else "drift"})
    return result
