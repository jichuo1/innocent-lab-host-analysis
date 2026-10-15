"""Group admission and member identity checks across partial runner failures."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import analysis_plan
import hostlab
import remote_schedule
import runner_group


def payload(count=4):
    return {"schema": 1, "request": {"backend": "dexsql", "tasks": [{"id": "i", "operation": "info"}]},
            "samples": [{"version_code": i + 1, "apk_sha256": format(i, "064x"), "sample_revision": "c" * 40}
                        for i in range(count)]}


class GroupTest(unittest.TestCase):
    def test_private_repository_gate_keeps_bounded_metadata_request(self):
        with patch("huggingface_hub.HfApi") as api:
            api.return_value.repo_info.return_value = SimpleNamespace(private=True, sha="a" * 40)
            self.assertEqual(hostlab.api_private("owner/private")[1], "a" * 40)
            api.return_value.repo_info.assert_called_once_with(repo_id="owner/private", repo_type="dataset", timeout=30)
            api.return_value.repo_info.return_value.private = False
            with self.assertRaises(RuntimeError): hostlab.api_private("owner/private")

    def test_wire_contract_rejects_duplicates_oversize_or_unpinned_selectors(self):
        value = payload()
        runner_group.validate(value)
        for bad in (dict(value, schema=True), dict(value, samples=value["samples"] * 2),
                    dict(value, samples=[value["samples"][0]] * 2),
                    dict(value, samples=[{"version_code": 1}]), dict(value, extra=True)):
            with self.subTest(bad=bad), self.assertRaises(ValueError): runner_group.validate(bad)

    def prepare(self, root, statuses, adaptive=False):
        spec = payload(len(statuses))
        if adaptive:
            spec.update(schema=2, execution={"mode": "adaptive-v1", "prefetch_max": 2})
        value = runner_group.validate(spec)
        receipt = {"schema": 1, "runner_revision": "a" * 40,
                   "request_sha256": analysis_plan.fingerprint(value["request"]), "samples": []}
        files = []
        if adaptive:
            receipt["execution"] = value["execution"]
        for index, (sample, status) in enumerate(zip(value["samples"], statuses)):
            receipt["samples"].append({"index": index, "sample": sample, "status": status})
            if status == "not_started": continue
            output = root / "samples" / str(index); output.mkdir(parents=True)
            metadata = {"operation": "batch", "version_code": sample["version_code"], "apk_sha256": sample["apk_sha256"],
                        "sample_revision": sample["sample_revision"], "runner_revision": "a" * 40,
                        "request_sha256": receipt["request_sha256"], "group_index": index,
                        "complete": status == "complete", "exit_code": 0 if status == "complete" else 2}
            if adaptive:
                metadata["execution_sha256"] = runner_group.execution_fingerprint(value)
            result = {"complete": status == "complete", "source_unchanged": status == "complete",
                      "sample": {"sha256": sample["apk_sha256"], "version_code": sample["version_code"], "revision": sample["sample_revision"]}}
            for name, data in (("job.json", metadata), ("result.txt", result)):
                p = output / name; p.write_text(json.dumps(data), encoding="utf-8"); files.append(str(p))
        p = root / "group.json"; p.write_text(json.dumps(receipt), encoding="utf-8"); files.append(str(p))
        return value, {"files": files}

    def test_adaptive_wire_is_bounded_and_does_not_expand_legacy_groups(self):
        with self.assertRaises(ValueError): runner_group.validate(payload(5))
        spec = {**payload(12), "schema": 2, "execution": {"mode": "adaptive-v1", "prefetch_max": 2}}
        self.assertEqual(len(runner_group.validate(spec)["samples"]), 12)
        for execution in ({"mode": "adaptive-v1", "prefetch_max": 3},
                          {"mode": "adaptive-v1", "prefetch_max": True},
                          {"mode": "adaptive-v2", "prefetch_max": 2}):
            with self.assertRaises(ValueError): runner_group.validate({**spec, "execution": execution})
        with self.assertRaises(ValueError): runner_group.validate({**spec, "samples": payload(13)["samples"]})

    def test_adaptive_policy_is_verified_in_receipt_and_every_member(self):
        with tempfile.TemporaryDirectory() as temp:
            value, downloaded = self.prepare(Path(temp), ["complete"]*12, adaptive=True)
            self.assertTrue(runner_group.collect(value, downloaded, "a"*40)["complete"])
            p = Path(temp)/"samples/11/job.json"
            metadata = json.loads(p.read_text(encoding="utf-8")); metadata["execution_sha256"] = "0"*64
            p.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "execution policy"):
                runner_group.collect(value, downloaded, "a"*40)
            p.write_text(json.dumps({**metadata, "execution_sha256":runner_group.execution_fingerprint(value)}), encoding="utf-8")
            p = Path(temp)/"group.json"; receipt = json.loads(p.read_text(encoding="utf-8")); receipt["execution"]["prefetch_max"] = 1
            p.write_text(json.dumps(receipt), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "execution policy"):
                runner_group.collect(value, downloaded, "a"*40)

    def test_partial_runner_failure_preserves_members_and_interrupted_pending(self):
        with tempfile.TemporaryDirectory() as temp:
            value, downloaded = self.prepare(Path(temp), ["complete", "failed", "not_started"])
            result = runner_group.collect(value, downloaded, "a" * 40)
        self.assertEqual([r["status"] for r in result["members"]], ["complete", "failed", "skipped"])
        self.assertFalse(result["complete"])

    def test_cross_version_metadata_or_missing_complete_payload_cannot_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            value, downloaded = self.prepare(Path(temp), ["complete", "complete"])
            p = Path(temp) / "samples/1/job.json"
            original = p.read_text(encoding="utf-8"); metadata = json.loads(original)
            for key, replacement in (("group_index", 0), ("apk_sha256", "f" * 64), ("runner_revision", "b" * 40)):
                p.write_text(json.dumps({**metadata, key: replacement}), encoding="utf-8")
                with self.subTest(key=key), self.assertRaises(ValueError): runner_group.collect(value, downloaded, "a" * 40)
            p.write_text(original, encoding="utf-8")
            downloaded["files"].remove(str(p))
            with self.assertRaises(ValueError): runner_group.collect(value, downloaded, "a" * 40)

    def test_checkpoint_crash_after_member_write_can_recover_verified_success(self):
        with tempfile.TemporaryDirectory() as temp:
            value, downloaded = self.prepare(Path(temp), ["complete"])
            p = Path(temp) / "group.json"
            receipt = json.loads(p.read_text(encoding="utf-8")); receipt["samples"][0]["status"] = "not_started"
            p.write_text(json.dumps(receipt), encoding="utf-8")
            self.assertTrue(runner_group.collect(value, downloaded, "a" * 40)["complete"])

    def test_success_cannot_contradict_source_proof(self):
        with tempfile.TemporaryDirectory() as temp:
            value, downloaded = self.prepare(Path(temp), ["complete"])
            p = Path(temp) / "samples/0/result.txt"
            result = json.loads(p.read_text(encoding="utf-8"))
            for changed in ({**result, "source_unchanged": False}, {**result, "sample": {**result["sample"], "sha256": "f" * 64}}):
                p.write_text(json.dumps(changed), encoding="utf-8")
                with self.assertRaises(ValueError): runner_group.collect(value, downloaded, "a" * 40)

    def test_group_job_result_exposes_failed_outputs_and_unambiguous_unicode_pages(self):
        import remote_artifacts
        import remote_mcp
        with tempfile.TemporaryDirectory() as temp:
            _, downloaded = self.prepare(Path(temp), ["complete", "failed"])
            p = Path(temp) / "samples/1/result.txt"; p.write_text("中文" * 5000, encoding="utf-8")
            downloaded.update(root=temp, cache_hit=True, artifact={}, integrity="verified", elapsed_ms=1, run_attempt=1)
            with patch.object(remote_mcp, "repository_report", return_value=None), \
                 patch.object(remote_mcp, "lookup", return_value={"status": "completed", "html_url": "https://example.invalid/run"}), \
                 patch.object(remote_artifacts, "get", return_value=downloaded):
                summary = json.loads(remote_mcp.job_result("a" * 32))
                self.assertTrue(summary["grouped"])
                self.assertEqual(len(summary["files"]), 5)
                first = json.loads(remote_mcp.job_result("a" * 32, sample_index=1))
                second = json.loads(remote_mcp.job_result("a" * 32, result_offset=8000, sample_index=1))
                self.assertEqual(first["result_page"]["next_offset"], 8000)
                self.assertIsNone(second["result_page"]["next_offset"])
                self.assertEqual(second["result_page"]["chars"], 2000)
                self.assertTrue(all(Path(p).parent.name == "1" for p in first["files"]))

    def test_unknown_group_post_and_explicit_failed_group_key_are_never_replayed(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(hostlab, "STATE", Path(temp)):
            posts = []
            def gh(args, data=None):
                if data is None: return json.dumps({"object": {"sha": "a" * 40}})
                posts.append(data); raise TimeoutError()
            def submit(lookup=lambda _: None, value=None):
                spec = value or payload()
                return remote_schedule.submit_group(spec["samples"], spec["request"], gh, lookup, lambda: [],
                    repository="owner/repo", workflow="host-analysis.yml", idempotency_key="group1")
            first = submit(); second = submit()
            self.assertIsNone(first["dispatched"])
            self.assertEqual(first["request_id"], second["request_id"])
            failed = submit(lambda _: {"status": "completed", "conclusion": "failure"})
            self.assertEqual(first["request_id"], failed["request_id"])
            changed = payload(); changed["samples"][0]["apk_sha256"] = "f" * 64
            with self.assertRaises(ValueError): submit(value=changed)
            self.assertEqual(len(posts), 1)
            self.assertEqual(posts[0]["inputs"]["operation"], "batch_group")


if __name__ == "__main__": unittest.main()
