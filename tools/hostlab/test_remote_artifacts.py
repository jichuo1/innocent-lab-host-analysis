"""Artifact integrity, transactional retries, bounded contention and MCP compatibility."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import stat
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
import zipfile

import hostlab
import remote_artifacts as artifacts


def archive_bytes(entries=None):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for name, value in entries or [("remote-output/result.txt", "hello 世界"), ("remote-output/job.json", "{}")]:
            info = zipfile.ZipInfo(name)
            info.filename = name
            archive.writestr(info, value)
    return buffer.getvalue()


class ArtifactTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        p = patch.object(hostlab, "STATE", self.root); p.start(); self.addCleanup(p.stop)
        self.request = "a" * 32
        self.run = {"id": 12, "run_attempt": 1, "head_sha": "b" * 40, "status": "completed",
                    "display_title": "hostlab-" + self.request, "html_url": "https://example.invalid/run/12"}
        self.raw = archive_bytes(); self.transfers = 0; self.api_reads = 0
        self.artifact = {"id": 20, "name": "host-analysis-12", "size_in_bytes": len(self.raw), "expired": False,
            "digest": "sha256:" + hashlib.sha256(self.raw).hexdigest(),
            "workflow_run": {"id": 12, "head_sha": "b" * 40}, "created_at": "2026-10-15T00:00:00Z"}

    def gh(self, args):
        self.api_reads += 1
        return json.dumps({"artifacts": [self.artifact]})

    def download(self, endpoint, target):
        self.transfers += 1
        target.write_bytes(self.raw)

    def get(self, **kwargs):
        return artifacts.get("owner/repo", self.request, self.run, self.gh, downloader=self.download, **kwargs)

    def test_verified_cache_reuses_download_without_network_and_rechecks_every_file(self):
        first = self.get(); second = self.get()
        self.assertFalse(first["cache_hit"]); self.assertTrue(second["cache_hit"])
        self.assertEqual((self.transfers, self.api_reads), (1, 1))
        Path(first["files"][0]).write_text("damaged", encoding="utf-8")
        repaired = self.get()
        self.assertFalse(repaired["cache_hit"])
        self.assertEqual((self.transfers, self.api_reads), (2, 2))
        self.assertNotEqual(first["root"], repaired["root"])

    def test_interrupted_download_does_not_publish_and_retry_recovers(self):
        def interrupted(endpoint, target):
            target.write_bytes(b"partial")
            raise OSError("simulated connection failure")
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.get("owner/repo", self.request, self.run, self.gh, downloader=interrupted)
        self.assertEqual(list(self.root.rglob("receipt.json")), [])
        self.assertEqual(list(self.root.rglob(".fetch-*")), [])
        self.assertFalse(self.get()["cache_hit"])

    def test_archive_digest_and_metadata_identity_are_required(self):
        for change in ({"digest": "sha256:" + "0" * 64}, {"expired": True},
                       {"workflow_run": {"id": 13, "head_sha": "b" * 40}}, {"digest": None},
                       {"size_in_bytes": artifacts.MAX_ARCHIVE_BYTES + 1}):
            with self.subTest(change=change), patch.dict(self.artifact, change), self.assertRaises(artifacts.ArtifactError):
                self.get()
        self.assertEqual(list(self.root.rglob("receipt.json")), [])

    def test_rerun_uses_a_separate_cache_and_rejects_previous_attempt_artifact(self):
        first = self.get()
        self.run.update(run_attempt=2, run_started_at="2026-10-15T00:10:00Z")
        with self.assertRaisesRegex(artifacts.ArtifactError, "older_attempt"):
            self.get()
        self.artifact["created_at"] = "2026-10-15T00:11:00Z"
        second = self.get()
        self.assertFalse(second["cache_hit"])
        self.assertNotEqual(first["root"], second["root"])

    def test_old_unverified_marker_is_not_trusted(self):
        old = self.root / "remote-results/12"; old.mkdir(parents=True)
        (old / ".downloaded").touch(); (old / "result.txt").write_text("unverified")
        self.assertFalse(self.get()["cache_hit"])
        self.assertEqual(self.transfers, 1)

    def test_malformed_archives_never_publish_outside_or_inside_the_cache(self):
        entries = [[("../outside.txt", "bad")], [("C:/escape.txt", "bad")], [("foo\\bar", "bad")],
                   [("/escape.txt", "bad")], [("A.txt", "a"), ("a.txt", "b")], [("base.apk", "bad")],
                   [("dir/result.txt", "x" * 20)]]
        for rows in entries:
            raw = archive_bytes(rows)
            self.raw = raw
            self.artifact.update(size_in_bytes=len(raw), digest="sha256:" + hashlib.sha256(raw).hexdigest())
            with self.subTest(rows=rows), patch.object(artifacts, "MAX_FILE_BYTES", 10), self.assertRaises(artifacts.ArtifactError):
                self.get()
        self.assertFalse((self.root.parent / "outside.txt").exists())
        self.assertEqual(list(self.root.rglob("receipt.json")), [])

    def test_zip_symlink_and_crc_failure_are_rejected(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            info = zipfile.ZipInfo("link"); info.create_system = 3; info.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(info, "../outside")
        for raw in (buffer.getvalue(), self.raw.replace(b"hello ", b"wrong ", 1)):
            self.raw = raw
            self.artifact.update(size_in_bytes=len(raw), digest="sha256:" + hashlib.sha256(raw).hexdigest())
            with self.assertRaises((artifacts.ArtifactError, zipfile.BadZipFile)):
                self.get()
        self.assertEqual(list(self.root.rglob("receipt.json")), [])

    def test_32_concurrent_requests_coalesce_one_download(self):
        def slow(endpoint, target):
            time.sleep(.04); self.download(endpoint, target)
        with ThreadPoolExecutor(max_workers=32) as pool:
            results = list(pool.map(lambda _: artifacts.get("owner/repo", self.request, self.run, self.gh, downloader=slow), range(32)))
        self.assertEqual((self.transfers, self.api_reads), (1, 1))
        self.assertEqual(sum(not r["cache_hit"] for r in results), 1)
        self.assertTrue(all(r["files"] == results[0]["files"] for r in results))

    def test_multiple_collectors_share_four_download_slots(self):
        mutex = threading.Lock(); active = 0; peak = 0
        def transfer(endpoint, target):
            nonlocal active, peak
            with mutex:
                active += 1; peak = max(peak, active)
            try:
                time.sleep(.04); target.write_bytes(self.raw)
            finally:
                with mutex: active -= 1
        def get(index):
            run = {**self.run, "id": index + 100}
            metadata = {**self.artifact, "name": "host-analysis-" + str(run["id"]),
                        "workflow_run": {"id": run["id"], "head_sha": run["head_sha"]}}
            return artifacts.get("owner/repo", self.request, run, lambda _: json.dumps({"artifacts": [metadata]}), downloader=transfer)
        with ThreadPoolExecutor(max_workers=16) as pool:
            results = list(pool.map(get, range(40)))
        self.assertEqual(len(results), 40); self.assertEqual(peak, 4)

    def test_job_result_unicode_pagination_preserves_interface_and_download_reuse(self):
        import remote_mcp
        self.raw = archive_bytes([("remote-output/result.txt", "中" * 9000), ("remote-output/job.json", "{}")])
        self.artifact.update(size_in_bytes=len(self.raw), digest="sha256:" + hashlib.sha256(self.raw).hexdigest())
        with patch.object(remote_mcp, "REPO", "owner/repo"), patch.object(remote_mcp, "repository_report", return_value=None), \
             patch.object(remote_mcp, "lookup", return_value=self.run), patch.object(remote_mcp, "gh", side_effect=self.gh), \
             patch.object(artifacts, "download", side_effect=self.download):
            first = json.loads(remote_mcp.job_result(self.request))
            second = json.loads(remote_mcp.job_result(self.request, first["result_page"]["next_offset"]))
        self.assertEqual(first["result_page"]["chars"], 8000)
        self.assertEqual(second["result_page"]["chars"], 1000)
        self.assertIsNone(second["result_page"]["next_offset"])
        self.assertEqual(first["result_page"]["file"], str(Path("remote-output/result.txt")))
        self.assertEqual(self.transfers, 1)


if __name__ == "__main__":
    unittest.main()
