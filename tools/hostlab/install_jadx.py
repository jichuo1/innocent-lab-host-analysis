"""Fetch the official fixed release and verify the exact JAR before use."""
import hashlib
import io
from pathlib import Path
import urllib.request
import zipfile

EXPECTED = "fe3e12c45acf75f92369685fd02d1d7a7323385dc725680a9b98a0dac0ea554b"
URL = "https://github.com/skylot/jadx/releases/download/v1.5.6/jadx-1.5.6.zip"
target = Path(__file__).resolve().parent / "vendor/jadx-1.5.6-all.jar"
if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == EXPECTED:
    print("Pinned JADX already verified")
else:
    with urllib.request.urlopen(URL, timeout=120) as response:
        data = response.read(200 * 1024 * 1024 + 1)
    if len(data) > 200 * 1024 * 1024:
        raise RuntimeError("Release exceeds size bound")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        data = archive.read("lib/jadx-1.5.6-all.jar")
    if hashlib.sha256(data).hexdigest() != EXPECTED:
        raise RuntimeError("JADX JAR checksum mismatch")
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix(".tmp")
    temp.write_bytes(data)
    temp.replace(target)
    print("Official pinned JADX downloaded and verified")
