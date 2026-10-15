"""Prepare a verified dependency-only venv. Never cache sample data or credentials."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import stat
import subprocess
import sys
import sysconfig
import time
import uuid
import venv

import hostlab
import remote_schedule

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAX_FILES = 30000
MAX_BYTES = 1024 * 1024 * 1024
POLICY = 1


def describe(requirements):
    if requirements not in {"requirements.txt", "requirements-query.txt"}:
        raise ValueError("unsupported runtime dependency subset")
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    identity = {"policy": POLICY, "requirements": requirements,
        "requirements_sha256": hostlab.digest(HERE / requirements), "bootstrap_sha256": hostlab.digest(Path(__file__)),
        "python": sys.version, "abi": sysconfig.get_config_var("SOABI"), "cache_tag": sys.implementation.cache_tag,
        "platform": platform.system(), "machine": platform.machine(), "image": os.environ.get("ImageOS", ""),
        "image_version": os.environ.get("ImageVersion", ""), "base_python": str(base), "base_sha256": hostlab.digest(base),
        "workspace": str(ROOT.resolve())}
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    return identity, fingerprint


def directory():
    return ROOT / "runtime/hostlab-prepared"


def interpreter(root):
    return root / "env" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def is_link(path):
    try:
        info = path.lstat()
        return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)
    except FileNotFoundError:
        return False


def controlled_root(root):
    expected = ROOT.absolute() / "runtime/hostlab-prepared"
    if root.absolute() != expected or root == ROOT or not root.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("runtime cache must stay in its dedicated workspace directory")
    for candidate in (ROOT / "runtime", root):
        if is_link(candidate):
            raise ValueError("linked runtime cache directory")


def inventory(root, base):
    rows = []; total = 0
    if any(p.name not in {"env", "receipt.json"} for p in root.iterdir()):
        raise ValueError("unexpected file outside the dependency environment")
    if not (root / "env").is_dir() or is_link(root / "env"):
        raise ValueError("missing or linked runtime environment")
    for parent, dirs, files in os.walk(root / "env", followlinks=False):
        for name in dirs:
            path = Path(parent) / name
            if is_link(path):
                if path != root / "env/lib64" or path.resolve() != (root / "env/lib").resolve():
                    raise ValueError("linked runtime package directory")
                rows.append({"path":path.relative_to(root).as_posix(),"link":os.readlink(path)})
            else:
                rows.append({"path":path.relative_to(root).as_posix(),"directory":True})
            if len(rows)>MAX_FILES:
                raise ValueError("prepared runtime exceeds its file/size budget")
        for name in files:
            path = Path(parent) / name
            relative = path.relative_to(root).as_posix()
            if is_link(path):
                if path.parent.name != "bin" or not re.fullmatch(r"python(?:3(?:\.\d+)?)?", name) or path.resolve() != base:
                    raise ValueError("unexpected link in prepared runtime")
                rows.append({"path": relative, "link": os.readlink(path)})
            else:
                if not stat.S_ISREG(path.stat().st_mode):
                    raise ValueError("nonregular runtime package file")
                size = path.stat().st_size; total += size
                rows.append({"path": relative, "bytes": size, "sha256": hostlab.digest(path)})
            if len(rows) > MAX_FILES or total > MAX_BYTES:
                raise ValueError("prepared runtime exceeds its file/size budget")
    if not rows:
        raise ValueError("empty prepared runtime")
    return sorted(rows, key=lambda row: row["path"])


def probe(root, requirements):
    expected = []
    for line in (HERE / requirements).read_text(encoding="utf-8").splitlines():
        if line.strip():
            name, version = line.strip().split("==")
            expected.append((name, version))
    script = """import importlib.metadata as m,json,sys
