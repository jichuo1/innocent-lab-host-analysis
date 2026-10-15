"""Source preparation and binding tests; no credentials, upload or dispatch."""
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch

import hostlab
import remote_mcp
import source_snapshot as codec
import snapshot_transport as transport


class TransportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="snapshot-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        state = patch.object(hostlab, "STATE", self.root / "state")
        state.start(); self.addCleanup(state.stop)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        "commit", "--allow-empty", "-qm", "fixture"], check=True)
        self.file = self.root / "Bilibili_Innocent_Lab/app/src/main/java/hook/Example.kt"
        self.file.parent.mkdir(parents=True)
        self.file.write_text("class Example\n", encoding="utf-8")
        self.ctx = codec.capture(self.root)
        self.binding = {"schema": 1, "repo": transport.SOURCE_REPO, "revision": "a"*40,
            "snapshot_sha256": hashlib.sha256(codec.serialize(self.ctx)).hexdigest(),
            "source_tree_sha256": self.ctx["source_tree_sha256"], "repository_head": self.ctx["repository_head"],
            "origin": "worktree", "captured_at": self.ctx["captured_at"],
            "verified_at": datetime.now(timezone.utc).isoformat()}
        self.binding["path"] = f"source-snapshots/{self.binding['snapshot_sha256']}/context.json"

    def test_binding_location_revision_hash_and_origin_are_strict(self):
        self.assertEqual(transport.checked_binding(self.binding), self.binding)
        for change in ({"revision":"main"}, {"repo":"attacker/repo"}, {"path":"../secret"},
                       {"snapshot_sha256":"short"}, {"origin":"current"}, {"verified_at":"undated"}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                transport.checked_binding(self.binding | change)
        self.assertNotIn("source", transport.checked_binding(self.binding | {"source":"never public"}))

    def test_upload_readback_is_remote_and_only_writes_the_source_namespace(self):
        from types import SimpleNamespace
        api = unittest.mock.Mock()
        api.create_commit.return_value = SimpleNamespace(oid="a"*40)
        with patch.object(hostlab, "api_private", return_value=(api,"b"*40)), \
             patch.object(transport, "load_pinned", return_value=self.ctx) as downloaded, \
             patch.object(transport, "_publish_pointer") as pointer:
            result = transport.publish(self.ctx)
        downloaded.assert_called_once_with(result, force_remote=True)
        operations = api.create_commit.call_args.kwargs["operations"]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0].path_in_repo, self.binding["path"])
        self.assertNotEqual(operations[0].path_in_repo, "manifest.json")
        pointer.assert_called_once_with(result,None)

    def test_private_cache_revalidates_payload_and_never_fetches_on_valid_hit(self):
        with patch.object(hostlab, "STATE", self.root / "state"), patch.object(hostlab, "api_private", side_effect=AssertionError("network")):
            cache = transport.cache_snapshot(self.ctx, self.binding)
            self.assertEqual(transport.load_pinned(self.binding), self.ctx)
            cache.write_text("{}", encoding="utf-8")
            with self.assertRaises(Exception): transport.load_pinned(self.binding)

    def test_cache_rejects_tree_or_head_binding_mismatch(self):
        with patch.object(hostlab, "STATE", self.root / "state"):
            for changes in ({"source_tree_sha256":"b"*64}, {"repository_head":"b"*40}):
                with self.assertRaises(RuntimeError): transport.cache_snapshot(self.ctx, self.binding | changes)

    def test_published_metadata_read_is_pinned_to_one_commit_and_does_not_need_hf(self):
        calls = []
        def gh(args, payload=None):
            calls.append(args)
            if "git/ref/heads/source-state" in args[1]: return json.dumps({"object":{"sha":"f"*40}})
            return json.dumps({"content":base64.b64encode(codec.serialize(self.binding)).decode()})
        with patch.object(hostlab, "api_private", side_effect=AssertionError("HF")):
            result = transport.resolve_published(gh)
        self.assertEqual(result["origin"], "published")
        self.assertIn("ref=" + "f"*40, calls[1][1])

    def test_explicit_worktree_requires_source_and_remote_only_uses_published(self):
        with patch.object(transport, "resolve_published", return_value=self.binding) as published:
            remote_root = self.root / "empty"
            self.assertEqual(transport.prepare(remote_root), self.binding)
            with self.assertRaises(RuntimeError): transport.prepare(remote_root, mode="worktree")
            self.assertEqual(transport.prepare(self.root, mode="published"), self.binding)
            self.assertEqual(published.call_count, 2)

    def test_edit_during_upload_blocks_dispatch_of_a_stale_worktree(self):
        def upload(ctx, gh):
            self.file.write_text("class NewProgress\n", encoding="utf-8")
            return self.binding
        with patch.object(transport, "publish", side_effect=upload), self.assertRaises(RuntimeError):
            transport.prepare(self.root)

    def test_query_inputs_do_not_capture_or_publish_source(self):
        with patch.object(remote_mcp, "gh", return_value="") as gh, patch.object(hostlab, "STATE", self.root / "state"), \
             patch.object(transport, "prepare", side_effect=AssertionError("source capture")):
            result = json.loads(remote_mcp.submit_job(9150200, "query", "SELECT 1"))
        inputs = gh.call_args.args[1]["inputs"]
        self.assertNotIn("module_source", inputs)
        self.assertIsNone(result["module_source"])

    def test_full_analysis_source_failure_does_not_dispatch(self):
        with patch.object(remote_mcp, "gh") as gh, patch.object(hostlab, "STATE", self.root / "state"), \
             patch.object(transport, "prepare", side_effect=RuntimeError("upload")), self.assertRaises(Exception):
            remote_mcp.submit_job(9150200, "multipath_audit")
        gh.assert_not_called()

    def test_full_analysis_pins_private_source_and_journals_metadata_only(self):
        with patch.object(remote_mcp, "gh", return_value="") as gh, patch.object(hostlab, "STATE", self.root / "state"), \
             patch.object(transport, "prepare", return_value=self.binding):
            result = json.loads(remote_mcp.submit_job(9150200, "multipath_audit"))
            journal = json.loads((hostlab.STATE / "remote-requests" / (result["request_id"]+".json")).read_text())
        self.assertEqual(json.loads(gh.call_args.args[1]["inputs"]["module_source"]), self.binding)
        self.assertEqual(journal["module_source"], self.binding)
        self.assertNotIn("source_records", journal)

    def test_historical_regenerate_does_not_publish_current_source_by_default(self):
        with patch.object(remote_mcp, "gh", return_value="") as gh, patch.object(hostlab, "STATE", self.root / "state"), \
             patch.object(transport, "prepare", side_effect=AssertionError("capture")):
            remote_mcp.submit_job(9150200, "regenerate_ai", "123456")
        self.assertNotIn("module_source", gh.call_args.args[1]["inputs"])

    def test_retrieved_manifest_detects_new_progress_without_modifying_report(self):
        report = {"source_snapshot":codec.public_context(self.ctx, self.binding)}
        with patch.object(hostlab, "ROOT", self.root):
            self.assertEqual(remote_mcp.source_freshness(report)["status"], "current")
            self.file.write_text("class LaterProgress\n", encoding="utf-8")
            self.assertEqual(remote_mcp.source_freshness(report)["status"], "drift")
        self.assertEqual(report["source_snapshot"]["source_tree_sha256"], self.ctx["source_tree_sha256"])

    def seed(self):
        transport.cache_snapshot(self.ctx, self.binding)
        transport._remember_worktree(self.ctx, self.binding)

    def published(self, ctx, gh=None):
        digest = hashlib.sha256(codec.serialize(ctx)).hexdigest()
        result = {**self.binding, "snapshot_sha256": digest, "path": f"source-snapshots/{digest}/context.json",
            "source_tree_sha256": ctx["source_tree_sha256"], "repository_head": ctx["repository_head"],
            "captured_at": ctx["captured_at"]}
        transport.cache_snapshot(ctx, result)
        return result

    def test_exact_worktree_index_hit_reuses_timestamp_and_needs_no_network(self):
        self.seed()
        with patch.object(transport, "publish", side_effect=AssertionError("upload")), \
             patch.object(hostlab, "api_private", side_effect=AssertionError("network")), \
             patch.object(transport, "resolve_published", side_effect=AssertionError("pointer")):
            first = transport.prepare(self.root, mode="worktree")
            second = transport.prepare(self.root)
        self.assertEqual(first, self.binding)
        self.assertEqual(second, self.binding)
        self.assertEqual(first["captured_at"], self.ctx["captured_at"])
        text = transport._worktree_path("current-worktree-binding.json").read_text(encoding="utf-8")
        self.assertNotIn("class Example", text)
        self.assertNotIn("source_records", text)
        self.assertNotIn('"source":', text)

    def test_source_or_head_change_publishes_a_new_binding(self):
        self.seed()
        self.file.write_text("class NewProgress\n", encoding="utf-8")
        with patch.object(transport, "publish", side_effect=self.published) as publish:
            first = transport.prepare(self.root)
            subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "--allow-empty", "-qm", "new head"], check=True)
            second = transport.prepare(self.root)
        self.assertEqual(publish.call_count, 2)
        self.assertNotEqual(first["snapshot_sha256"], self.binding["snapshot_sha256"])
        self.assertNotEqual(second["repository_head"], first["repository_head"])

    def test_dirty_identity_or_corrupt_index_cannot_reuse_the_old_binding(self):
        self.seed()
        index = transport._worktree_path("current-worktree-binding.json")
        value = json.loads(index.read_text(encoding="utf-8"))
        value["identity"]["working_tree_dirty"] = not value["identity"]["working_tree_dirty"]
        index.write_text(json.dumps(value), encoding="utf-8")
        with patch.object(transport, "publish", side_effect=self.published) as publish:
            transport.prepare(self.root)
            index.write_text("{broken", encoding="utf-8")
            transport.prepare(self.root)
        self.assertEqual(publish.call_count, 2)

    def test_corrupt_payload_is_repaired_only_at_the_exact_pinned_revision(self):
        self.seed()
        cached = hostlab.STATE / "source-snapshots" / self.binding["snapshot_sha256"] / "context.json"
        cached.write_text("{}", encoding="utf-8")
        remote = self.root / "verified-remote.json"
        remote.write_bytes(codec.serialize(self.ctx))
        with patch.object(transport, "publish", side_effect=AssertionError("upload")), \
             patch.object(hostlab, "api_private", return_value=(None, "f" * 40)), \
             patch("huggingface_hub.hf_hub_download", return_value=str(remote)) as download:
            actual = transport.prepare(self.root)
        self.assertEqual(actual, self.binding)
        download.assert_called_once_with(repo_id=transport.SOURCE_REPO, repo_type="dataset", filename=self.binding["path"],
            revision=self.binding["revision"], token=True, force_download=True)

    def test_capture_secret_gate_cannot_be_bypassed_by_a_cached_binding(self):
        self.seed()
        self.file.write_text('val API_TOKEN = "hf_' + 'a' * 40 + '"\n', encoding="utf-8")
        with patch.object(transport, "publish") as publish, self.assertRaisesRegex(ValueError, "secret gate"):
            transport.prepare(self.root)
        publish.assert_not_called()

    def test_index_reparse_is_ignored_without_reading_or_overwriting_it(self):
        self.seed()
        index = transport._worktree_path("current-worktree-binding.json")
        raw = index.read_bytes()
        original = Path.lstat
        def reparse(path):
            info = original(path)
            return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400,
                st_nlink=1, st_size=info.st_size) if path == index else info
        with patch.object(Path, "lstat", reparse), patch.object(transport, "load_pinned", side_effect=AssertionError("unsafe read")), \
             patch.object(transport, "publish", side_effect=self.published) as publish:
            transport.prepare(self.root)
        self.assertEqual(publish.call_count, 1)
        self.assertEqual(index.read_bytes(), raw)

    def test_four_concurrent_misses_publish_the_same_tree_once(self):
        def publish(ctx, gh=None):
            time.sleep(.05)
            return self.published(ctx)
        with patch.object(transport, "publish", side_effect=publish) as posted:
            with ThreadPoolExecutor(max_workers=4) as pool:
                bindings = list(pool.map(lambda _: transport.prepare(self.root), range(4)))
        self.assertEqual(posted.call_count, 1)
        self.assertEqual(len({row["snapshot_sha256"] for row in bindings}), 1)

    def test_worktree_lock_wait_is_bounded_and_never_bypassed(self):
        with patch("remote_schedule.admission_lock", return_value=None), \
             patch.object(transport.time, "monotonic", side_effect=(0, 121)), \
             patch.object(transport, "publish") as publish, self.assertRaisesRegex(RuntimeError, "busy"):
            transport.prepare(self.root)
        publish.assert_not_called()


if __name__ == "__main__": unittest.main()
