"""Sample preparation keeps exact bytes while reusing verified staged inputs."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import io
from pathlib import Path
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import analyze
import hostlab


class SampleFetchTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.blob = self.root / "hub-blob"
        self.content = b"verified APK bytes\x00\xff" * 13
        self.blob.write_bytes(self.content)
        sha = hostlab.digest(self.blob)
        self.row = {"version_code": 9150200, "sha256": sha, "size": len(self.content),
                    "path": f"apks/tv.danmaku.bili/9150200/{sha}/base.apk"}
        self.state = self.root / "state"
        self.target = self.state / "samples" / sha / "base.apk"
        self.addCleanup(patch.stopall)
        patch.object(hostlab, "STATE", self.state).start()
        self.download = patch("huggingface_hub.hf_hub_download", return_value=str(self.blob)).start()

    def fetch(self, row=None, timings=None):
        return analyze.fetch_sample(row or self.row, "test/private", "b" * 40, timings=timings)

    def test_cold_copy_checks_exact_bytes_and_publishes_regular_apk(self):
        timings = {}
        path = self.fetch(timings=timings)
        self.assertEqual(path, self.target)
        self.assertFalse(path.is_symlink())
        self.assertEqual(path.read_bytes(), self.content)
        self.assertEqual(self.blob.read_bytes(), self.content)
        self.assertFalse(timings["staged_cache_hit"])
        self.assertTrue(all(timings[key] >= 0 for key in ("download_ms", "verify_ms", "stage_ms")))
        self.assertEqual(list(self.target.parent.glob("*.apk")), [self.target])
        self.download.assert_called_once_with(repo_id="test/private", repo_type="dataset",
            filename=self.row["path"], revision="b" * 40, token=True)

    def test_warm_cache_rehashes_and_never_downloads(self):
        self.fetch()
        self.download.reset_mock()
        timings = {}
        with patch.object(hostlab, "digest", wraps=hostlab.digest) as digest:
            self.assertEqual(self.fetch(timings=timings), self.target)
            digest.assert_called_once_with(self.target)
        self.download.assert_not_called()
        self.assertTrue(timings["staged_cache_hit"])
        self.assertEqual(timings["download_ms"], 0)

    def test_same_size_corruption_is_recovered_without_trusting_metadata(self):
        self.fetch()
        self.target.write_bytes(b"x" * self.row["size"])
        self.download.reset_mock()
        timings = {}
        self.assertEqual(self.fetch(timings=timings).read_bytes(), self.content)
        self.download.assert_called_once()
        self.assertFalse(timings["staged_cache_hit"])

    def test_bad_source_never_publishes_target_and_retry_recovers(self):
        self.blob.write_bytes(b"x" * self.row["size"])
        with self.assertRaisesRegex(RuntimeError, "integrity mismatch"):
            self.fetch()
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.target.parent.glob("*.apk")), [])
        self.blob.write_bytes(self.content)
        self.assertEqual(self.fetch().read_bytes(), self.content)

    def test_wrong_source_size_is_rejected_before_copy(self):
        self.blob.write_bytes(self.content + b"extra")
        with patch.object(analyze.tempfile, "NamedTemporaryFile") as temp:
            with self.assertRaisesRegex(RuntimeError, "integrity mismatch"):
                self.fetch()
            temp.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_download_failure_is_retryable_and_does_not_publish(self):
        self.download.side_effect = OSError("download interrupted")
        with self.assertRaises(OSError):
            self.fetch()
        self.assertFalse(self.target.exists())
        self.download.side_effect = None
        self.assertEqual(self.fetch().read_bytes(), self.content)

    def test_copy_failure_cleans_temporary_file_and_releases_lock(self):
        original_open = Path.open
        resolved_blob = self.blob.resolve()

        class Interrupted(io.BytesIO):
            def read(self, size=-1):
                raise OSError("interrupted source read")

        def opened(path, *args, **kwargs):
            if path == resolved_blob and args == ("rb",):
                return Interrupted(self.content)
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", opened):
            with self.assertRaisesRegex(OSError, "interrupted"):
                self.fetch()
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.target.parent.glob("*.apk")), [])
        self.assertEqual(self.fetch().read_bytes(), self.content)

    def test_atomic_publication_failure_keeps_prior_file_and_recovers(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(b"x" * self.row["size"])
        with patch.object(analyze.os, "replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                self.fetch()
        self.assertEqual(self.target.read_bytes(), b"x" * self.row["size"])
        self.assertEqual(list(self.target.parent.glob("*.apk")), [self.target])
        self.assertEqual(self.fetch().read_bytes(), self.content)

    def test_regular_apk_download_is_verified_without_extra_copy(self):
        apk = self.root / "download.apk"
        apk.write_bytes(self.content)
        self.download.return_value = str(apk)
        self.assertEqual(self.fetch(), apk)
        self.assertFalse(self.target.exists())
        apk.write_bytes(b"x" * self.row["size"])
        with self.assertRaisesRegex(RuntimeError, "integrity mismatch"):
            self.fetch()

    def test_invalid_identity_never_opens_cache_or_downloads(self):
        for key, value in (("path", "../../outside.apk"), ("sha256", "../outside"),
                           ("size", 0), ("size", True), ("size", 1024**3 + 1),
                           ("version_code", True)):
            with self.subTest(key=key, value=value):
                row = deepcopy(self.row)
                row[key] = value
                with self.assertRaisesRegex(RuntimeError, "Invalid immutable"):
                    self.fetch(row)
        self.download.assert_not_called()
        self.assertFalse(self.state.exists())

    def symlink(self, target, link, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as exc:
            self.skipTest("symlinks unavailable: " + type(exc).__name__)

    def test_linked_target_is_rejected_without_following_or_deleting(self):
        self.target.parent.mkdir(parents=True)
        self.symlink(self.blob, self.target)
        with self.assertRaisesRegex(RuntimeError, "Linked"):
            self.fetch()
        self.assertTrue(self.target.is_symlink())
        self.assertEqual(self.blob.read_bytes(), self.content)
        self.download.assert_not_called()

    def test_dangling_target_link_is_rejected(self):
        self.target.parent.mkdir(parents=True)
        self.symlink(self.root / "absent", self.target)
        with self.assertRaisesRegex(RuntimeError, "Linked"):
            self.fetch()
        self.download.assert_not_called()

    def test_linked_cache_directory_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.state.mkdir()
        self.symlink(outside, self.state / "samples", directory=True)
        with self.assertRaisesRegex(RuntimeError, "Linked"):
            self.fetch()
        self.assertEqual(list(outside.iterdir()), [])
        self.download.assert_not_called()

    def test_linked_lock_is_rejected_before_opening(self):
        self.target.parent.mkdir(parents=True)
        self.symlink(self.blob, self.target.parent / "prepare.lock")
        with self.assertRaisesRegex(RuntimeError, "Linked"):
            self.fetch()
        self.assertEqual(self.blob.read_bytes(), self.content)
        self.download.assert_not_called()

    def test_windows_reparse_attribute_is_rejected_even_for_regular_file_mode(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(self.content)
        original_lstat = Path.lstat

        def linked(path):
            info = original_lstat(path)
            if path == self.target:
                return SimpleNamespace(st_mode=info.st_mode, st_size=info.st_size,
                                       st_file_attributes=0x400)
            return info

        with patch.object(Path, "lstat", linked):
            with self.assertRaisesRegex(RuntimeError, "Linked"):
                self.fetch()
        self.download.assert_not_called()

    def test_lock_wait_is_bounded_without_partial_download(self):
        with patch("remote_schedule.admission_lock", return_value=None), \
             patch.object(analyze.time, "monotonic", side_effect=range(0, 10000, 601)):
            with self.assertRaisesRegex(RuntimeError, "lock timed out"):
                self.fetch()
        self.download.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_concurrent_same_sha_preparation_downloads_once(self):
        entered = threading.Event()

        def download(**kwargs):
            entered.set()
            time.sleep(0.15)
            return str(self.blob)

        self.download.side_effect = download
        metrics = [{} for _ in range(8)]
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda timings: self.fetch(timings=timings), metrics))
        self.assertTrue(entered.is_set())
        self.assertEqual(results, [self.target] * 8)
        self.download.assert_called_once()
        self.assertEqual(sum(m["staged_cache_hit"] for m in metrics), 7)
        self.assertEqual(self.target.read_bytes(), self.content)


if __name__ == "__main__":
    unittest.main()
