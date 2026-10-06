"""Resume a verified local inventory; publish each APK with its manifest atomically."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[2]
state = root / "runtime" / "hostlab"
rows = json.loads((state / "inventory.json").read_text(encoding="utf-8"))["samples"]
env = {**os.environ, "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONIOENCODING": "utf-8"}
settings_file = state / "transfer-settings.json"
if settings_file.exists():
    settings = json.loads(settings_file.read_text(encoding="utf-8"))
    if settings.get("proxy"):
        env["HTTP_PROXY"] = settings["proxy"]
        env["HTTPS_PROXY"] = settings["proxy"]
env["HF_XET_HIGH_PERFORMANCE"] = "1"
log = state / "upload-state.json"
status = {"total": len(rows), "completed": [], "failed": []}
status["started_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
status["proxy_enabled"] = bool(env.get("HTTPS_PROXY"))
for row in sorted(rows, key=lambda x: x["version_code"], reverse=True):
    status["current_version_code"] = row["version_code"]
    status["current_started_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    temp = log.with_suffix(".tmp")
    temp.write_text(json.dumps(status, indent=2), encoding="utf-8")
    os.replace(temp, log)
    print(f"Publishing {row['version_name']} / {row['version_code']}", flush=True)
    ok = False
    for attempt in range(3):
        rc = subprocess.call([sys.executable, str(Path(__file__).with_name("hostlab.py")),
                              "upload", row["local_path"]], cwd=root, env=env)
        if rc == 0:
            ok = True
            break
        if attempt < 2:
            time.sleep(5)
    status["completed" if ok else "failed"].append(row["sha256"])
    temp = log.with_suffix(".tmp")
    temp.write_text(json.dumps(status, indent=2), encoding="utf-8")
    os.replace(temp, log)
    if not ok:
        print("Stopped after three failures; rerun to resume verified remote samples", flush=True)
        sys.exit(1)
print("All inventory samples published", flush=True)
