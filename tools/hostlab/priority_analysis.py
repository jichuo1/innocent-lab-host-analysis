"""Audit all detected priority families and compare a pinned baseline APK."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import SimpleNamespace
import json
import os
import sys
import zipfile
import analyze
import hostlab
import surface_workers as W


def scan_apk(apk, sample):
    with zipfile.ZipFile(apk) as archive:
        names = [n for n in archive.namelist() if __import__("re").fullmatch(r"classes\d*\.dex", n)]
    names.sort(key=lambda n:int(__import__("re").sub(r"\D", "", n) or 1))
    jobs = [(str(apk), name, idx) for idx, name in enumerate(names)]
    with ProcessPoolExecutor(max_workers=min(2, os.cpu_count() or 1), initializer=W.W.init_worker) as pool:
        report = W.summarize(list(pool.map(W.scan, jobs)))
    report["sample"] = sample
    return report


def resolve(code, sha, revision):
    return analyze.inputs(SimpleNamespace(apk=None, version_code=code, sha256=sha, revision=revision))


def audit_sample(sample, revision):
    rc = analyze.main(["audit", "--version-code", str(sample["version_code"]),
                       "--sha256", sample["sha256"], "--revision", revision])
    folder = hostlab.STATE / "reports" / str(sample["version_code"]) / sample["sha256"][:16]
    paths = sorted(folder.glob("*/summary.json"))
    report = json.loads(paths[-1].read_text(encoding="utf-8")) if paths else {}
    if rc not in (0, 1) or not report.get("features"):
        raise RuntimeError("Standard audit did not produce usable FEATURE evidence")
    return {"exit_code": rc, "features": report["features"], "runtime_verified": False,
            "scope": "legacy_offline_auditor_snapshot_not_production_coverage"}


def main():
    code = int(os.environ["HOSTLAB_VERSION"])
    revision = os.environ["HOSTLAB_REVISION"]
    sha = os.environ["HOSTLAB_SHA"]
    out = hostlab.STATE / "remote-output"
    out.mkdir(parents=True, exist_ok=True)
    target_apk, target_sample = resolve(code, sha, revision)
    target_audit = audit_sample(target_sample, revision)
    target = scan_apk(target_apk, target_sample)
    hostlab.write_json(out / "priority-target.json", target)
    baseline_sha = os.environ.get("HOSTLAB_BASELINE_SHA", "")
    baseline = None
    baseline_audit = None
    if baseline_sha:
        repo = hostlab.config()["repo"]
        rows = hostlab.manifest(repo, revision)["samples"]
        row = next(r for r in rows if r["sha256"] == baseline_sha)
        if row.get("certificate_sha256") != target_sample.get("certificate_sha256"):
            raise RuntimeError("Baseline signing lineage differs")
        apk, sample = resolve(row["version_code"], baseline_sha, revision)
        baseline_audit = audit_sample(sample, revision)
        baseline = scan_apk(apk, sample)
        hostlab.write_json(out / "priority-baseline.json", baseline)
    changes = W.compare(baseline, target) if baseline else []
    context = Path(__file__).with_name("production-context.json")
    source_context = json.loads(context.read_text(encoding="utf-8")) if context.exists() else None
    summary = {"sample": target_sample, "baseline": baseline["sample"] if baseline else None,
               "standard_target_audit": target_audit, "standard_baseline_audit": baseline_audit,
               "changes": changes, "families": target["families"], "unknown_families": target["unknown_families"],
               "coverage_claim": "candidate_discovery_only", "ai_status": "not_configured",
               "source_snapshot": source_context,
               "page_path_matrix": target["page_path_matrix"],
               "protocol_paths": target["protocol_paths"],
               "protocol_twins": target["protocol_twins"], "unregistered_protocols": target["unregistered_protocols"],
               "unclassified_protocol_callers": target["unclassified_protocol_callers"],
               "runtime_verified": False, "limitations": target["limitations"]}
    summary["analysis_status"] = "REVIEW_REQUIRED" if (changes or target["unknown_families"] or
        target["unregistered_protocols"] or (source_context or {}).get("unmapped_multi_path_candidates")) else "NO_STATIC_DRIFT_FOUND"
    hostlab.write_json(out / "priority-summary.json", summary)
    lines = ["# 页面多路径覆盖与样式变化审计", "", "分析结果：" + summary["analysis_status"], "",
             "任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 未接入，运行期样式启用未知。", "",
             "| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |", "|---|---:|---:|---:|---|"]
    for family, r in target["families"].items():
        lines.append(f"| {family} | {r['classes']} | {r['compose_methods']} | {r['external_invoke_edges']} | {r['evidence']} |")
    lines += ["", "## 需要复核的变化", "", *[f"- {r['family']}: {r['kind']}" for r in changes],
              "", "## 未归类的源码多路径候选", "", *["- " + name for name in (source_context or {}).get("unmapped_multi_path_candidates", [])],
              "", "## 未归类协议调用者", "", "完整列表见 priority-summary.json；这些调用者不会静默排除。",
              "", "## 未覆盖边界", "", *["- " + s for s in target["limitations"]]]
    (out / "priority-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"families": len(target["families"]), "changes": len(changes), "ai": "not_configured"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
