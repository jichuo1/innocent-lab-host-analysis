"""Exact-APK compatibility and workflow timings; raw APK/DEX never enters result artifacts."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

import analysis_batch
import hostlab

CONTENT = "Lcom/bapis/bilibili/main/community/reply/v1/Content;"
METHOD = CONTENT + "->getUrlsMap()Ljava/util/Map;"


def tasks():
    return [
        {"id": "class", "operation": "locate", "kind": "class", "name": CONTENT, "limit": 1000},
        {"id": "methods", "operation": "locate", "kind": "method", "name": "getUrlsMap", "limit": 1000},
        {"id": "fields", "operation": "locate", "kind": "field", "name": "urls_", "owner": CONTENT, "limit": 1000},
        {"id": "string", "operation": "refs", "kind": "string", "target": "disable_underline", "limit": 1000},
        {"id": "callers", "operation": "refs", "kind": "method", "target": METHOD, "limit": 1000},
        {"id": "field_refs", "operation": "refs", "kind": "field", "target": CONTENT + "->urls_:Lcom/google/protobuf/MapFieldLite;", "limit": 1000},
        {"id": "type_refs", "operation": "refs", "kind": "type", "target": CONTENT, "limit": 1000},
        {"id": "smali", "operation": "decode", "method": METHOD},
        {"id": "manifest", "operation": "info"},
        {"id": "string_reused", "operation": "refs", "kind": "string", "target": "disable_underline", "limit": 1000},
    ]


def canonical(report):
    rows = {}
    for task in report["tasks"]:
        result = task["result"]
        if "identities" in result:
            values = sorted((r["entry_name"], r["descriptor"]) for r in result["identities"])
            encoded = json.dumps(values, ensure_ascii=False, separators=(",", ":")).encode()
            rows[task["id"]] = {"rows": len(values), "distinct": len(set(values)), "sha256": hashlib.sha256(encoded).hexdigest()}
    return rows


async def verify(apk, sample, output, *, rounds=2, jadx=False):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    apk = Path(apk).resolve(strict=True)
    if hostlab.digest(apk) != sample["sha256"]:
        raise RuntimeError("verification sample SHA mismatch")
    proof = {"scope": "offline_static_only", "sample": sample, "rounds": [],
             "os": os.name, "cpu_count": os.cpu_count(), "result_multisets_equal": False,
             "measurement": "serial real MCP sessions; OS file cache not flushed; shared input fetched once"}
    here = Path(__file__).resolve().parent
    source_files = [here / name for name in ("verify_backends.py", "analysis_batch.py", "analysis_plan.py", "install_dexsql.py",
                                             "analyze.py", "hostlab.py", "dexq/server.py", "dexq/dexq_workers.py")]
    proof["tools"] = {str(p.relative_to(here)):hostlab.digest(p) for p in source_files}
    baseline = None
    previous_cache = os.environ.get("DEXQ_CACHE_DIR")
    try:
        # A fresh validation cache leaves the user's normal structural index intact.
        os.environ["DEXQ_CACHE_DIR"] = str(output / "sqlite-cache")
        for i in range(rounds):
            for backend in (["sqlite", "dexsql"] if i % 2 else ["dexsql", "sqlite"]):
                started = time.monotonic()
                report = await analysis_batch.execute(apk, {"backend": backend, "timeout_seconds": 600,
                    "threads": 2, "tasks": tasks()}, roots=[apk.parent], sample=sample)
                if not report["complete"]:
                    # Keep bounded error evidence while withholding raw code from public CI artifacts.
                    hostlab.write_json(output / "failure.json", {"backend": backend,
                        "tasks": [{k:v for k,v in t.items() if k != "result"} for t in report["tasks"]],
                        "sessions": report["sessions"]})
                    raise RuntimeError("backend validation incomplete: " + backend)
                identities = canonical(report)
                if baseline is None:
                    baseline = identities
                if identities != baseline:
                    raise RuntimeError("backend result multisets differ: " + backend)
                mapped = {t["id"]:t for t in report["tasks"]}
                if not all(identities[name]["rows"] > 0 for name in ("class", "methods", "fields", "callers", "field_refs", "type_refs")):
                    raise RuntimeError("verification anchor unexpectedly missing")
                if mapped["string_reused"]["reused_from"] != "string":
                    raise RuntimeError("identical semantic task did not reuse its result")
                manifest = mapped["manifest"]["result"]["manifest"]
                package = manifest["manifest"]["package"] if backend == "dexsql" else manifest["package"]
                code = manifest["manifest"]["android:versionCode"] if backend == "dexsql" else manifest["versionCode"]
                if package != "tv.danmaku.bili" or int(code) != sample["version_code"]:
                    raise RuntimeError("Manifest does not match pinned sample identity")
                body = mapped["smali"]["result"]["smali"]
                if "internalGetUrls" not in body or "unmodifiableMap" not in body:
                    raise RuntimeError("Smali consumer semantics mismatch")
                proof["rounds"].append({"round": i+1, "backend": backend,
                    "total_ms": (time.monotonic() - started) * 1000, "sessions": report["sessions"],
                    "identities": identities, "backend_versions": report["backend_versions"],
                    "tasks": [{k:v for k,v in t.items() if k != "result"} for t in report["tasks"]]})
                hostlab.write_json(output / "verification.json", proof)
        proof["result_multisets_equal"] = True
        if jadx:
            import analyze
            jar = analyze.jar_path()
            if jar is None:
                raise RuntimeError("pinned JADX missing")
            with tempfile.TemporaryDirectory(prefix="hostlab-jadx-validation-") as temp:
                classes = Path(temp) / "classes"
                classes.mkdir()
                subprocess.run(["javac", "-encoding", "UTF-8", "-cp", str(jar), "-d", str(classes),
                                str(analyze.SUITE / "SingleClassDump.java")], check=True, timeout=120,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                began = time.monotonic()
                with (Path(temp) / "source.java").open("wb") as source, (Path(temp) / "java.log").open("wb") as log:
                    rc = subprocess.run(["java", "-Xmx4g", "-Dhostlab.output=" + str(Path(temp) / "jadx"),
                        "-cp", str(classes) + os.pathsep + str(jar), "SingleClassDump", str(apk),
                        "com.bapis.bilibili.main.community.reply.v1.Content"], stdout=source, stderr=log, timeout=180).returncode
                source_bytes = (Path(temp) / "source.java").read_bytes()
                if rc != 0 or b"getUrlsMap" not in source_bytes:
                    raise RuntimeError("existing JADX CLI path failed")
                proof["jadx"] = {"verified": True, "elapsed_ms": (time.monotonic() - began)*1000,
                                 "sha256": hostlab.digest(jar), "output_bytes": len(source_bytes)}
        proof["source_sha_reverified"] = hostlab.digest(apk) == sample["sha256"]
        if not proof["source_sha_reverified"]:
            raise RuntimeError("sample changed during verification")
        proof["tool_sources_unchanged"] = all(hostlab.digest(p) == proof["tools"][str(p.relative_to(here))] for p in source_files)
        if not proof["tool_sources_unchanged"]:
            raise RuntimeError("tool source changed during verification")
        hostlab.write_json(output / "verification.json", proof)
        return proof
    finally:
        if previous_cache is None:
            os.environ.pop("DEXQ_CACHE_DIR", None)
        else:
            os.environ["DEXQ_CACHE_DIR"] = previous_cache


if __name__ == "__main__":
    import analyze
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--apk", type=Path)
    source.add_argument("--version-code", type=int)
    parser.add_argument("--sha256")
    parser.add_argument("--revision")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, choices=(1,2,3), default=2)
    parser.add_argument("--jadx", action="store_true")
    args = parser.parse_args()
    apk, sample = analyze.inputs(args)
    result = asyncio.run(verify(apk, sample, args.output, rounds=args.rounds, jadx=args.jadx))
    print(json.dumps({"complete": True, "result_multisets_equal": result["result_multisets_equal"], "rounds": len(result["rounds"])}))
