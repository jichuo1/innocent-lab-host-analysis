"""Read-only APK analysis, reusing the project's explicit offline audit rules."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import hostlab

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
    path = Path(hf_hub_download(repo_id=repo, repo_type="dataset", filename=row["path"],
                               revision=revision, token=True))
    if path.stat().st_size != row["size"] or hostlab.digest(path) != row["sha256"]:
        raise RuntimeError("APK download integrity mismatch")
    return path, {**row, "source": "huggingface", "repo": repo, "revision": revision}


def tool_hashes():
    files = [HERE / "analyze.py", HERE / "hostlab.py", *sorted(SUITE.glob("*.py")),
             *sorted(SUITE.glob("*.java"))]
    return {str(p.relative_to(HERE)).replace("\\", "/"): hostlab.digest(p) for p in files}


def execute(command, log, env, timeout):
    with log.open("w", encoding="utf-8") as stream:
        try:
            return subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                  env=env, timeout=timeout, check=False).returncode
        except subprocess.TimeoutExpired:
            stream.write("\nHOSTLAB_TIMEOUT\n")
            return 124


def features(path):
    if not path.is_file():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) >= 3 and fields[0] == "FEATURE":
            result[fields[1]] = {"status": fields[2], "detail": "\t".join(fields[3:])}
    return result


def main(argv):
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
        else:
            p.add_argument("--class", dest="class_name", required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("--base", type=Path, required=True, help="Base summary.json")
    compare.add_argument("--target", type=Path, required=True, help="Target summary.json")
    args = parser.parse_args(argv)
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
    needs_java = args.command == "decompile" or args.mode == "full"
    if needs_java and (not jar or not shutil.which("java") or not shutil.which("javac")):
        raise RuntimeError("Run doctor; install JDK and set HOSTLAB_JADX_JAR")
    if args.command == "decompile" and not re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+", args.class_name):
        raise RuntimeError("Expected raw fully qualified DEX class name")
    apk, sample = inputs(args)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = hostlab.STATE / "reports" / str(sample["version_code"]) / sample["sha256"][:16] / stamp
    out.mkdir(parents=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    if jar:
        env["HOSTLAB_JADX_JAR"] = str(jar)
    try:
        env["HOSTLAB_AAPT"] = str(hostlab.sdk_tool("aapt.exe"))
    except RuntimeError:
        pass
    report = {"scope": "offline_static_only", "sample": sample, "tools": tool_hashes(),
              "jadx_sha256": hostlab.digest(jar) if jar else None, "features": {}}
    if args.command == "decompile":
        classes = out / "classes"
        classes.mkdir()
        rc = execute(["javac", "-encoding", "UTF-8", "-cp", str(jar), "-d", str(classes),
                      str(SUITE / "SingleClassDump.java")], out / "compile.log", env, args.timeout)
        if rc == 0:
            with (out / "class.java").open("w", encoding="utf-8") as source, (out / "decompile.log").open("w", encoding="utf-8") as log:
                try:
                    rc = subprocess.run(["java", "-Xmx4g", "-Dhostlab.output=" + str(out / "jadx-output"), "-cp", str(classes) + os.pathsep + str(jar),
                                         "SingleClassDump", str(apk), args.class_name], stdout=source,
                                        stderr=log, env=env, timeout=args.timeout, check=False).returncode
                except subprocess.TimeoutExpired:
                    log.write("\nHOSTLAB_TIMEOUT\n")
                    rc = 124
        report.update({"class": args.class_name, "exit_code": rc,
                       "source_written": rc == 0 and (out / "class.java").is_file() and (out / "class.java").stat().st_size > 0})
        hostlab.write_json(out / "summary.json", report)
        print("Report: " + str(out / "summary.json"))
        print("Source: " + str(out / "class.java"))
        return rc or (0 if report["source_written"] else 1)
    # Each invocation compiles in its own directory; concurrent audits do not share classes.
    with tempfile.TemporaryDirectory(prefix="hostlab-audit-") as temp:
        sandbox = Path(temp)
        for file in SUITE.iterdir():
            if file.suffix in {".py", ".java"}:
                shutil.copyfile(file, sandbox / file.name)
        command = [sys.executable, str(sandbox / "run_intake.py"), str(apk),
                   "--tsv", str(out / "features.tsv")]
        if args.mode == "full":
            command.append("--audit")
        rc = execute(command, out / "intake.log", env, args.timeout)
        home_rc = execute([sys.executable, str(sandbox / "home_frame_audit.py"), str(apk)],
                          out / "home-frame.log", env, args.timeout)
    report.update({"mode": args.mode, "intake_exit_code": rc, "home_probe_exit_code": home_rc,
                   "features": features(out / "features.tsv"),
                   "coverage_gaps": "See intake.log; feature set does not cover all installers",
                   "runtime_verified": False})
    hostlab.write_json(out / "summary.json", report)
    print("Report: " + str(out / "summary.json"))
    print(f"Intake exit={rc}; home probe exit={home_rc}; features={len(report['features'])}")
    return rc or home_rc
