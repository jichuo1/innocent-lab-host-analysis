"""Reuse immutable static evidence for a new AI review; no fake APK or baseline."""
import json
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import hostlab
import source_snapshot
import snapshot_transport


def review_source(data, explicit_binding):
    previous = data.get("source_snapshot") or {}
    if explicit_binding or previous.get("binding"):
        selected = explicit_binding or json.dumps(previous["binding"], separators=(",", ":"))
        context, binding = snapshot_transport.load_for_analysis(selected)
        source_snapshot.validate(context, expected_sha256=binding["snapshot_sha256"])
        snapshot_transport.cache_snapshot(context, binding)
        metadata = source_snapshot.public_context(context, binding)
        metadata["freshness"] = ("historical_static_evidence_new_source" if explicit_binding else "historical")
    else:
        if previous.get("schema", 0) >= 2:
            raise RuntimeError("Historical verified source binding is missing")
        metadata = {k:v for k,v in previous.items() if k not in {"source_records", "files"}}
        metadata.update({"schema": 0, "legacy": True, "freshness": "historical"})
        metadata["source_records"] = [{k:v for k,v in row.items() if k != "source"}
                                      for row in previous.get("source_records", previous.get("files", []))]
        if any("source" in row for row in previous.get("source_records", [])):
            raw = json.dumps(previous, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            digest = hashlib.sha256(raw).hexdigest()
            cache = hostlab.STATE / "source-snapshots" / ("legacy-" + digest) / "context.json"
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(raw)
            metadata["legacy_cache_sha256"] = digest
        digest = metadata.get("legacy_cache_sha256", "")
        cached = (hostlab.STATE / "source-snapshots" / ("legacy-" + digest) / "context.json"
                  if re.fullmatch(r"[0-9a-f]{64}", digest) else None)
        metadata["source_availability"] = ("legacy_private_cache_available" if cached and cached.is_file()
                                           else "legacy_source_unavailable")
        if metadata["source_availability"] == "legacy_source_unavailable":
            note = "历史报告缺少私有源码全文缓存；module_source 不可用，不会替换为最新源码。"
            if note not in data.setdefault("limitations", []):
                data["limitations"].append(note)
    return metadata


def main():
    source_run = os.environ["HOSTLAB_ARGUMENT"]
    if not re.fullmatch(r"[1-9][0-9]{0,19}", source_run):
        raise RuntimeError("Expected an existing analysis run ID")
    folder = hostlab.STATE / "regenerate-input" / source_run
    folder.mkdir(parents=True, exist_ok=True)
    subprocess.run(["gh", "run", "download", source_run, "--repo", "jichuo1/innocent-lab-host-analysis",
                    "--name", "host-analysis-" + source_run, "--dir", str(folder)], check=True)
    source = folder / "remote-output"
    data = json.loads((source/"priority-summary.json").read_text(encoding="utf-8"))
    if data["sample"]["version_code"] != int(os.environ["HOSTLAB_VERSION"]):
        raise RuntimeError("Requested version differs from source evidence")
    if not (source/"priority-target.json").exists() or (data.get("baseline") and not (source/"priority-baseline.json").exists()):
        raise RuntimeError("Full frozen evidence is missing")
    module_source = review_source(data, os.environ.get("HOSTLAB_MODULE_SOURCE", ""))
    destination = hostlab.STATE/"remote-output"
    destination.mkdir(parents=True, exist_ok=True)
    for p in source.iterdir():
        if p.name.startswith("priority-") or p.name == "job.json":
            shutil.copyfile(p, destination/p.name)
    report = (destination/"priority-report.md").read_text(encoding="utf-8")
    (destination/"priority-report.md").write_text(report.split("\n# AI 适配分析",1)[0],encoding="utf-8")
    data.pop("ai_review",None)
    data["ai_status"] = "pending"
    data["regenerated_from_run"] = int(source_run)
    data["static_evidence_run"] = data.get("static_evidence_run", int(source_run))
    data["source_rebound_for_review"] = bool(os.environ.get("HOSTLAB_MODULE_SOURCE"))
    data["source_snapshot"] = module_source
    hostlab.write_json(destination/"priority-summary.json",data)
    job = json.loads((destination/"job.json").read_text(encoding="utf-8"))
    job["regenerated_from_run"] = int(source_run)
    job["static_evidence_run"] = data["static_evidence_run"]
    job["operation"] = "regenerate_ai"
    job["source_snapshot"] = module_source
    job["source_rebound_for_review"] = data["source_rebound_for_review"]
    hostlab.write_json(destination/"job.json",job)
    if (folder/"reports").exists():
        shutil.copytree(folder/"reports",hostlab.STATE/"reports",dirs_exist_ok=True)
    hostlab.write_json(hostlab.CONFIG,{"repo":"innocent-lab-dev/bilibili-host-apks"})
    print("Frozen evidence restored for AI regeneration")


if __name__ == "__main__":
    main()
