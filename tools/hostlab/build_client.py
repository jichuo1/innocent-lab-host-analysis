"""Build an allowlisted client archive; never include config, credentials or reports."""
from pathlib import Path
import hashlib
import json
import zipfile

here = Path(__file__).resolve().parent
output = here.parents[1] / "artifacts/hostlab/hostlab-client.zip"
files = [here / name for name in ("hostlab.py", "analyze.py", "dexq_cli.py", "requirements.txt", "README.md",
                                  "setup-client.cmd", "hostlab.cmd", "upload-apk.cmd")]
files += [here / "test_dexq_mcp.py", here / "bench_dexq.py"]
files += [here / "remote_mcp.py", here / "remote_job.py", here / "host-analysis.yml", here / "install_jadx.py"]
files += [here / "requirements-remote.txt", here / "setup-remote.cmd", here / "REMOTE_README.md"]
files += [here / "surface_workers.py", here / "priority_analysis.py", here / "production-context.json",
          here / "bootstrap-samples.json", here / "auto_intake.py", here / "auto-intake.yml"]
files += [here / "ai_review.py", here / "ai_prompts.py", here / "publish_report.py", here / "regenerate_report.py"]
files += sorted(p for p in (here / "analysis").iterdir() if p.suffix in {".py", ".java", ".md"})
files += [here / "vendor/jadx-1.5.6-all.jar", here / "vendor/JADX-LICENSE"]
files += [here / "dexq/server.py", here / "dexq/dexq_workers.py"]
integrity = {}
output.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
    for file in files:
        relative = str(file.relative_to(here)).replace("\\", "/")
        archive.write(file, "tools/hostlab/" + relative)
        integrity[relative] = hashlib.sha256(file.read_bytes()).hexdigest()
    archive.writestr("tools/hostlab/package-integrity.json", json.dumps(integrity, indent=2))
print(str(output))
print(f"Files: {len(files) + 1}; bytes: {output.stat().st_size}")
remote = output.with_name("hostlab-remote-client.zip")
with zipfile.ZipFile(remote, "w", zipfile.ZIP_DEFLATED) as archive:
    for name in ("hostlab.py", "remote_mcp.py", "requirements-remote.txt", "setup-remote.cmd", "REMOTE_README.md"):
        archive.write(here / name, "tools/hostlab/" + name)
print(f"Remote-only client: {remote}; bytes: {remote.stat().st_size}")
