"""Trusted Actions entry point. Inputs are data, never interpolated shell code."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import hostlab
import analyze


def main():
    code = os.environ["HOSTLAB_VERSION"]
    operation = os.environ["HOSTLAB_OPERATION"]
    argument = os.environ.get("HOSTLAB_ARGUMENT", "")
    if not re.fullmatch(r"[1-9][0-9]{0,9}", code) or len(argument) > 4096:
        raise RuntimeError("Invalid bounded input")
    if operation == "regenerate_ai":
        import regenerate_report
        regenerate_report.main()
        return 0
    os.environ["DEXQ_WORKERS"] = "2"
    repo = "innocent-lab-dev/bilibili-host-apks"
    _, current_head = hostlab.api_private(repo)
    head = os.environ.get("HOSTLAB_REVISION") or current_head
    sha = os.environ.get("HOSTLAB_SHA") or None
    if not re.fullmatch(r"[0-9a-f]{40}", head) or (sha and not re.fullmatch(r"[0-9a-f]{64}", sha)):
        raise RuntimeError("Invalid immutable sample identity")
    samples = hostlab.manifest(repo, head)["samples"]
    if operation == "inventory":
        output = hostlab.STATE / "remote-output"
        output.mkdir(parents=True, exist_ok=True)
        keys = ("version_code", "version_name", "sha256", "size", "certificate_sha256")
        inventory = {"schema": 1, "sample_revision": head,
                     "samples": [{k: r[k] for k in keys if k in r}
                                 for r in sorted(samples, key=lambda r: (r["version_code"], r["sha256"]))]}
        hostlab.write_json(output / "inventory.json", inventory)
        hostlab.write_json(output / "job.json", {"operation": operation, "sample_revision": head,
                           "sample_count": len(samples), "exit_code": 0, "scope": "metadata_only"})
        return 0
    row = hostlab.select({"samples": samples}, int(code), sha)
    hostlab.write_json(hostlab.CONFIG, {"repo": repo})
    base = [sys.executable, str(Path(__file__).with_name("hostlab.py"))]
    source = ["--version-code", code, "--sha256", row["sha256"], "--revision", head]
    if operation == "multipath_audit":
        os.environ["HOSTLAB_REVISION"] = head
        os.environ["HOSTLAB_SHA"] = row["sha256"]
        if not os.environ.get("HOSTLAB_BASELINE_SHA"):
            candidates = [r for r in samples if r["version_code"] < row["version_code"] and
                          r.get("certificate_sha256") == row.get("certificate_sha256")]
            if candidates:
                os.environ["HOSTLAB_BASELINE_SHA"] = max(candidates, key=lambda r:r["version_code"])["sha256"]
        command = [sys.executable, str(Path(__file__).with_name("priority_analysis.py"))]
    elif operation == "audit":
        command = base + ["audit"] + source
    elif operation == "decompile":
        command = base + ["decompile"] + source + ["--class", argument]
    elif operation == "query":
        command = base + ["dexq", "query"] + source + ["--sql", argument, "--limit", "100"]
    elif operation == "decode":
        command = base + ["dexq", "decode"] + source + ["--method", argument]
    elif operation == "string_refs":
        command = base + ["dexq", "refs"] + source + ["--kind", "string", "--target", argument, "--limit", "100"]
    elif operation == "info":
        command = base + ["dexq", "info"] + source
    else:
        raise RuntimeError("Unsupported operation")
    output = hostlab.STATE / "remote-output"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "result.txt").open("w", encoding="utf-8") as stream:
        try:
            rc = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                timeout=1500, check=False).returncode
        except subprocess.TimeoutExpired:
            stream.write("Task timed out\n")
            rc = 124
    hostlab.write_json(output / "job.json", {"version_code": int(code), "operation": operation,
        "apk_sha256": row["sha256"], "sample_revision": head, "exit_code": rc,
        "scope": "offline_static_only", "tools": analyze.tool_hashes()})
    return rc


if __name__ == "__main__":
    sys.exit(main())
