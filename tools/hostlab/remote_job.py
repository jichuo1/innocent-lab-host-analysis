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
    os.environ["DEXQ_WORKERS"] = "2"
    repo = "innocent-lab-dev/bilibili-host-apks"
    _, head = hostlab.api_private(repo)
    row = hostlab.select(hostlab.manifest(repo, head), int(code), None)
    hostlab.write_json(hostlab.CONFIG, {"repo": repo})
    base = [sys.executable, str(Path(__file__).with_name("hostlab.py"))]
    source = ["--version-code", code, "--sha256", row["sha256"], "--revision", head]
    if operation == "audit":
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
