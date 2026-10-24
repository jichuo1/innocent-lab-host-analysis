"""Fresh, serial, exact-APK reference/native equivalence and resource measurements."""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import analyze
import hostlab
import priority_analysis
import process_control
import runner_resources
import surface_workers as W

MULTISETS = {"class_records", "invoke_edges", "protocol_definitions", "protocol_twins",
             "unclassified_protocol_callers", "discoveries"}


def normalized(value, *, multiset=False):
    # JSON also normalizes Python tuples; sorting preserves duplicate evidence.
    value = json.loads(json.dumps(value, ensure_ascii=False))
    if multiset:
        value = sorted(json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":")) for row in value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def fingerprint(value, *, multiset=False):
    return {"sha256": hashlib.sha256(normalized(value, multiset=multiset)).hexdigest(),
            "count": len(value) if isinstance(value, (dict, list, tuple)) else None}


def compare(left, right):
    if set(left) != set(right):
        raise RuntimeError("audit evidence fields differ")
    checks = {}
    for key in sorted(left):
        before, after = (fingerprint(v, multiset=key in MULTISETS) for v in (left[key], right[key]))
        checks[key] = {"equal": before == after, "reference": before, "native": after}
    return checks


def evidence(report, surface, tsv, home_log):
    discoveries = [line.split("\t")[1:] for line in Path(tsv).read_text(encoding="utf-8").splitlines()
                   if line.startswith("DISCOVERY\t")]
    return {**{key: value for key, value in surface.items() if key != "scan_execution"},
            "features": report["features"], "discoveries": discoveries,
            "gates": {key: report[key] for key in ("audit_complete", "intake_exit_code", "home_probe_exit_code")},
            "home_probe_sha256": hashlib.sha256(Path(home_log).read_text(encoding="utf-8").encode()).hexdigest()}


