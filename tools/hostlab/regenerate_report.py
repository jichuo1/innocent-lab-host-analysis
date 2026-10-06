"""Reuse immutable static evidence for a new AI review; no fake APK or baseline."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import hostlab


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
    if not (source/"priority-target.json").exists() or not (source/"priority-baseline.json").exists():
        raise RuntimeError("Full frozen evidence is missing")
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
    hostlab.write_json(destination/"priority-summary.json",data)
    job = json.loads((destination/"job.json").read_text(encoding="utf-8"))
    job["regenerated_from_run"] = int(source_run)
    hostlab.write_json(destination/"job.json",job)
    if (folder/"reports").exists():
        shutil.copytree(folder/"reports",hostlab.STATE/"reports",dirs_exist_ok=True)
    hostlab.write_json(hostlab.CONFIG,{"repo":"innocent-lab-dev/bilibili-host-apks"})
    print("Frozen evidence restored for AI regeneration")


if __name__ == "__main__":
    main()