from pathlib import Path
root,expected=json.loads(sys.argv[1])
assert Path(sys.prefix).resolve()==Path(root).resolve()
for name,version in expected: assert m.version(name)==version
import huggingface_hub,mcp
if any(name=='androguard' for name,_ in expected): import androguard
print(json.dumps(sorted((d.metadata['Name'],d.version) for d in m.distributions())))
"""
    result = subprocess.run([str(interpreter(root)), "-I", "-B", "-c", script,
        json.dumps([str(root / "env"), expected])], capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    return json.loads(result.stdout)


def verify(root, identity, fingerprint):
    controlled_root(root)
    try:
        receipt = root / "receipt.json"
        if not receipt.is_file() or is_link(receipt) or receipt.stat().st_size > 8 * 1024 * 1024:
            return False
        saved = json.loads(receipt.read_text(encoding="utf-8"))
        if not isinstance(saved, dict) or saved.get("schema") != POLICY or saved.get("identity") != identity or saved.get("fingerprint") != fingerprint:
            return False
        observed = inventory(root, Path(identity["base_python"]))
        if observed != saved["files"]:
            return False
        # Only execute the cached interpreter after the complete file/link inventory passed.
        return probe(root, identity["requirements"]) == saved["distributions"]
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        return False


def build(root, identity, fingerprint):
    controlled_root(root)
    root.mkdir(parents=True, exist_ok=False)
    venv.EnvBuilder(with_pip=False, symlinks=os.name != "nt").create(root / "env")
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1"}
    subprocess.run([sys.executable, "-B", "-m", "pip", "--python", str(interpreter(root)), "install",
        "--disable-pip-version-check", "--no-compile", "-r", str(HERE / identity["requirements"])],
        env=env, check=True, timeout=300)
    subprocess.run([sys.executable, "-B", "-m", "pip", "--python", str(interpreter(root)), "check"],
                   env=env, check=True, timeout=30)
    distributions = probe(root, identity["requirements"])
    files = inventory(root, Path(identity["base_python"]))
    hostlab.write_json(root / "receipt.json", {"schema": POLICY, "fingerprint": fingerprint,
        "identity": identity, "distributions": distributions, "files": files})


def prepare(requirements):
    started = time.monotonic()
    identity, fingerprint = describe(requirements)
    root = directory()
    controlled_root(root)
    root.parent.mkdir(parents=True, exist_ok=True)
    lock_path=root.parent / "hostlab-prepared.lock"
    if is_link(lock_path) or lock_path.exists() and not stat.S_ISREG(lock_path.stat().st_mode):
        raise ValueError("linked or nonregular runtime preparation lock")
    lock = remote_schedule.admission_lock(lock_path)
    if lock is None:
        raise RuntimeError("runtime preparation is already in progress")
    try:
        hit = verify(root, identity, fingerprint)
        repaired = root.exists() and not hit
        if not hit:
            if root.exists():
                # Preserve invalid evidence outside the cached directory; never recursively delete.
                root.rename(root.with_name(root.name + "-invalid-" + uuid.uuid4().hex))
            build(root, identity, fingerprint)
            if not verify(root, identity, fingerprint):
                raise RuntimeError("new runtime failed verification")
        return {"fingerprint": fingerprint, "cache_hit": hit, "built": not hit, "repaired": repaired,
                "python": str(interpreter(root)), "requirements": requirements,
                "elapsed_ms": (time.monotonic() - started) * 1000}
    finally:
        lock.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("fingerprint", "prepare"))
    parser.add_argument("--requirements", required=True, choices=("requirements.txt", "requirements-query.txt"))
    args = parser.parse_args()
    if args.operation == "fingerprint":
        _, fingerprint = describe(args.requirements)
        result = {"fingerprint": fingerprint, "path": str(directory())}
    else:
        result = prepare(args.requirements)
        hostlab.write_json(hostlab.STATE / "preparation.json", result)
        if os.environ.get("GITHUB_PATH"):
            with open(os.environ["GITHUB_PATH"], "a", encoding="utf-8") as stream:
                stream.write(str(Path(result["python"]).parent) + "\n")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
            for key,value in result.items():
                stream.write(key + "=" + (str(value).lower() if type(value) is bool else str(value)) + "\n")
    print(json.dumps(result))


if __name__ == "__main__": main()