def worker(sample, revision, backend, output):
    """Run the real intake/home/FEATURE gates in a fresh process for each backend."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    apk = analyze.fetch_sample(sample, "innocent-lab-dev/bilibili-host-apks", revision)
    start = time.monotonic()
    sampler = runner_resources.make_sampler(disk_path=output)
    sampler.start()
    try:
        folder = hostlab.STATE / "reports" / str(sample["version_code"]) / sample["sha256"][:16]
        previous = set(folder.glob("*/summary.json"))
        carrier = {}
        rc = analyze.main(["audit", "--version-code", str(sample["version_code"]), "--sha256", sample["sha256"],
                           "--revision", revision, "--backend", backend], surface_output=carrier)
        paths = set(folder.glob("*/summary.json")) - previous
        if len(paths) != 1:
            raise RuntimeError("validation did not produce one fresh audit summary")
        summary = paths.pop()
        report = json.loads(summary.read_text(encoding="utf-8"))
        from analysis.run_intake import EXPECTED_FEATURES
        if (rc not in (0, 1) or not report.get("audit_complete") or report["audit_backend"] != backend or
                set(report["features"]) != set(EXPECTED_FEATURES) or
                report["sample"]["sha256"] != sample["sha256"] or report["sample"]["revision"] != revision):
            raise RuntimeError("validation audit failed a retained completeness/identity gate")
        structural_ms = (time.monotonic()-start)*1000
        if backend == "dexsql":
            surface = carrier["report"]
        else:
            surface = priority_analysis.scan_apk(apk, report["sample"])
        surface["sample"] = report["sample"]
        if hostlab.digest(apk) != sample["sha256"]:
            raise RuntimeError("validation input changed during analysis")
        hostlab.write_json(output/"evidence.json", evidence(report, surface, summary.with_name("features.tsv"),
                                                         summary.with_name("home-frame.log")))
        metrics = {"backend": backend, "elapsed_ms": (time.monotonic()-start)*1000,
                   "audit_and_shared_scan_ms": structural_ms, "surface": surface["scan_execution"],
                   "native": report.get("native_audit"), "audit_complete": True, "exit_code": rc}
    finally:
        resources = sampler.stop(output/"resources.json")
    metrics["resources"] = resources
    hostlab.write_json(output/"metrics.json", metrics)


def verify(samples, revision, output, *, rounds=2):
    if (len(samples) != 2 or samples[0]["sha256"] == samples[1]["sha256"] or
            samples[0].get("certificate_sha256") != samples[1].get("certificate_sha256") or
            type(rounds) is not int or rounds not in {1, 2, 3}):
        raise ValueError("validation requires distinct target/baseline with matching signing lineage and 1..3 rounds")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    proof = {"scope": "offline_static_only", "complete": False, "samples": samples,
             "sample_revision": revision, "system": platform.platform(), "cpu_count": os.cpu_count(),
             "measurement": "fresh serial processes; shared fetched APK; OS cache retained; order alternates by round/sample",
             "tools": {**analyze.tool_hashes(), "verify_audits.py": hostlab.digest(Path(__file__))}, "rounds": []}
    pair = {}
    for number in range(rounds):
        for index, sample in enumerate(samples):
            side = "target" if index == 0 else "baseline"
            sample_file = output/(side+"-sample.json")
            hostlab.write_json(sample_file, sample)
            runs, paths = [], {}
            for backend in (["legacy", "dexsql"] if (number+index)%2 == 0 else ["dexsql", "legacy"]):
                folder = output/f"round-{number+1}-{side}-{backend}"
                folder.mkdir(exist_ok=True)
                with (folder/"worker.log").open("wb") as log:
                    rc = process_control.run([sys.executable, str(Path(__file__)), "worker", "--sample", str(sample_file),
                        "--revision", revision, "--backend", backend, "--output", str(folder)], stdout=log, timeout=1500)
                if rc != 0:
                    raise RuntimeError(f"audit validation worker failed: {side}/{backend} rc={rc}")
                runs.append(json.loads((folder/"metrics.json").read_text(encoding="utf-8")))
                paths[backend] = folder/"evidence.json"
            left, right = (json.loads(paths[b].read_text(encoding="utf-8")) for b in ("legacy", "dexsql"))
            checks = compare(left, right)
            proof["rounds"].append({"round": number+1, "sample": side, "runs": runs, "checks": checks,
                                    "all_equal": all(v["equal"] for v in checks.values())})
            hostlab.write_json(output/"verification.json", proof)
            if not proof["rounds"][-1]["all_equal"]:
                raise RuntimeError("native audit equivalence failed: "+side+"/"+",".join(k for k,v in checks.items() if not v["equal"]))
            pair[side] = paths
            del left, right
            gc.collect()
    outcomes = {}
    for backend in ("legacy", "dexsql"):
        target, baseline = (json.loads(pair[side][backend].read_text(encoding="utf-8")) for side in ("target", "baseline"))
        changes = W.compare(baseline, target)
        resources = priority_analysis.resource_changes(baseline, target)
        outcomes[backend] = {"changes": changes, "resource_changes": resources,
            "verdict": priority_analysis.verdict(changes, target, None, resources, True)}
    proof["pair_checks"] = compare(outcomes["legacy"], outcomes["dexsql"])
    proof["tools_reverified"] = proof["tools"] == {**analyze.tool_hashes(), "verify_audits.py": hostlab.digest(Path(__file__))}
    proof["complete"] = proof["tools_reverified"] and all(v["equal"] for v in proof["pair_checks"].values())
    hostlab.write_json(output/"verification.json", proof)
    if not proof["complete"]:
        raise RuntimeError("target/baseline change or verdict equivalence failed")
    return proof


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("worker",))
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--backend", choices=("legacy", "dexsql"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    worker(json.loads(args.sample.read_text(encoding="utf-8")), args.revision, args.backend, args.output)


if __name__ == "__main__":
    main()
