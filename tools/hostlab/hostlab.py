"""Private Hugging Face host APK library. No credentials in project files."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "runtime" / "hostlab"
CONFIG = STATE / "config.json"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sdk_tool(name):
    sdk = Path(os.environ.get("ANDROID_HOME") or
               Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk")
    candidates = sorted((sdk / "build-tools").glob("*/" + name), reverse=True)
    if not candidates:
        raise RuntimeError("Android SDK tool missing: " + name)
    return candidates[0]


def identity(path):
    # aapt on Windows cannot reliably open Unicode paths.
    with tempfile.TemporaryDirectory(prefix="hostlab-") as temp:
        import shutil
        target = Path(temp) / "host.apk"
        shutil.copyfile(path, target)
        output = subprocess.check_output(
            [str(sdk_tool("aapt.exe")), "dump", "badging", str(target)],
            text=True, encoding="utf-8", errors="replace", stderr=subprocess.STDOUT)
        match = re.search(r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'", output)
        if not match or match[1] != "tv.danmaku.bili":
            raise RuntimeError("APK identity missing or package is not tv.danmaku.bili")
        # Pass cmd arguments as a list; temporary target contains no shell metacharacters.
        cert = subprocess.check_output(
            ["cmd.exe", "/d", "/c", str(sdk_tool("apksigner.bat")), "verify",
             "--print-certs", str(target)], text=True, encoding="utf-8",
            errors="replace", stderr=subprocess.STDOUT)
        fingerprints = re.findall(r"certificate SHA-256 digest: ([0-9a-fA-F]{64})", cert)
        if not fingerprints:
            raise RuntimeError("APK signature verification did not yield certificate fingerprints")
    sha = digest(path)
    return {"package": match[1], "version_code": int(match[2]), "version_name": match[3],
            "sha256": sha, "size": path.stat().st_size,
            "certificate_sha256": sorted(set(x.lower() for x in fingerprints)),
            "path": f"apks/tv.danmaku.bili/{match[2]}/{sha}/base.apk"}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def config():
    if not CONFIG.exists():
        raise RuntimeError("First run: hostlab.py configure OWNER/REPOSITORY")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def api_private(repo):
    from huggingface_hub import HfApi
    api = HfApi(token=True)
    info = api.repo_info(repo_id=repo, repo_type="dataset")
    if not info.private:
        raise RuntimeError("Refusing access: sample repository must be private")
    return api, info.sha


def manifest(repo, revision):
    from huggingface_hub import hf_hub_download
    from huggingface_hub.errors import EntryNotFoundError
    try:
        file = hf_hub_download(repo_id=repo, repo_type="dataset", filename="manifest.json",
                               revision=revision, token=True)
    except EntryNotFoundError:
        return {"schema": 1, "samples": []}
    data = json.loads(Path(file).read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("samples"), list):
        raise RuntimeError("Unsupported manifest")
    return data


def select(data, code, sha):
    rows = [x for x in data["samples"] if x["version_code"] == code and
            (not sha or x["sha256"] == sha)]
    if len(rows) != 1:
        raise RuntimeError(f"Expected exactly one sample, got {len(rows)}; use --sha256 to disambiguate")
    row = rows[0]
    expected = f"apks/tv.danmaku.bili/{code}/{row['sha256']}/base.apk"
    if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) or row["path"] != expected:
        raise RuntimeError("Invalid manifest path or hash")
    return row


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "dexq":
        import dexq_cli
        sys.exit(dexq_cli.main(sys.argv[2:]))
    if len(sys.argv) > 1 and sys.argv[1] in {"doctor", "audit", "compare", "decompile"}:
        import analyze
        sys.exit(analyze.main(sys.argv[1:]))
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("login")
    setup = commands.add_parser("configure")
    setup.add_argument("repo")
    scan = commands.add_parser("inventory")
    scan.add_argument("directory", type=Path)
    upload = commands.add_parser("upload")
    upload.add_argument("apk", type=Path)
    commands.add_parser("list")
    fetch = commands.add_parser("fetch")
    fetch.add_argument("--version-code", type=int, required=True)
    fetch.add_argument("--sha256")
    fetch.add_argument("--revision")
    args = parser.parse_args()
    if args.command == "upload":
        os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
        transfer_file = STATE / "transfer-settings.json"
        if transfer_file.exists():
            import socket
            from urllib.parse import urlsplit
            proxy = json.loads(transfer_file.read_text(encoding="utf-8")).get("proxy", "")
            parsed = urlsplit(proxy)
            if parsed.hostname in {"127.0.0.1", "localhost", "::1"} and parsed.port:
                try:
                    with socket.create_connection((parsed.hostname, parsed.port), timeout=0.5):
                        pass
                    os.environ["HTTP_PROXY"] = proxy
                    os.environ["HTTPS_PROXY"] = proxy
                    print("Using the configured local upload proxy")
                except OSError:
                    print("Local upload proxy unavailable; using the default route")
    if args.command == "login":
        from getpass import getpass
        from huggingface_hub import login
        token = getpass("Hugging Face token (hidden): ").strip()
        if not token.startswith("hf_"):
            raise RuntimeError("Expected a Hugging Face access token")
        login(token=token, add_to_git_credential=False)
        return
    if args.command == "configure":
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
            raise RuntimeError("Expected OWNER/REPOSITORY")
        api_private(args.repo)
        write_json(CONFIG, {"repo": args.repo})
        print("Private repository configured: " + args.repo)
        return
    if args.command == "inventory":
        samples, seen = [], set()
        for path in sorted(args.directory.resolve().glob("*.apk")):
            row = identity(path)
            if row["sha256"] not in seen:
                samples.append({**row, "local_path": str(path)})
                seen.add(row["sha256"])
            print(f"Verified {row['version_name']} / {row['version_code']} / {row['sha256'][:12]}", flush=True)
        write_json(STATE / "inventory.json", {"schema": 1, "samples": samples})
        print(f"Inventory: {len(samples)} distinct APKs; no uploads performed")
        return
    repo = config()["repo"]
    api, head = api_private(repo)
    revision = getattr(args, "revision", None) or head
    data = manifest(repo, revision)
    if args.command == "list":
        print("Repository revision: " + head)
        for row in data["samples"]:
            print(f"{row['version_name']}\t{row['version_code']}\t{row['sha256']}\t{row['size']}")
    elif args.command == "upload":
        from huggingface_hub import CommitOperationAdd
        row = identity(args.apk.resolve())
        if any(x["sha256"] == row["sha256"] for x in data["samples"]):
            print("Sample already registered: " + row["sha256"])
            return
        data["samples"].append(row)
        data["samples"].sort(key=lambda x: (x["version_code"], x["sha256"]))
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        # Publish APK and index atomically; reject concurrent head changes.
        result = api.create_commit(repo_id=repo, repo_type="dataset", parent_commit=head,
            commit_message=f"chore(samples): add {row['version_code']} {row['sha256'][:12]}",
            operations=[CommitOperationAdd(path_in_repo=row["path"], path_or_fileobj=str(args.apk.resolve())),
                        CommitOperationAdd(path_in_repo="manifest.json", path_or_fileobj=io.BytesIO(payload))])
        remote = manifest(repo, result.oid)
        if row not in remote["samples"]:
            raise RuntimeError("Published manifest readback failed")
        print("Published private sample; commit=" + result.oid)
        bootstrap_path = Path(__file__).with_name("bootstrap-samples.json")
        bootstrap = json.loads(bootstrap_path.read_text(encoding="utf-8")) if bootstrap_path.exists() else []
        if bootstrap_path.exists() and row["sha256"] not in bootstrap:
            import shutil
            if shutil.which("gh"):
                trigger = subprocess.run(["gh", "workflow", "run", "auto-intake.yml", "--repo",
                    "jichuo1/innocent-lab-host-analysis"], capture_output=True, timeout=30)
                print("Automatic intake requested" if trigger.returncode == 0 else
                      "Automatic trigger unavailable; cloud poll will retry")
    elif args.command == "fetch":
        from huggingface_hub import hf_hub_download
        row = select(data, args.version_code, args.sha256)
        file = Path(hf_hub_download(repo_id=repo, repo_type="dataset", filename=row["path"],
                                   revision=revision, token=True))
        if file.stat().st_size != row["size"] or digest(file) != row["sha256"]:
            raise RuntimeError("Downloaded APK size/hash mismatch; do not analyze")
        print("Verified SHA-256: " + row["sha256"])
        print("Revision: " + revision)
        print("APK: " + str(file))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # SDK errors may include request details. Never echo tokens or raw server bodies.
        message = str(exc) if type(exc) is RuntimeError else type(exc).__name__ + ". Check login, private repository and inputs."
        print("Failed: " + message, file=sys.stderr)
        sys.exit(1)
