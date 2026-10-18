"""Grouped runners retain every exact sample while overlapping bounded preparation."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import analysis_batch
import analysis_plan
import hostlab
import plan_ci
import remote_job
import runner_group
import runner_worker
import runner_resources


class RunnerWorkerTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch.object(hostlab, "STATE", self.root / "state").start()
        patch.dict(os.environ, {"HOSTLAB_RUNNER_REVISION": "c"*40, "GITHUB_SHA": "d"*40}, clear=True).start()
        patch("sys.stdout", new_callable=io.StringIO).start()
        self.request = {"backend": "dexsql", "timeout_seconds": 1, "tasks": [{"id": "info", "operation": "info"}]}
        self.paths, self.rows, self.samples = {}, [], []
        for index in range(4):
            code = 100 + index
            path = self.root / f"sample-{index}.apk"
            path.write_bytes(f"exact sample {index}".encode())
            sha = hostlab.digest(path)
            self.paths[code] = path
            self.rows.append({"version_code": code, "sha256": sha, "size": path.stat().st_size,
                "path": f"apks/tv.danmaku.bili/{code}/{sha}/base.apk"})
            self.samples.append({"version_code": code, "apk_sha256": sha, "sample_revision": "b"*40})
        self.payload = {"schema": 1, "request": self.request, "samples": self.samples}
        self.gate = patch.object(hostlab, "api_private", return_value=(None, "a"*40)).start()
        self.manifest = patch.object(hostlab, "manifest", return_value={"samples": self.rows}).start()
        self.fetch = patch.object(runner_worker.analyze, "fetch_sample", side_effect=self.fetch_fixture).start()
        self.execute = patch.object(analysis_batch, "execute", new_callable=AsyncMock,
            side_effect=self.execute_fixture).start()

    def fetch_fixture(self, row, repo, revision, *, timings):
        timings.update(download_ms=1.0, verify_ms=1.0, stage_ms=1.0, staged_cache_hit=False)
        return self.paths[row["version_code"]]

    async def execute_fixture(self, apk, request, *, roots, sample, resume=None, checkpoint=None):
        matches = hostlab.digest(apk) == sample["sha256"]
        return {"complete": matches, "tasks": [{"id": "info", "status": "complete"}],
            "source_unchanged": matches, "sample": sample,
            "backend_versions": {"dexsql": {"version": "fixture"}}}

    def group(self):
        return json.loads((hostlab.STATE / "remote-output/group.json").read_text(encoding="utf-8"))

    def job(self, index):
        return json.loads((hostlab.STATE / f"remote-output/samples/{index}/job.json").read_text(encoding="utf-8"))

    def result(self, index):
        return json.loads((hostlab.STATE / f"remote-output/samples/{index}/result.txt").read_text(encoding="utf-8"))

    def test_exact_members_share_gate_manifest_and_keep_independent_metadata(self):
        self.assertEqual(runner_worker.run(self.payload), 0)
        self.gate.assert_called_once_with(runner_worker.SAMPLE_REPOSITORY)
        self.manifest.assert_called_once_with(runner_worker.SAMPLE_REPOSITORY, "b"*40)
        self.assertEqual(self.fetch.call_count, 4)
        self.assertEqual(self.execute.await_count, 4)
        group = self.group()
        self.assertTrue(group["complete"])
        self.assertEqual([row["sample"] for row in group["samples"]], self.samples)
        self.assertEqual([row["status"] for row in group["samples"]], ["complete"]*4)
        self.assertEqual(sorted(group["processing_order"]), list(range(4)))
        for index, sample in enumerate(self.samples):
            job = self.job(index)
            self.assertEqual(job["operation"], "batch")
            self.assertEqual(job["group_index"], index)
            self.assertEqual(job["version_code"], sample["version_code"])
            self.assertEqual(job["apk_sha256"], sample["apk_sha256"])
            self.assertEqual(job["sample_revision"], sample["sample_revision"])
            self.assertEqual(job["request_sha256"], analysis_plan.fingerprint(self.request))
            self.assertEqual(job["runner_revision"], "c"*40)
            self.assertIn("runner_group.py", job["tools"])
            self.assertIn("runner_worker.py", job["tools"])
            self.assertTrue(job["complete"])
            self.assertTrue(self.result(index)["source_unchanged"])
            for key in ("group_fetch_started_ms", "group_fetch_finished_ms", "group_fetch_queue_ms",
                        "group_prefetch_ready_wait_ms", "analysis_ms"):
                self.assertGreaterEqual(job["phases"][key], 0)
        collected = runner_group.collect(self.payload, {"files": [str(path) for path in
            (hostlab.STATE / "remote-output").rglob("*") if path.is_file()]}, "c"*40)
        self.assertTrue(collected["complete"])

    def test_group_receipt_contains_all_not_started_before_any_network_call(self):
        def gate(repo):
            checkpoint = self.group()
            self.assertEqual([row["status"] for row in checkpoint["samples"]], ["not_started"]*4)
            self.manifest.assert_not_called()
            self.fetch.assert_not_called()
            return None, "a"*40

        self.gate.side_effect = gate
        self.assertEqual(runner_worker.run(self.payload), 0)

    def test_fetch_failure_does_not_lose_other_versions_or_leak_exception_message(self):
        def fetch(row, repo, revision, *, timings):
            if row["version_code"] == 101:
                raise OSError("Authorization fixture-sensitive-message")
            return self.fetch_fixture(row, repo, revision, timings=timings)

        self.fetch.side_effect = fetch
        self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual([row["status"] for row in self.group()["samples"]],
                         ["complete", "failed", "complete", "complete"])
        self.assertEqual(self.execute.await_count, 3)
        self.assertEqual(self.result(1)["error"], "OSError")
        self.assertNotIn("fixture-sensitive-message", json.dumps(self.result(1)))
        self.assertEqual(self.job(1)["group_index"], 1)

    def test_analysis_failure_is_local_to_one_member(self):
        async def execute(apk, request, *, roots, sample, resume=None, checkpoint=None):
            if sample["version_code"] == 101:
                raise RuntimeError("fixture-sensitive-analysis-message")
            return await self.execute_fixture(apk, request, roots=roots, sample=sample)

        self.execute.side_effect = execute
        self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual([row["status"] for row in self.group()["samples"]],
                         ["complete", "failed", "complete", "complete"])
        self.assertNotIn("fixture-sensitive-analysis-message", json.dumps(self.result(1)))
        self.assertEqual(self.execute.await_count, 4)

    def test_partial_analysis_is_not_promoted_to_complete(self):
        async def execute(apk, request, *, roots, sample, resume=None, checkpoint=None):
            result = await self.execute_fixture(apk, request, roots=roots, sample=sample)
            if sample["version_code"] == 102:
                result["complete"] = False
                result["tasks"][0]["status"] = "partial"
            return result

        self.execute.side_effect = execute
        self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual(self.group()["samples"][2]["status"], "failed")
        self.assertEqual(self.job(2)["exit_code"], 2)
        self.assertFalse(self.result(2)["complete"])

    def test_each_revision_manifest_is_resolved_once_and_bound_to_that_revision(self):
        self.samples[1]["sample_revision"] = "e"*40
        self.samples[3]["sample_revision"] = "e"*40
        self.assertEqual(runner_worker.run(self.payload), 0)
        self.assertEqual(self.manifest.call_count, 2)
        self.assertEqual({call.args[1] for call in self.manifest.call_args_list}, {"b"*40, "e"*40})
        for index, sample in enumerate(self.samples):
            self.assertEqual(self.job(index)["sample_revision"], sample["sample_revision"])

    def test_failed_manifest_does_not_block_unrelated_revision(self):
        self.samples[1]["sample_revision"] = "e"*40
        self.samples[3]["sample_revision"] = "e"*40

        def manifest(repo, revision):
            if revision == "e"*40:
                raise OSError("fixture-private-path")
            return {"samples": self.rows}

        self.manifest.side_effect = manifest
        self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual(self.fetch.call_count, 2)
        self.assertEqual([row["status"] for row in self.group()["samples"]],
                         ["complete", "failed", "complete", "failed"])

    def test_missing_exact_sample_fails_only_that_member(self):
        self.manifest.return_value = {"samples": self.rows[1:]}
        self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual(self.group()["samples"][0]["status"], "failed")
        self.assertEqual(self.fetch.call_count, 3)
        self.assertEqual(self.execute.await_count, 3)

    def test_private_repository_gate_failure_prevents_all_sample_access(self):
        self.gate.side_effect = RuntimeError("fixture-gate-detail")
        self.assertEqual(runner_worker.run(self.payload), 2)
        self.manifest.assert_not_called()
        self.fetch.assert_not_called()
        self.execute.assert_not_awaited()
        self.assertEqual([row["status"] for row in self.group()["samples"]], ["failed"]*4)
        for index in range(4):
            self.assertEqual(self.job(index)["apk_sha256"], self.samples[index]["apk_sha256"])
            self.assertNotIn("fixture-gate-detail", json.dumps(self.result(index)))

    def test_completed_prefetch_avoids_waiting_for_slow_first_version(self):
        second_analyzed = threading.Event()

        def fetch(row, repo, revision, *, timings):
            if row["version_code"] == 100 and not second_analyzed.wait(3):
                raise RuntimeError("head of line blocked faster member")
            return self.fetch_fixture(row, repo, revision, timings=timings)

        async def execute(apk, request, *, roots, sample, resume=None, checkpoint=None):
            if sample["version_code"] == 101:
                second_analyzed.set()
            return await self.execute_fixture(apk, request, roots=roots, sample=sample)

        self.fetch.side_effect, self.execute.side_effect = fetch, execute
        self.assertEqual(runner_worker.run(self.payload), 0)
        order = self.group()["processing_order"]
        self.assertLess(order.index(1), order.index(0))
        self.assertEqual([row["index"] for row in self.group()["samples"]], list(range(4)))

    def test_prefetch_peak_is_two_and_native_analyses_do_not_overlap(self):
        mutex = threading.Lock()
        first_pair = threading.Barrier(2)
        active = peak = native = native_peak = 0
        thread_ids = set()

        def fetch(row, repo, revision, *, timings):
            nonlocal active, peak
            with mutex:
                active += 1
                peak = max(peak, active)
                thread_ids.add(threading.get_ident())
            try:
                if row["version_code"] < 102:
                    first_pair.wait(timeout=3)
                time.sleep(0.01)
                return self.fetch_fixture(row, repo, revision, timings=timings)
            finally:
                with mutex:
                    active -= 1

        async def execute(apk, request, *, roots, sample, resume=None, checkpoint=None):
            nonlocal native, native_peak
            with mutex:
                native += 1
                native_peak = max(native_peak, native)
            try:
                return await self.execute_fixture(apk, request, roots=roots, sample=sample)
            finally:
                with mutex:
                    native -= 1

        self.fetch.side_effect, self.execute.side_effect = fetch, execute
        self.assertEqual(runner_worker.run(self.payload), 0)
        self.assertEqual(peak, 2)
        self.assertEqual(native_peak, 1)
        self.assertEqual(len(thread_ids), 2)

    def test_partial_checkpoint_is_saved_before_later_sample_finishes(self):
        saw_complete = threading.Event()

        async def execute(apk, request, *, roots, sample, resume=None, checkpoint=None):
            checkpoint = self.group()
            if any(row["status"] == "complete" for row in checkpoint["samples"]):
                saw_complete.set()
            return await self.execute_fixture(apk, request, roots=roots, sample=sample)

        self.execute.side_effect = execute
        self.assertEqual(runner_worker.run(self.payload), 0)
        self.assertTrue(saw_complete.is_set())

    def test_reporting_exception_still_leaves_failed_member_and_continues(self):
        original = remote_job.run_batch

        def batch(*args, **kwargs):
            if kwargs["group_index"] == 1:
                raise RuntimeError("fixture-private-report-path")
            return original(*args, **kwargs)

        with patch.object(remote_job, "run_batch", side_effect=batch):
            self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual(self.group()["samples"][1]["status"], "failed")
        self.assertEqual(self.job(1)["group_index"], 1)
        self.assertIn("runner_worker.py", self.job(1)["tools"])
        self.assertNotIn("fixture-private-report-path", json.dumps(self.result(1)))
        self.assertEqual(self.execute.await_count, 3)

    def test_unexpected_future_failure_is_local_and_does_not_abort_group(self):
        original = runner_worker.fetch

        def fetch(row, *args):
            if row["version_code"] == 102:
                raise RuntimeError("unexpected preparation wrapper failure")
            return original(row, *args)

        with patch.object(runner_worker, "fetch", side_effect=fetch):
            self.assertEqual(runner_worker.run(self.payload), 2)
        self.assertEqual([row["status"] for row in self.group()["samples"]],
                         ["complete", "complete", "failed", "complete"])

    def test_deadline_joins_running_downloads_and_does_not_claim_they_ended(self):
        entered, release = threading.Event(), threading.Event()

        def fetch(row, repo, revision, *, timings):
            entered.set()
            if not release.wait(3):
                raise RuntimeError("test fetch release missing")
            return self.fetch_fixture(row, repo, revision, timings=timings)

        self.fetch.side_effect = fetch
        with patch.object(runner_worker, "MAX_GROUP_SECONDS", 0.04), ThreadPoolExecutor(max_workers=1) as pool:
            running = pool.submit(runner_worker.run, self.payload)
            try:
                self.assertTrue(entered.wait(2))
                deadline = time.monotonic() + 2
                while not self.group()["deadline_exhausted"] and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(self.group()["deadline_exhausted"])
                self.assertFalse(running.done(), "running downloads must be joined before final return")
                self.execute.assert_not_awaited()
            finally:
                release.set()
            self.assertEqual(running.result(timeout=3), 2)
        self.assertEqual([row["status"] for row in self.group()["samples"]], ["not_started"]*4)
        self.assertFalse(self.group()["complete"])
        self.assertEqual(self.fetch.call_count, 2)

    def test_invalid_group_rejected_before_network_or_output(self):
        malformed = deepcopy(self.payload)
        malformed["samples"] *= 2
        with self.assertRaises(ValueError):
            runner_worker.run(malformed)
        self.gate.assert_not_called()
        self.fetch.assert_not_called()
        self.assertFalse(hostlab.STATE.exists())

    def adaptive_payload(self):
        return {**self.payload, "schema": 2, "execution": {"mode": "adaptive-v1", "prefetch_max": 2}}

    def test_adaptive_twelve_members_keep_exact_proofs_and_execution_identity(self):
        for index in range(4, 12):
            code = 100+index
            path = self.root / f"sample-{index}.apk"
            path.write_bytes(f"exact sample {index}".encode())
            sha = hostlab.digest(path)
            self.paths[code] = path
            self.rows.append({"version_code": code, "sha256": sha, "size": path.stat().st_size,
                "path": f"apks/tv.danmaku.bili/{code}/{sha}/base.apk"})
            self.samples.append({"version_code": code, "apk_sha256": sha, "sample_revision": "b"*40})
        payload = self.adaptive_payload()
        self.assertEqual(runner_worker.run(payload), 0)
        self.assertEqual(self.execute.await_count, 12)
        self.assertEqual(self.group()["execution"], payload["execution"])
        self.assertLessEqual((hostlab.STATE / "remote-output/group.json").stat().st_size, 65536)
        for index in range(12):
            self.assertEqual(self.job(index)["execution_sha256"], runner_group.execution_fingerprint(payload))
            self.assertIn("group_analysis_started_ms", self.job(index)["phases"])
            self.assertIn("group_analysis_finished_ms", self.job(index)["phases"])
        files = {"files": [str(path) for path in (hostlab.STATE / "remote-output").rglob("*") if path.is_file()]}
        self.assertTrue(runner_group.collect(payload, files, "c"*40)["complete"])

    def test_both_policies_write_bounded_same_sampler_artifacts(self):
        self.assertEqual(runner_worker.run(self.payload), 0)
        raw = (hostlab.STATE / "remote-output/resources.json").read_bytes()
        artifact = json.loads(raw)
        self.assertEqual(artifact["schema"], 1)
        self.assertEqual(artifact["summary"]["interval_seconds"], 0.5)
        self.assertLessEqual(len(raw), 1024**2)
        self.assertLessEqual(len(artifact["samples"]), 7200)
        self.assertIn("sampled_tree_rss_peak_bytes", self.group()["resources"])

    def test_no_disk_capacity_leaves_members_unstarted_with_reason(self):
        with patch.object(runner_worker.shutil, "disk_usage", return_value=SimpleNamespace(free=1)):
            self.assertEqual(runner_worker.run(self.adaptive_payload()), 2)
        self.fetch.assert_not_called()
        self.execute.assert_not_awaited()
        self.assertFalse(self.group()["deadline_exhausted"])
        self.assertEqual([row["status"] for row in self.group()["samples"]], ["not_started"]*4)
        self.assertTrue(all(row["reason"] == "disk_capacity" for row in self.group()["samples"]))

    def test_fresh_disk_check_reserves_inflight_inputs_before_second_admission(self):
        mutex = threading.Lock()
        active = peak = 0

        def fetch(row, repo, revision, *, timings):
            nonlocal active, peak
            with mutex:
                active += 1; peak = max(peak, active)
            try:
                time.sleep(0.01)
                return self.fetch_fixture(row, repo, revision, timings=timings)
            finally:
                with mutex:
                    active -= 1

        self.fetch.side_effect = fetch
        size = self.rows[0]["size"]
        free = 512*1024**2+3*size
        with patch.object(runner_worker.shutil, "disk_usage", return_value=SimpleNamespace(free=free)) as disk:
            self.assertEqual(runner_worker.run(self.payload), 0)
        self.assertEqual(peak, 1)
        self.assertGreaterEqual(disk.call_count, 4)
        self.assertTrue(all("reason" not in row for row in self.group()["samples"]))
        self.assertTrue(any(event["inputs"]["reserved_download_bytes"] > 0 for event in self.group()["prefetch_decisions"]))

    def test_resource_failures_do_not_change_member_results_or_leave_threads(self):
        for method in ("start", "set_phase", "snapshot", "summary", "stop"):
            with self.subTest(method=method), patch.object(runner_resources.Sampler, method,
                    side_effect=RuntimeError("fixture-sensitive-resource-path")):
                self.assertEqual(runner_worker.run(self.adaptive_payload()), 0)
                self.assertIn("RuntimeError", self.group()["resources"]["telemetry_errors"])
                self.assertNotIn("fixture-sensitive-resource-path", json.dumps(self.group()))
                self.assertFalse(any(thread.name == "hostlab-resources" and thread.is_alive()
                                     for thread in threading.enumerate()))

    def test_partial_sampler_start_failure_still_stops_real_monitor(self):
        original = runner_resources.Sampler.start

        def partial_start(sampler):
            original(sampler)
            raise RuntimeError("failure after monitor started")

        with patch.object(runner_resources.Sampler, "start", partial_start):
            self.assertEqual(runner_worker.run(self.payload), 0)
        self.assertFalse(any(thread.name == "hostlab-resources" and thread.is_alive()
                             for thread in threading.enumerate()))

    def test_unexpected_group_interrupt_still_stops_sampler(self):
        self.gate.side_effect = KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            runner_worker.run(self.payload)
        self.assertFalse(any(thread.name == "hostlab-resources" and thread.is_alive()
                             for thread in threading.enumerate()))

    def test_maximum_receipt_decisions_remain_below_collector_budget(self):
        sample = {"ts_ms": 1234, "cpu_usage_fraction": 0.99,
            "memory_available_bytes": 1000000000, "memory_limit_bytes": 8000000000,
            "disk_free_bytes": 10000000000, "psi_io_some_fraction": 0.15}
        decision = runner_resources.AdaptivePrefetch().decide(sample, phase="processing", next_size=1024**3, inflight=2)
        state = {"samples": [{"sample": self.samples[index % 4], "index": index, "status": "complete"} for index in range(12)],
            "sample_timings": [{"index": index, **{f"metric_{i}": 123456.789 for i in range(18)}} for index in range(12)],
            "resources": runner_resources.Sampler().summary(), "prefetch_decisions_omitted": 0,
            "prefetch_decisions": [{"index": index % 12, **deepcopy(decision)} for index in range(48)]}
        runner_worker.bound_decisions(state)
        self.assertLessEqual(len(json.dumps(state, ensure_ascii=False, indent=2).encode())+1, 65536)
        self.assertLessEqual(len(state["prefetch_decisions"]), 48)
        self.assertGreater(state["prefetch_decisions_omitted"], 0)


class GroupDispatcherTest(unittest.TestCase):
    def payload(self, backend="dexsql"):
        return {"schema": 1, "request": {"backend": backend, "tasks": [{"id": "a", "operation": "info"}]},
            "samples": [{"version_code": 100, "apk_sha256": "a"*64, "sample_revision": "b"*40}]}

    def env(self, payload):
        return {"HOSTLAB_VERSION": "100", "HOSTLAB_OPERATION": "batch_group", "HOSTLAB_ARGUMENT": json.dumps(payload),
                "HOSTLAB_RUNNER_REVISION": "c"*40, "HOSTLAB_MAX_CELL_CHARS": "300"}

    def test_dispatch_checks_exact_checkout_then_enters_group_worker(self):
        payload = self.payload()
        with patch.dict(os.environ, self.env(payload), clear=True), \
             patch.object(remote_job.subprocess, "check_output", return_value="c"*40+"\n"), \
             patch.object(runner_worker, "run", return_value=0) as worker, \
             patch.object(hostlab, "api_private") as gate:
            self.assertEqual(remote_job.main(), 0)
        worker.assert_called_once()
        self.assertEqual(worker.call_args.args[0], runner_group.validate(payload))
        gate.assert_not_called()

    def test_mismatched_compatibility_version_or_checkout_never_starts_worker(self):
        for bad_version, observed in (("101", "c"*40), ("100", "e"*40)):
            env = self.env(self.payload())
            env["HOSTLAB_VERSION"] = bad_version
            with self.subTest(version=bad_version, observed=observed), patch.dict(os.environ, env, clear=True), \
                 patch.object(remote_job.subprocess, "check_output", return_value=observed), \
                 patch.object(runner_worker, "run") as worker, self.assertRaises(RuntimeError):
                remote_job.main()
            worker.assert_not_called()

    def test_group_dependency_subset_matches_legacy_batch_and_preserves_sqlite(self):
        for backend in ("dexsql", "sqlite", "auto"):
            payload = self.payload(backend)
            group = plan_ci.requirements("batch_group", json.dumps(payload))
            batch = plan_ci.requirements("batch", json.dumps(payload["request"]))
            self.assertEqual(group, batch)
            self.assertEqual(group["needs_java"], "false")
        self.assertEqual(plan_ci.requirements("batch_group", json.dumps(self.payload()))["requirements"],
                         "requirements-query.txt")
        self.assertEqual(plan_ci.requirements("batch_group", json.dumps(self.payload("sqlite")))["requirements"],
                         "requirements.txt")


if __name__ == "__main__":
    unittest.main()
