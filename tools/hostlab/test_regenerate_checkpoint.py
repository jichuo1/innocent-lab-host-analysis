"""Regeneration restores verified frozen bytes, never an APK or a new DEX scan."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import analyze
import hostlab
import plan_ci
import priority_analysis
import regenerate_report as regen
import remote_artifacts
import snapshot_transport
import source_snapshot
from test_source_runner import frozen_source, sample, summary

VERIFIED_ARTIFACT = regen.verified_artifact


class RegenerateCheckpointTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ctx, self.binding = frozen_source("current")
        self.data = summary(self.ctx, self.binding)
        self.data["analysis_status"] = "NO_STATIC_DRIFT_FOUND"
        self.data["page_path_matrix"] = {"comment": {"paths": {}, "status": "installer_and_runtime_validation_required"}}
        self.target = {"sample": sample(), "rule_sha256": "c" * 64,
            "page_path_matrix": self.data["page_path_matrix"], "unknown_families": [], "unregistered_protocols": []}
        self.job = {"version_code": 2, "operation": "multipath_audit", "exit_code": 0,
                    "apk_sha256": "a" * 64, "sample_revision": "b" * 40}
        self.source = self.root / "artifact/remote-output"
        self.source.mkdir(parents=True)
        for name, value in (("priority-summary.json", self.data), ("priority-target.json", self.target), ("job.json", self.job)):
            self.save(self.source / name, value)
        (self.source / "priority-report.md").write_text(
            "static\n分析结果：NO_STATIC_DRIFT_FOUND\n\n## 未归类的源码多路径候选\n\n- stale.kt\n\n## 未覆盖边界\nunknown\n"
            "# AI 分析未完成\nold failure\n# AI 适配分析\nold result", encoding="utf-8")
        self.run = {"id": 987, "run_attempt": 1, "head_sha": "d" * 40,
                    "display_title": "hostlab-" + "e" * 32, "status": "completed", "conclusion": "failure"}
        self.downloaded = {"root": str(self.source.parent), "files": [str(p) for p in self.source.iterdir()],
            "artifact": {"id": 42, "name": "host-analysis-987", "digest": "sha256:" + "f" * 64,
                         "size_in_bytes": 123}, "cache_hit": True, "integrity": "fixture_verified"}
        self.patches = [patch.object(hostlab, "STATE", self.root / "state"),
            patch.object(hostlab, "CONFIG", self.root / "state/config.json"),
            patch.dict("os.environ", {"HOSTLAB_ARGUMENT": "987", "HOSTLAB_VERSION": "2"}, clear=True),
            patch.object(regen, "verified_artifact", return_value=(self.run, self.downloaded)),
            patch.object(snapshot_transport, "load_for_analysis", return_value=(self.ctx, self.binding)),
            patch.object(analyze, "fetch_sample", side_effect=AssertionError("APK fetch forbidden")),
            patch.object(priority_analysis, "scan_apk", side_effect=AssertionError("APK scan forbidden"))]
        self.started = [item.start() for item in self.patches]
        for item in self.patches:
            self.addCleanup(item.stop)

    def save(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def restored(self):
        return json.loads((hostlab.STATE / "remote-output/priority-summary.json").read_text(encoding="utf-8"))

    def test_number_and_bounded_explicit_checkpoint_options(self):
        self.assertEqual(regen.argument("987"), {"static_run": 987, "resume_unknown": False})
        self.assertTrue(regen.argument('{"static_run":987,"checkpoint_run":988,"resume_unknown":true}')["resume_unknown"])
        for value in ({"static_run": True}, {"static_run": 1, "resume_unknown": 1},
                      {"static_run": 1, "checkpoint_run": "2"}, {"static_run": 1, "extra": True},
                      {"static_run": 1, "recovery_policy": "extended-v1"},
                      {"static_run": 1, "checkpoint_run": 2, "recovery_policy": "extended-v2"},
                      {"static_run": 1, "checkpoint_run": 2, "recovery_policy": True}):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                regen.argument(json.dumps(value))

    def test_explicit_extended_policy_restores_only_verified_public_recovery_inputs(self):
        checkpoint_files = self.checkpoint()
        restore = Mock(return_value={"parent_run": 988, "checkpoint_sha256": "a"*64, "evidence_sha256": "b"*64})
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint_files if run == 988 else self.downloaded)), \
             patch.dict("sys.modules", {"ai_recovery": SimpleNamespace(restore_inputs=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988,"recovery_policy":"extended-v1"}'}):
            regen.main()
        restore.assert_called_once_with(hostlab.STATE/"remote-output", checkpoint_files["files"], 988)
        self.assertEqual(self.restored()["ai_recovery_policy"], "extended-v1")
        self.assertEqual(self.restored()["ai_recovery_inputs"]["parent_run"], 988)

    def test_policy_from_old_summary_does_not_implicitly_authorize_extension(self):
        self.data.update(ai_recovery_policy="extended-v1", ai_recovery_inputs={"untrusted": True})
        self.save(self.source/"priority-summary.json", self.data)
        regen.main()
        self.assertNotIn("ai_recovery_policy", self.restored())
        self.assertNotIn("ai_recovery_inputs", self.restored())

    def test_initial_multipath_checkpoint_derives_manifest_only_from_its_own_verified_artifact(self):
        restore = Mock(return_value={"parent_run": 987, "checkpoint_sha256": "a"*64, "evidence_sha256": "b"*64})
        with patch.dict("sys.modules", {"ai_recovery": SimpleNamespace(restore_inputs=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":987,"recovery_policy":"extended-v1"}'}):
            regen.main()
        self.assertTrue(self.restored()["ai_no_apk_access"])
        self.assertEqual(self.restored()["checkpoint_from_run"], 987)
        self.assertTrue((hostlab.STATE/"remote-output/static-manifest.json").is_file())
        restore.assert_called_once()

    def test_other_run_cannot_bootstrap_a_missing_checkpoint_manifest(self):
        with patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988,"recovery_policy":"extended-v1"}'}):
            with self.assertRaisesRegex(RuntimeError, "manifest is missing"):
                regen.main()

    def test_completion_policy_is_explicit_and_uses_its_own_verified_parent(self):
        checkpoint_files = self.checkpoint()
        restore = Mock(return_value={"parent_run": 988, "checkpoint_sha256": "a"*64, "evidence_sha256": "b"*64})
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint_files if run == 988 else self.downloaded)), \
             patch.dict("sys.modules", {"ai_recovery": SimpleNamespace(restore_inputs=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988,"recovery_policy":"completion-v2"}'}):
            regen.main()
        restore.assert_called_once_with(hostlab.STATE/"remote-output", checkpoint_files["files"], 988, policy="completion-v2")
        self.assertEqual(self.restored()["ai_recovery_policy"], "completion-v2")
        with self.assertRaises(RuntimeError):
            regen.argument('{"static_run":987,"recovery_policy":"completion-v2"}')

    def test_final_completion_policy_uses_its_own_explicit_verified_parent(self):
        checkpoint_files = self.checkpoint()
        restore = Mock(return_value={"parent_run": 988, "checkpoint_sha256": "a"*64, "evidence_sha256": "b"*64})
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint_files if run == 988 else self.downloaded)), \
             patch.dict("sys.modules", {"ai_recovery": SimpleNamespace(restore_inputs=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988,"recovery_policy":"completion-v3"}'}):
            regen.main()
        restore.assert_called_once_with(hostlab.STATE/"remote-output", checkpoint_files["files"], 988, policy="completion-v3")
        self.assertEqual(self.restored()["ai_recovery_policy"], "completion-v3")
        for value in (None, {}, [], "completion-v4"):
            with self.assertRaises(RuntimeError):
                regen.argument(json.dumps({"static_run": 987, "checkpoint_run": 988, "recovery_policy": value}))

    def test_current_restore_metrics_do_not_relabel_the_original_apk_scan(self):
        original = {**self.job, "command": ["old-apk-auditor"], "phases": {"analysis_ms": 319000},
                    "preparation": {"requirements": "requirements.txt", "elapsed_ms": 5000}}
        self.save(self.source / "job.json", original)
        current = {"requirements": "requirements-query.txt", "elapsed_ms": 1700, "cache_hit": True}
        self.save(hostlab.STATE / "preparation.json", current)
        regen.main()
        job = json.loads((hostlab.STATE / "remote-output/job.json").read_text())
        self.assertEqual(job["scope"], "verified_static_restore_and_ai_only")
        self.assertFalse(job["apk_analysis_rerun"])
        self.assertEqual(job["preparation"], current)
        self.assertNotIn("command", job)
        self.assertNotIn("analysis_ms", job["phases"])
        self.assertGreaterEqual(job["phases"]["restore_static_and_source_ms"], 0)
        previous = job["previous_provenance"]["static_job_performance"]
        self.assertEqual(previous["phases"], original["phases"])
        self.assertEqual(previous["command"], original["command"])

    def test_failed_ai_run_reuses_successful_static_job_and_keeps_exact_bytes(self):
        original = (self.source / "priority-target.json").read_bytes()
        regen.main()
        data = self.restored()
        self.assertTrue(data["ai_no_apk_access"])
        self.assertFalse(data["ai_resume_unknown"])
        self.assertEqual(data["static_evidence_run"], 987)
        self.assertEqual(data["page_path_matrix"], self.data["page_path_matrix"])
        self.assertEqual((hostlab.STATE / "remote-output/priority-target.json").read_bytes(), original)
        manifest = hostlab.STATE / "remote-output/static-manifest.json"
        self.assertEqual(hostlab.digest(manifest), data["static_manifest_sha256"])
        self.assertEqual(json.loads(manifest.read_text())["source_run"], {"id": 987, "run_attempt": 1, "head_sha": "d" * 40})
        self.assertIn("source_contract_review_required", data["review_reasons"])
        report = (hostlab.STATE / "remote-output/priority-report.md").read_text(encoding="utf-8")
        self.assertNotIn("old failure", report)
        self.assertNotIn("old result", report)
        self.assertNotIn("stale.kt", report)
        analyze.fetch_sample.assert_not_called()
        priority_analysis.scan_apk.assert_not_called()

    def test_static_manifest_is_stable_across_cache_restore_and_new_source(self):
        regen.main()
        first = self.restored()["static_manifest_sha256"]
        new_ctx, new_binding = frozen_source("new source")
        with patch.object(snapshot_transport, "load_for_analysis", return_value=(new_ctx, new_binding)), \
             patch.dict("os.environ", {"HOSTLAB_MODULE_SOURCE": json.dumps(new_binding)}):
            regen.main()
        self.assertEqual(self.restored()["static_manifest_sha256"], first)
        self.assertTrue(self.restored()["source_rebound_for_review"])
        self.assertEqual(self.restored()["source_snapshot"]["binding"], new_binding)

    def test_target_job_and_matrix_identity_fail_before_source_or_ai(self):
        cases = [("priority-target.json", {**self.target, "sample": {**sample(), "sha256": "f" * 64}}),
                 ("job.json", {**self.job, "sample_revision": "f" * 40}),
                 ("job.json", {**self.job, "exit_code": True}),
                 ("priority-target.json", {**self.target, "page_path_matrix": {}})]
        for name, invalid in cases:
            original = (self.source / name).read_bytes()
            self.save(self.source / name, invalid)
            with self.subTest(name=name), self.assertRaises(RuntimeError):
                regen.main()
            (self.source / name).write_bytes(original)
        snapshot_transport.load_for_analysis.assert_not_called()

    def test_baseline_rules_or_sample_mismatch_is_rejected(self):
        baseline = {**sample(), "version_code": 1, "sha256": "b" * 64}
        self.save(self.source / "priority-summary.json", {**self.data, "baseline": baseline})
        path = self.source / "priority-baseline.json"
        self.downloaded["files"].append(str(path))
        for value in ({"sample": baseline, "rule_sha256": "f" * 64},
                      {"sample": sample(), "rule_sha256": "c" * 64}):
            self.save(path, value)
            with self.assertRaisesRegex(RuntimeError, "baseline"):
                regen.main()

    def checkpoint(self):
        regen.main()
        folder = self.root / "checkpoint/remote-output"
        folder.mkdir(parents=True)
        for name in ("priority-summary.json", "static-manifest.json"):
            (folder / name).write_bytes((hostlab.STATE / "remote-output" / name).read_bytes())
        self.save(folder / "ai-checkpoint.json", {"schema": 1, "units": []})
        return {"root": str(folder.parent), "files": [str(p) for p in folder.iterdir()]}

    def test_checkpoint_restoration_is_verified_and_unknown_retry_is_explicit(self):
        checkpoint = self.checkpoint()
        restore = Mock()
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint if run == 988 else self.downloaded)), \
             patch.dict("sys.modules", {"ai_checkpoint": SimpleNamespace(restore_checkpoint=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988,"resume_unknown":true}'}):
            regen.main()
        restore.assert_called_once_with(hostlab.STATE / "remote-output", checkpoint["files"])
        self.assertTrue(self.restored()["ai_resume_unknown"])
        self.assertEqual(self.restored()["checkpoint_from_run"], 988)

    def test_checkpoint_default_uses_its_pinned_source_instead_of_static_run_source(self):
        checkpoint = self.checkpoint()
        context, binding = frozen_source("checkpoint-current-source")
        metadata = source_snapshot.public_context(context, binding)
        metadata["freshness"] = "ancestor_annotation_preserved"
        summary_path = Path(next(path for path in checkpoint["files"] if Path(path).name == "priority-summary.json"))
        checkpoint_summary = json.loads(summary_path.read_text(encoding="utf-8"))
        checkpoint_summary["source_snapshot"] = metadata
        self.save(summary_path, checkpoint_summary)
        restore = Mock()
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint if run == 988 else self.downloaded)), \
             patch.object(snapshot_transport, "load_for_analysis", return_value=(context, binding)) as load, \
             patch.dict("sys.modules", {"ai_checkpoint": SimpleNamespace(restore_checkpoint=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988}'}):
            regen.main()
        self.assertEqual(json.loads(load.call_args.args[0]), binding)
        self.assertEqual(self.restored()["source_snapshot"], metadata)
        self.assertEqual(self.restored()["source_selection"], "checkpoint")
        self.assertEqual(self.restored()["freshness"], "checkpoint_resume")
        self.assertEqual(self.restored()["previous_provenance"]["source_snapshot"]["binding"], self.binding)
        self.assertEqual(self.restored()["previous_provenance"]["checkpoint_source_snapshot"]["binding"], binding)
        job = json.loads((hostlab.STATE/"remote-output/job.json").read_text(encoding="utf-8"))
        self.assertEqual(job["source_selection"], "checkpoint")
        self.assertEqual(job["freshness"], "checkpoint_resume")
        restore.assert_called_once()

    def test_explicit_source_conflict_is_not_silently_replaced_with_checkpoint_source(self):
        checkpoint = self.checkpoint()
        context, binding = frozen_source("different-checkpoint-source")
        metadata = source_snapshot.public_context(context, binding)
        summary_path = Path(next(path for path in checkpoint["files"] if Path(path).name == "priority-summary.json"))
        checkpoint_summary = json.loads(summary_path.read_text(encoding="utf-8"))
        checkpoint_summary["source_snapshot"] = metadata
        self.save(summary_path, checkpoint_summary)
        restore = Mock()
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint if run == 988 else self.downloaded)), \
             patch.dict("sys.modules", {"ai_checkpoint": SimpleNamespace(restore_checkpoint=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988}',
                                       "HOSTLAB_MODULE_SOURCE": json.dumps(self.binding)}), \
             self.assertRaisesRegex(RuntimeError, "Checkpoint source binding differs"):
            regen.main()
        self.assertEqual(json.loads(snapshot_transport.load_for_analysis.call_args.args[0]), self.binding)
        restore.assert_not_called()

    def test_explicit_matching_checkpoint_source_keeps_explicit_selection(self):
        checkpoint = self.checkpoint()
        restore = Mock()
        with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                checkpoint if run == 988 else self.downloaded)), \
             patch.dict("sys.modules", {"ai_checkpoint": SimpleNamespace(restore_checkpoint=restore)}), \
             patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988}',
                                       "HOSTLAB_MODULE_SOURCE": json.dumps(self.binding)}):
            regen.main()
        self.assertEqual(self.restored()["source_selection"], "explicit")
        self.assertEqual(self.restored()["source_snapshot"]["binding"], self.binding)
        self.assertEqual(self.restored()["freshness"], "checkpoint_resume")
        restore.assert_called_once()

    def test_checkpoint_static_or_source_drift_rejects_before_restore(self):
        checkpoint = self.checkpoint()
        snapshot_transport.load_for_analysis.reset_mock()
        restore = Mock()
        checkpoint_summary = Path(next(p for p in checkpoint["files"] if Path(p).name == "priority-summary.json"))
        original = json.loads(checkpoint_summary.read_text(encoding="utf-8"))
        for changed in ({**original, "static_manifest_sha256": "f" * 64},
                        {**original, "source_snapshot": {"binding": {}}}):
            self.save(checkpoint_summary, changed)
            with patch.object(regen, "verified_artifact", side_effect=lambda run: (self.run,
                    checkpoint if run == 988 else self.downloaded)), \
                 patch.dict("sys.modules", {"ai_checkpoint": SimpleNamespace(restore_checkpoint=restore)}), \
                 patch.dict("os.environ", {"HOSTLAB_ARGUMENT": '{"static_run":987,"checkpoint_run":988}'}), \
                 self.assertRaisesRegex(RuntimeError, "Checkpoint"):
                regen.main()
        restore.assert_not_called()
        snapshot_transport.load_for_analysis.assert_not_called()

    def test_copy_interruption_preserves_prior_file_and_retry_recovers(self):
        target = self.root / "copy/target.json"
        target.parent.mkdir()
        target.write_bytes(b"prior")
        with patch.object(regen.shutil, "copyfile", return_value=None), self.assertRaisesRegex(RuntimeError, "changed"):
            regen.copy_verified(self.source / "priority-target.json", target)
        self.assertEqual(target.read_bytes(), b"prior")
        self.assertEqual(list(target.parent.glob(".restore-*")), [])
        regen.copy_verified(self.source / "priority-target.json", target)
        self.assertEqual(target.read_bytes(), (self.source / "priority-target.json").read_bytes())

    def test_artifact_cache_accepts_failed_overall_run_and_rejects_wrong_run(self):
        with patch.object(regen, "gh", return_value=json.dumps(self.run)), \
             patch.object(remote_artifacts, "get", return_value=self.downloaded) as cached:
            run, result = VERIFIED_ARTIFACT(987)
            self.assertEqual(run["conclusion"], "failure")
            self.assertIs(result, self.downloaded)
            cached.assert_called_once_with(snapshot_transport.ANALYSIS_REPO, "e" * 32, self.run, regen.gh, profile="frozen-report-v1")
            with self.assertRaises(RuntimeError):
                VERIFIED_ARTIFACT(988)

    def test_regeneration_does_not_prepare_java_jadx_or_androguard(self):
        planned = plan_ci.requirements("regenerate_ai", "987")
        self.assertEqual(planned["requirements"], "requirements-query.txt")
        self.assertEqual(planned["needs_java"], "false")
        self.assertEqual(planned["needs_dexsql"], "false")
        text = Path(regen.__file__).with_name("host-analysis.yml").read_text(encoding="utf-8")
        jadx_condition = text.split("- name: Download verified JADX", 1)[1].split("run:", 1)[0]
        self.assertNotIn("regenerate_ai", jadx_condition)


class PinnedCacheRepairTest(unittest.TestCase):
    def test_corrupt_cache_refetches_exact_binding_once_and_reuses_repaired_bytes(self):
        ctx, binding = frozen_source("repair")
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab, "STATE", Path(folder)):
            cached = snapshot_transport.cache_snapshot(ctx, binding)
            cached.write_text("{}", encoding="utf-8")
            remote = Path(folder) / "download.json"
            remote.write_bytes(source_snapshot.serialize(ctx))
            with patch.object(hostlab, "api_private", return_value=(None, "f" * 40)) as gate, \
                 patch("huggingface_hub.hf_hub_download", return_value=str(remote)) as download:
                self.assertEqual(snapshot_transport.load_pinned(binding), ctx)
                self.assertEqual(snapshot_transport.load_pinned(binding), ctx)
            gate.assert_called_once_with(snapshot_transport.SOURCE_REPO)
            download.assert_called_once_with(repo_id=snapshot_transport.SOURCE_REPO, repo_type="dataset",
                filename=binding["path"], revision=binding["revision"], token=True, force_download=True)

    def test_bad_remote_repair_is_not_retried_or_replaced_with_latest(self):
        ctx, binding = frozen_source("repair")
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab, "STATE", Path(folder)):
            cached = snapshot_transport.cache_snapshot(ctx, binding)
            cached.write_text("{}", encoding="utf-8")
            remote = Path(folder) / "bad.json"
            remote.write_text("{}", encoding="utf-8")
            with patch.object(hostlab, "api_private", return_value=(None, "f" * 40)), \
                 patch("huggingface_hub.hf_hub_download", return_value=str(remote)) as download, \
                 patch.object(snapshot_transport, "resolve_published", side_effect=AssertionError("latest forbidden")):
                with self.assertRaises(ValueError):
                    snapshot_transport.load_pinned(binding)
            self.assertEqual(download.call_count, 1)


if __name__ == "__main__":
    unittest.main()
