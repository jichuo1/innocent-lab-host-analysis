"""Read-only APK analysis, reusing the project's explicit offline audit rules."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import hostlab
import process_control
import runner_resources

HERE = Path(__file__).resolve().parent
SUITE = HERE / "analysis"


def jar_path(explicit=None):
    candidates = [explicit, os.environ.get("HOSTLAB_JADX_JAR"),
                  str(HERE / "vendor/jadx-1.5.6-all.jar"),
                  str(Path.home() / "jadx/lib/jadx-1.5.6-all.jar")]
    return next((Path(x).resolve() for x in candidates if x and Path(x).is_file()), None)


def inputs(args):
    if args.apk:
        path = args.apk.resolve()
        row = hostlab.identity(path)
        return path, {**row, "source": "local"}
    from huggingface_hub import hf_hub_download
    repo = hostlab.config()["repo"]
    _, head = hostlab.api_private(repo)
    revision = args.revision or head
    row = hostlab.select(hostlab.manifest(repo, revision), args.version_code, args.sha256)
    return fetch_sample(row, repo, revision), {**row, "source": "huggingface", "repo": repo, "revision": revision}


def fetch_sample(row, repo, revision, *, timings=None):
    """Fetch one already-selected immutable sample; batch tasks share this input."""
    from huggingface_hub import hf_hub_download
    from remote_schedule import admission_lock
    metrics = timings if timings is not None else {}
    metrics.update(download_ms=0.0, verify_ms=0.0, stage_ms=0.0, staged_cache_hit=False)
    started = time.monotonic()
    lock = temp = None

    def regular(path):
        try:
            info = path.lstat()
        except FileNotFoundError:
            return None
        if not stat.S_ISREG(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise RuntimeError("Linked or nonregular sample cache file")
        return info

    def matches(path):
        checked = time.monotonic()
        try:
            info = regular(path)
            return info is not None and info.st_size == row["size"] and hostlab.digest(path) == row["sha256"]
        finally:
            metrics["verify_ms"] += (time.monotonic() - checked) * 1000

    try:
        code, sha, size = row["version_code"], row["sha256"], row["size"]
        if (type(code) is not int or not 1 <= code <= 9999999999 or not isinstance(sha, str)
                or not re.fullmatch(r"[0-9a-f]{64}", sha) or type(size) is not int
                or not 1 <= size <= 1024 * 1024 * 1024
                or row["path"] != f"apks/tv.danmaku.bili/{code}/{sha}/base.apk"):
            raise RuntimeError("Invalid immutable sample identity")
        root = hostlab.STATE.absolute()
        target = root / "samples" / sha / "base.apk"
        # Check all existing ancestors before mkdir/open, including Windows junctions.
        for directory in reversed((target.parent, *target.parent.parents)):
            try:
                info = directory.lstat()
            except FileNotFoundError:
                continue
            if not stat.S_ISDIR(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise RuntimeError("Linked or non-directory sample cache path")
        target.parent.mkdir(parents=True, exist_ok=True)
        lock_path = target.parent / "prepare.lock"
        regular(lock_path)
        deadline = time.monotonic() + 600
        while lock is None:
            lock = admission_lock(lock_path)
            if lock is None:
                if time.monotonic() >= deadline:
                    raise RuntimeError("Sample preparation lock timed out")
                time.sleep(0.05)
        if matches(target):
            metrics["staged_cache_hit"] = True
            return target
        downloaded = time.monotonic()
        try:
            path = Path(hf_hub_download(repo_id=repo, repo_type="dataset", filename=row["path"],
                                       revision=revision, token=True))
        finally:
            metrics["download_ms"] += (time.monotonic() - downloaded) * 1000
        # Hub snapshots on Linux link to extensionless blobs. Verify the bytes
        # while copying, then publish only the complete regular .apk file.
        resolved = path.resolve(strict=True)
        info = regular(resolved)
        if info is None or info.st_size != size:
            raise RuntimeError("APK download integrity mismatch")
        if resolved.suffix.lower() == ".apk":
            if not matches(resolved):
                raise RuntimeError("APK download integrity mismatch")
            return path
        digest, count = hashlib.sha256(), 0
        with resolved.open("rb") as source, tempfile.NamedTemporaryFile(
                dir=target.parent, suffix=".apk", delete=False) as stream:
            temp = Path(stream.name)
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                count += len(chunk)
                if count > size:
                    raise RuntimeError("APK download integrity mismatch")
                checked = time.monotonic()
                digest.update(chunk)
                metrics["verify_ms"] += (time.monotonic() - checked) * 1000
                stream.write(chunk)
        if count != size or digest.hexdigest() != sha:
            raise RuntimeError("APK download integrity mismatch")
        os.replace(temp, target)
        temp = None
        return target
    finally:
        try:
            if temp is not None:
                temp.unlink(missing_ok=True)
        finally:
            if lock is not None:
                lock.close()
            metrics["stage_ms"] = max(0.0, (time.monotonic() - started) * 1000
                                      - metrics["download_ms"] - metrics["verify_ms"])


def tool_hashes():
    files = [HERE / "analyze.py", HERE / "hostlab.py", HERE / "process_control.py",
             HERE / "runner_resources.py", HERE / "remote_job.py", HERE / "priority_analysis.py", HERE / "surface_workers.py",
             *[HERE / n for n in ("audit_common.py", "native_audit.py", "native_cli.py", "native_session.py", "native_graph.py", "native_rules.py", "native_surface.py")],
             SUITE / "audit_catalog.json", *sorted(SUITE.glob("*.py")),
             *sorted(SUITE.glob("*.java"))]
    return {str(p.relative_to(HERE)).replace("\\", "/"): hostlab.digest(p) for p in files}


def execute(command, log, env, timeout):
    with log.open("w", encoding="utf-8") as stream:
        rc = process_control.run(command, stdout=stream, env=env, timeout=timeout)
        if rc == 124:
            stream.write("\nHOSTLAB_TIMEOUT\n")
        return rc


def features(path):
    if not path.is_file():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) >= 3 and fields[0] == "FEATURE":
            result[fields[1]] = {"status": fields[2], "detail": "\t".join(fields[3:])}
    return result


def main(argv, *, surface_output=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor")
    doctor.add_argument("--jadx-jar")
    for name in ("audit", "decompile"):
        p = sub.add_parser(name)
        source = p.add_mutually_exclusive_group(required=True)
        source.add_argument("--apk", type=Path)
        source.add_argument("--version-code", type=int)
        p.add_argument("--sha256")
        p.add_argument("--revision")
        p.add_argument("--jadx-jar")
        p.add_argument("--timeout", type=int, default=900)
        if name == "audit":
            p.add_argument("--mode", choices=("basic", "full"), default="full")
            p.add_argument("--backend", choices=("auto", "dexsql", "legacy"), default=os.environ.get("HOSTLAB_AUDIT_BACKEND", "auto"))
        else:
            p.add_argument("--class", dest="class_name", required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("--base", type=Path, required=True, help="Base summary.json")
    compare.add_argument("--target", type=Path, required=True, help="Target summary.json")
    args = parser.parse_args(argv)
    if args.command == "audit" and args.backend not in {"auto", "dexsql", "legacy"}:
        raise ValueError("HOSTLAB_AUDIT_BACKEND must be auto, dexsql or legacy")
    if args.command == "doctor":
        report = {"python": sys.version.split()[0], "java": shutil.which("java"),
                  "javac": shutil.which("javac"), "jadx_jar": str(jar_path(args.jadx_jar) or "missing")}
        try:
            report["aapt"] = str(hostlab.sdk_tool("aapt.exe"))
            report["apksigner"] = str(hostlab.sdk_tool("apksigner.bat"))
        except RuntimeError:
            report["android_sdk"] = "missing; needed for local APK identity"
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["java"] and report["javac"] and jar_path(args.jadx_jar) else 1
    if args.command == "compare":
        base = json.loads(args.base.read_text(encoding="utf-8"))
        target = json.loads(args.target.read_text(encoding="utf-8"))
        if base.get("mode") != "full" or target.get("mode") != "full" or not base.get("features") or not target.get("features"):
            raise RuntimeError("Comparison requires two full audit reports with FEATURE results")
        same_rules = (base["tools"] == target["tools"] and
                      base.get("jadx_sha256") == target.get("jadx_sha256"))
        changes = []
        for key in sorted(set(base["features"]) | set(target["features"])):
            before, after = base["features"].get(key), target["features"].get(key)
            if before != after:
                changes.append({"feature": key, "base": before, "target": after})
        print(json.dumps({"same_rules": same_rules, "changes": changes,
                          "scope": "offline_static_only"}, ensure_ascii=False, indent=2))
        return 0 if same_rules else 2
    if args.timeout < 1 or args.timeout > 3600:
        raise RuntimeError("Timeout must be between 1 and 3600 seconds")
    jar = jar_path(args.jadx_jar)
    native = None
    fallback = None
    backend = "legacy"
    if args.command == "audit" and args.mode == "full" and args.backend != "legacy":
        import install_dexsql
        if install_dexsql.status()["available"]:
            backend = "dexsql"
        elif args.backend == "dexsql":
            raise RuntimeError("Requested pinned DexSQL audit backend is unavailable")
        else:
            fallback = "dexsql_unavailable"
    needs_java = args.command == "decompile" or args.mode == "full" and backend == "legacy"
    if needs_java and jar is None:
        # A structural-only job need not download JADX; semantic reads and explicit
        # reference/fallback runs obtain the same pinned JAR on demand.
        rc = process_control.run([sys.executable, str(HERE/"install_jadx.py")], stdout=sys.stderr, timeout=120)
        if rc:
            raise RuntimeError("Pinned JADX preparation failed")
        jar = jar_path(args.jadx_jar)
    if needs_java and (not jar or not shutil.which("java") or not shutil.which("javac")):
        raise RuntimeError("Run doctor; install JDK and set HOSTLAB_JADX_JAR")
    if args.command == "decompile" and not re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+", args.class_name):
        raise RuntimeError("Expected raw fully qualified DEX class name")
    apk, sample = inputs(args)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = hostlab.STATE / "reports" / str(sample["version_code"]) / sample["sha256"][:16] / stamp
    out.mkdir(parents=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    if needs_java:
        env["HOSTLAB_AUDIT_HEAP_MIB"] = str(runner_resources.audit_heap_mib())
    if jar:
        env["HOSTLAB_JADX_JAR"] = str(jar)
    try:
        env["HOSTLAB_AAPT"] = str(hostlab.sdk_tool("aapt.exe"))
    except RuntimeError:
        pass
    report = {"scope": "offline_static_only", "sample": sample, "tools": tool_hashes(),
              "jadx_sha256": hostlab.digest(jar) if jar else None, "features": {}}
    report["java_heap_mib"] = int(env["HOSTLAB_AUDIT_HEAP_MIB"]) if needs_java else None
    if args.command == "decompile":
        classes = out / "classes"
        classes.mkdir()
        rc = execute(["javac", "-encoding", "UTF-8", "-cp", str(jar), "-d", str(classes),
                      str(SUITE / "SingleClassDump.java")], out / "compile.log", env, args.timeout)
        if rc == 0:
            with (out / "class.java").open("w", encoding="utf-8") as source, (out / "decompile.log").open("w", encoding="utf-8") as log:
                rc = process_control.run(["java", "-Xmx" + env["HOSTLAB_AUDIT_HEAP_MIB"] + "m", "-XX:+ExitOnOutOfMemoryError", "-Dhostlab.output=" + str(out / "jadx-output"), "-cp", str(classes) + os.pathsep + str(jar),
                                     "SingleClassDump", str(apk), args.class_name], stdout=source,
                                    stderr=log, env=env, timeout=args.timeout)
                if rc == 124:
                    log.write("\nHOSTLAB_TIMEOUT\n")
        report.update({"class": args.class_name, "exit_code": rc,
                       "source_written": rc == 0 and (out / "class.java").is_file() and (out / "class.java").stat().st_size > 0})
        hostlab.write_json(out / "summary.json", report)
        print("Report: " + str(out / "summary.json"))
        print("Source: " + str(out / "class.java"))
        return rc or (0 if report["source_written"] else 1)
    if backend == "dexsql":
        import native_audit
        try:
            native = native_audit.run(apk, sha256=sample["sha256"], surface=surface_output is not None, timeout=args.timeout)
        except native_audit.UnsupportedAudit as exc:
            if args.backend != "auto": raise
            fallback, backend = str(exc), "legacy"
            jar = jar_path(args.jadx_jar)
            if jar is None:
                rc = process_control.run([sys.executable, str(HERE/"install_jadx.py")], stdout=sys.stderr, timeout=120)
                if rc: raise RuntimeError("Pinned JADX fallback preparation failed")
                jar = jar_path(args.jadx_jar)
            if not jar or not shutil.which("java") or not shutil.which("javac"):
                raise RuntimeError("Native audit is unsupported and verified Java fallback is unavailable")
            env["HOSTLAB_JADX_JAR"] = str(jar)
            env["HOSTLAB_AUDIT_HEAP_MIB"] = str(runner_resources.audit_heap_mib())
            report.update(jadx_sha256=hostlab.digest(jar), java_heap_mib=int(env["HOSTLAB_AUDIT_HEAP_MIB"]))
        else:
            native_audit.write_tsv(out/"features.tsv", native, apk.name)
            if surface_output is not None:
                surface_output["report"] = native["surface"]
            report["native_audit"] = {k:v for k,v in native.items() if k not in {"features", "discoveries", "surface"}}
    report.update(audit_backend=backend, backend_fallback_reason=fallback)
    # Each invocation compiles in its own directory; concurrent audits do not share classes.
    with tempfile.TemporaryDirectory(prefix="hostlab-audit-") as temp:
        sandbox = Path(temp)
        for file in SUITE.iterdir():
            if file.suffix in {".py", ".java"}:
                shutil.copyfile(file, sandbox / file.name)
        command = [sys.executable, str(sandbox / "run_intake.py"), str(apk),
                   "--tsv", str(out / "features.tsv")]
        if args.mode == "full" and backend == "legacy":
            command.append("--audit")
        rc = execute(command, out / "intake.log", env, args.timeout)
        if native is not None and backend == "dexsql" and rc in (0, 1):
            import contextlib
            from analysis.run_intake import print_feature_report
            with (out/"intake.log").open("a", encoding="utf-8") as stream, contextlib.redirect_stdout(stream):
                problems = print_feature_report(str(out/"features.tsv"), None)
            rc = 1 if rc or problems else 0
        home_rc = execute([sys.executable, str(sandbox / "home_frame_audit.py"), str(apk)],
                          out / "home-frame.log", env, args.timeout)
    from analysis.run_intake import EXPECTED_FEATURES
    rows = features(out / "features.tsv")
    completed = ((out / "features.tsv").is_file() and
                 "META\taudit_complete\ttrue" in (out / "features.tsv").read_text(encoding="utf-8").splitlines() and
                 set(rows) == set(EXPECTED_FEATURES) and rc in (0, 1) and home_rc == 0)
    report.update({"mode": args.mode, "intake_exit_code": rc, "home_probe_exit_code": home_rc,
                   "audit_complete": completed,
                   "features": rows,
                   "coverage_gaps": "See intake.log; feature set does not cover all installers",
                   "runtime_verified": False})
    hostlab.write_json(out / "summary.json", report)
    print("Report: " + str(out / "summary.json"))
    print(f"Intake exit={rc}; home probe exit={home_rc}; features={len(report['features'])}")
    return rc or home_rc or (1 if args.mode == "full" and not completed else 0)
