"""Build and verify the pinned MeguvizDexDash CLI binary from its immutable commit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import tempfile

PRODUCT = "MeguvizDexDash"
VERSION = "1.2.2"
SOURCE_REPO = "https://github.com/Meguvizarchic/MeguvizDexDash.git"
SOURCE_COMMIT = "0ecc13aa96514f8517729551a6978390dd9b56b9"
REQUIRED_DIALECT = "dexsql-0.1.0"
ENV_OVERRIDE = "HOSTLAB_MEGUVIZDEXDASH"
PLATFORMS = {
    ("Windows", "AMD64"): (
        "meguvizdexdash.exe",
        "source-sha256:8127c890e2071069b50a619fd87a8a7768732f909d1c559d9aff1d8ecd4ed402",
    ),
    ("Linux", "x86_64"): (
        "meguvizdexdash",
        "source-sha256:b1f590b763871e2ffe7a9080954981cb035cf40f05f2744a5a8d5cfcef782c1c",
    ),
    ("Darwin", "arm64"): (
        "meguvizdexdash",
        "source-sha256:2400df1920e55b8a89c6ce3269fda28623aeed6bb046e6c2fb488b42202f1dd1",
    ),
}
HERE = Path(__file__).resolve().parent


def sha256(path: str | os.PathLike[str]) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def asset() -> tuple[str, str]:
    key = (platform.system(), platform.machine())
    if key not in PLATFORMS:
        raise RuntimeError("unsupported MeguvizDexDash platform: " + "/".join(key))
    return PLATFORMS[key]


def executable() -> Path:
    name, _ = asset()
    override = os.environ.get(ENV_OVERRIDE)
    return Path(override).expanduser().resolve() if override else HERE / "vendor/meguvizdexdash" / VERSION / name


def _run_json(path: Path, *args: str) -> dict:
    try:
        proc = subprocess.run(
            [str(path), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f"MeguvizDexDash `{args[0]}` check failed: {type(exc).__name__}") from None
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        raise RuntimeError(f"MeguvizDexDash `{args[0]}` did not return JSON") from None
    if not isinstance(data, dict):
        raise RuntimeError(f"MeguvizDexDash `{args[0]}` returned unexpected JSON payload")
    return data


def _check_regular_file(path: Path) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        raise RuntimeError("pinned MeguvizDexDash is missing; run install_meguvizdexdash.py") from None
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise RuntimeError("pinned MeguvizDexDash must be a regular non-symlink file")


def inspect(path: str | os.PathLike[str] | None = None) -> dict:
    candidate = Path(path) if path else executable()
    _, expected_build_id = asset()
    _check_regular_file(candidate)
    version = _run_json(candidate, "version")
    if (
        version.get("product") != PRODUCT
        or version.get("engine_version") != VERSION
        or version.get("build_id") != expected_build_id
    ):
        raise RuntimeError(
            "MeguvizDexDash version/build_id mismatch; expected "
            f"{PRODUCT} {VERSION} ({expected_build_id})"
        )
    caps = _run_json(candidate, "capabilities")
    if caps.get("schema_version") != "mdd.capabilities.v1" or caps.get("build_id") != expected_build_id:
        raise RuntimeError("MeguvizDexDash capabilities metadata mismatch")
    dialects = {d.get("name"): d for d in caps.get("sql_dialects", []) if isinstance(d, dict)}
    if REQUIRED_DIALECT not in dialects:
        raise RuntimeError(f"MeguvizDexDash binary lacks required dialect {REQUIRED_DIALECT}")
    features = {c.get("name"): c for c in caps.get("capabilities", []) if isinstance(c, dict)}
    if not (features.get("cli-serve") or {}).get("available"):
        raise RuntimeError("MeguvizDexDash binary lacks cli-serve capability")
    return {
        "engine": "meguvizdexdash",
        "product": PRODUCT,
        "version": VERSION,
        "build_id": expected_build_id,
        "dialect": REQUIRED_DIALECT,
        "sha256": sha256(candidate),
        "path": str(candidate),
    }


def verify(path: str | os.PathLike[str] | None = None) -> Path:
    info = inspect(path)
    return Path(info["path"])


def status(path: str | os.PathLike[str] | None = None) -> dict:
    try:
        return {"available": True, **inspect(path)}
    except (OSError, RuntimeError) as exc:
        return {"available": False, "engine": "meguvizdexdash", "version": VERSION, "reason": str(exc)}


def _build_from_pinned_source(target: Path, binary_name: str) -> None:
    if not shutil.which("git") or not shutil.which("cargo"):
        raise RuntimeError("git and cargo are required to build MeguvizDexDash from pinned source")
    env = {**os.environ, "CARGO_INCREMENTAL": "0", "GIT_TERMINAL_PROMPT": "0"}
    with tempfile.TemporaryDirectory(prefix="mdd-build-") as tmp_dir:
        src = Path(tmp_dir) / "MeguvizDexDash"
        src.mkdir()
        subprocess.run(["git", "init"], cwd=src, env=env, check=True, timeout=30, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", SOURCE_REPO],
            cwd=src,
            env=env,
            check=True,
            timeout=30,
            capture_output=True,
        )
        subprocess.run(
            ["git", "fetch", "--depth", "1", "origin", SOURCE_COMMIT],
            cwd=src,
            env=env,
            check=True,
            timeout=300,
        )
        subprocess.run(
            ["git", "-c", "advice.detachedHead=false", "checkout", "--detach", "FETCH_HEAD"],
            cwd=src,
            env=env,
            check=True,
            timeout=60,
        )
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=src, text=True, timeout=30).strip()
        if head != SOURCE_COMMIT:
            raise RuntimeError(f"checked out commit {head} != pinned {SOURCE_COMMIT}")
        subprocess.run(
            ["cargo", "build", "--release", "--locked", "-p", "mdd-cli"],
            cwd=src,
            env=env,
            check=True,
            timeout=1200,
        )
        built = src / "target" / "release" / binary_name
        if not built.is_file():
            raise RuntimeError(f"built MeguvizDexDash binary missing at {built}")
        with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".staging", delete=False) as stream:
            staged = Path(stream.name)
        try:
            shutil.copyfile(built, staged)
            staged.chmod(0o755)
            info = inspect(staged)
            os.replace(staged, target)
            receipt = target.with_name("BUILD_INFO.json")
            receipt.write_text(
                json.dumps(
                    {
                        "product": PRODUCT,
                        "version": VERSION,
                        "source_repo": SOURCE_REPO,
                        "source_commit": SOURCE_COMMIT,
                        "build_id": info["build_id"],
                        "sha256": info["sha256"],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        finally:
            staged.unlink(missing_ok=True)


def install() -> Path:
    if os.environ.get(ENV_OVERRIDE):
        return verify()  # Explicit override path is never built into or overwritten.
    binary_name, _ = asset()
    target = executable()
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        _build_from_pinned_source(target, binary_name)
    return verify(target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        install()
    info = status()
    print(json.dumps(info, indent=2))
    raise SystemExit(0 if info["available"] else 1)
