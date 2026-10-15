"""Optional shared runners preserve exact version identities and paid retry boundaries."""
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

import analysis_plan
import hostlab
import version_matrix as matrix


def samples(count):
    return [{"version_code": 9000000+i, "apk_sha256": format(i+1, "064x"),
             "sample_revision": "c"*40} for i in range(count)]


def request():
    return {"backend": "dexsql", "tasks": [{"id": "feature", "operation": "locate", "name": "getUrlsMap"}]}


class GroupMatrixTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        p = patch.object(hostlab, "STATE", self.root); p.start(); self.addCleanup(p.stop)
        self.head = "a"*40
        self.jobs = {}; self.keys = {}; self.calls = []; self.outcomes = {}
        p = patch.object(matrix.remote_schedule, "submit_group", side_effect=self.submit)
        p.start(); self.addCleanup(p.stop)

    def gh(self, *args, **kwargs):
        return json.dumps({"object": {"sha": self.head}})

    def create(self, count=8, **kwargs):
        return matrix.create(samples(count), request(), self.gh, repository="owner/repo",
                             runner_batch_size=kwargs.pop("runner_batch_size", 2), **kwargs)

    def submit(self, rows, spec, gh, lookup, runs, **kwargs):
        self.calls.append({**kwargs, "samples": rows})
        key = kwargs["idempotency_key"]
        if key in self.keys:
            rid = self.keys[key]; run = self.jobs[rid]
            return {"request_id": rid, "status": run["status"], "conclusion": run["conclusion"], "reused": True}
        rid = format(len(self.keys)+1, "032x"); self.keys[key] = rid
        self.jobs[rid] = {"id": len(self.keys), "status": "queued", "conclusion": None,
                          "html_url": "https://example.invalid/"+rid, "head_sha": "a"*40,
                          "run_attempt": 1, "display_title": "hostlab-"+rid}
        return {"request_id": rid, "status": "submitted", "reused": False}

    def collect(self, group, payload, run):
        statuses = self.outcomes.get(group["group_id"], ["complete"]*len(payload["samples"]))
        return {"members": [{"index": i, "sample": sample, "status": statuses[i], "files": [],
                             **({"reason": "runner_interrupted_before_member"} if statuses[i] == "skipped" else {})}
                            for i, sample in enumerate(payload["samples"])],
                "complete": all(s == "complete" for s in statuses)}

    def advance(self, identifier, **kwargs):
        return matrix.advance(identifier, self.gh, self.jobs.get, lambda: [], repository="owner/repo",
            workflow="host-analysis.yml", collect_group=kwargs.pop("collect_group", self.collect), **kwargs)

    def complete(self, conclusion="success"):
        for job in self.jobs.values():
            job.update(status="completed", conclusion=conclusion)

    def test_default_definition_and_saved_schema_remain_compatible(self):
        old = matrix.definition(samples(2), request())
        self.assertNotIn("runner_batch_size", old)
        self.assertEqual(old, matrix.definition(samples(2), request(), runner_batch_size=1))
        created = self.create(count=2, runner_batch_size=1)
        saved = matrix.load(created["matrix_id"])
        self.assertEqual(saved["schema"], 1)
        self.assertNotIn("groups", saved)
        for size in (0, 5, True):
            with self.subTest(size=size), self.assertRaises(ValueError):
                matrix.plan(samples(2), request(), runner_batch_size=size)

    def test_groups_are_immutable_and_use_physical_slots(self):
        created = self.create(count=9, max_parallel=2, runner_batch_size=4)
        first = self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys), 2)
        self.assertEqual(first["physical_inflight"], 2)
        self.assertEqual(first["counts"], {"submitted": 8, "queued_local": 1})
        self.assertEqual(first["physical_job_count"], 3)
        self.assertEqual(len({e["request_id"] for e in first["entries"][:4]}), 1)
        self.complete(); self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys), 3)
        self.complete(); final = self.advance(created["matrix_id"])
        self.assertTrue(final["complete"])
        self.assertEqual(final["peak_inflight"], 2)

    def test_group_and_member_topology_tampering_fails_before_dispatch(self):
        for kind in ("indices", "group_key", "member_index", "physical_request"):
            created = self.create(count=3)
            value = matrix.load(created["matrix_id"])
            if kind == "indices": value["groups"][0]["sample_indices"] = [1, 0]
            elif kind == "group_key": value["groups"][0]["dispatch_key"] = "changed"
            elif kind == "member_index": value["entries"][0]["group_index"] = 1
            else: value["entries"][0]["request_id"] = "d"*32
            hostlab.write_json(matrix.path(created["matrix_id"]), value)
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.advance(created["matrix_id"])
        self.assertEqual(self.calls, [])

    def test_unknown_group_dispatch_is_never_split_or_replayed(self):
        created = self.create(count=4, max_parallel=1)
        with patch.object(matrix.remote_schedule, "submit_group", return_value={
                "request_id": "d"*32, "status": "dispatch_unknown"}) as submit:
            self.advance(created["matrix_id"]); state = self.advance(created["matrix_id"])
        self.assertEqual(submit.call_count, 1)
        self.assertEqual(state["physical_inflight"], 1)
        self.assertEqual(state["counts"], {"dispatch_unknown": 2, "queued_local": 2})
        with self.assertRaises(ValueError): matrix.recover(created["matrix_id"], self.gh, repository="owner/repo")

    def test_crash_after_fast_group_completion_reuses_persisted_key(self):
        created = self.create(count=2, reuse_completed=False)
        def crash(*args, **kwargs):
            self.submit(*args, **kwargs); self.complete()
            raise SystemExit("caller stopped before saving group acceptance")
        with patch.object(matrix.remote_schedule, "submit_group", side_effect=crash), self.assertRaises(SystemExit):
            self.advance(created["matrix_id"])
        self.advance(created["matrix_id"])
        final = self.advance(created["matrix_id"])
        self.assertTrue(final["complete"])
        self.assertEqual(len(self.keys), 1)
        self.assertEqual(self.calls[0]["idempotency_key"], self.calls[1]["idempotency_key"])

    def test_partial_failed_run_preserves_per_version_success_and_explicit_recovery(self):
        created = self.create(count=3, runner_batch_size=3)
        self.advance(created["matrix_id"]); self.complete("failure")
        self.outcomes["g0"] = ["complete", "failed", "skipped"]
        state = self.advance(created["matrix_id"])
        self.assertTrue(state["finished"])
        self.assertFalse(state["complete"])
        self.assertEqual([e["status"] for e in state["entries"]], ["complete", "failed", "skipped"])
        self.advance(created["matrix_id"])
        self.assertEqual(len(self.calls), 1)
        self.head = "b"*40
        recovery = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo")
        saved = matrix.load(recovery["matrix_id"])
        self.assertEqual(saved["definition"]["samples"], samples(3)[1:])
        self.assertFalse(saved["definition"]["reuse_completed"])
        self.assertEqual(saved["runner_revision"], "a"*40)
        repeated = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo")
        self.assertEqual(repeated["matrix_id"], recovery["matrix_id"])
        self.outcomes.clear()
        self.advance(recovery["matrix_id"]); self.complete()
        recovered = self.advance(recovery["matrix_id"])
        self.assertTrue(recovered["complete"])
        self.assertEqual(self.calls[-1]["samples"], samples(3)[1:])
        self.assertEqual(matrix.load(created["matrix_id"])["entries"][0]["request_id"], state["entries"][0]["request_id"])
        calls_before = len(self.calls)
        repeated = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo")
        self.advance(repeated["matrix_id"])
        self.assertEqual(len(self.calls), calls_before)
        another = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo", idempotency_key="second")
        self.assertNotEqual(another["matrix_id"], recovery["matrix_id"])

    def test_result_recovery_does_not_occupy_runner_or_dispatch_again(self):
        created = self.create(count=4, max_parallel=1)
        self.advance(created["matrix_id"]); self.complete()
        unavailable = Mock(side_effect=OSError("temporary collection error"))
        state = self.advance(created["matrix_id"], collect_group=unavailable)
        self.assertEqual(state["counts"], {"awaiting_results": 2, "submitted": 2})
        self.assertEqual(state["physical_inflight"], 1)
        self.assertEqual(len(self.keys), 2)
        self.complete(); state = self.advance(created["matrix_id"])
        self.assertTrue(state["complete"])
        self.assertEqual(len(self.keys), 2)

    def test_member_identity_failure_leaves_entire_group_retryable(self):
        created = self.create(count=2)
        self.advance(created["matrix_id"]); self.complete()
        def mismatched(*args):
            result = self.collect(*args)
            result["members"][1]["sample"] = samples(3)[2]
            return result
        state = self.advance(created["matrix_id"], collect_group=mismatched)
        self.assertEqual(state["counts"], {"awaiting_results": 2})
        self.assertFalse(state["finished"])
        final = self.advance(created["matrix_id"])
        self.assertTrue(final["complete"])
        self.assertEqual(len(self.calls), 1)

    def test_missing_results_need_explicit_opt_in_and_never_replay_running_members(self):
        import remote_artifacts
        created = self.create(count=4)
        self.advance(created["matrix_id"])
        first = next(iter(self.jobs.values())); first.update(status="completed", conclusion="failure")
        missing = Mock(side_effect=remote_artifacts.ArtifactError("artifact_missing_or_ambiguous"))
        state = self.advance(created["matrix_id"], collect_group=missing, dispatch=False)
        self.assertEqual(state["counts"], {"awaiting_results": 2, "queued": 2})
        self.assertEqual(state["poll_errors"][0]["error"], "artifact_missing_or_ambiguous")
        self.assertIn("include_unverified_results=true", state["next_action_detail"])
        before = matrix.path(created["matrix_id"]).read_bytes()
        with self.assertRaises(ValueError): matrix.recover(created["matrix_id"], self.gh, repository="owner/repo")
        for flag in (1, "true", None):
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                matrix.recover(created["matrix_id"], self.gh, repository="owner/repo", include_unverified_results=flag)
        recovery = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo", include_unverified_results=True)
        saved = matrix.load(recovery["matrix_id"])
        self.assertEqual(saved["definition"]["samples"], samples(4)[:2])
        self.assertFalse(saved["definition"]["reuse_completed"])
        self.assertEqual(matrix.path(created["matrix_id"]).read_bytes(), before)
        repeat = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo", include_unverified_results=True)
        self.assertEqual(recovery["matrix_id"], repeat["matrix_id"])
        self.assertEqual(len(self.calls), 2)

    def test_unverified_recovery_opt_in_has_a_separate_immutable_key_binding(self):
        created = self.create(count=4)
        self.advance(created["matrix_id"]); self.complete()
        self.outcomes["g0"] = ["complete", "failed"]
        def partial(group, payload, run):
            if group["group_id"] == "g1": raise OSError("results not available")
            return self.collect(group, payload, run)
        self.advance(created["matrix_id"], collect_group=partial)
        default = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo", idempotency_key="attempt1")
        opted = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo", idempotency_key="attempt1",
                               include_unverified_results=True)
        self.assertNotEqual(default["matrix_id"], opted["matrix_id"])
        self.assertEqual(matrix.load(default["matrix_id"])["definition"]["samples"], [samples(4)[1]])
        self.assertEqual(matrix.load(opted["matrix_id"])["definition"]["samples"], samples(4)[1:])

    def test_one_snapshot_covers_all_group_members_without_extra_lookup(self):
        created = self.create(count=8)
        self.advance(created["matrix_id"])
        snapshot = [{**job, "display_title": "hostlab-"+rid} for rid, job in self.jobs.items()]
        lookup = Mock(side_effect=AssertionError("unnecessary member polling"))
        matrix.advance(created["matrix_id"], self.gh, lookup, lambda: snapshot, repository="owner/repo",
                       workflow="host-analysis.yml", dispatch=False, collect_group=self.collect)
        lookup.assert_not_called()

    def test_completed_group_collection_has_four_workers_and_only_main_thread_publishes_matrix(self):
        created = self.create(count=32, runner_batch_size=4)
        unavailable = Mock(side_effect=OSError("retry result collection"))
        while len(self.keys) < 8:
            self.advance(created["matrix_id"], collect_group=unavailable)
            self.complete()
        self.advance(created["matrix_id"], collect_group=unavailable, dispatch=False)
        self.assertEqual(matrix.load(created["matrix_id"])["entries"][0]["status"], "awaiting_results")
        main_thread = threading.get_ident()
        barrier = threading.Barrier(4)
        mutex = threading.Lock(); active = 0; peak = 0
        callback_threads = set(); publication_threads = []
        original_write = hostlab.write_json
        def write(path, value):
            if Path(path) == matrix.path(created["matrix_id"]):
                publication_threads.append(threading.get_ident())
            return original_write(path, value)
        def collect(group, payload, run):
            nonlocal active, peak
            with mutex:
                active += 1; peak = max(peak, active)
                callback_threads.add(threading.get_ident())
            try:
                barrier.wait(timeout=5)
                return self.collect(group, payload, run)
            finally:
                with mutex: active -= 1
        calls_before = len(self.calls)
        with patch.object(hostlab, "write_json", side_effect=write):
            state = self.advance(created["matrix_id"], collect_group=collect)
        self.assertTrue(state["complete"])
        self.assertEqual(peak, 4)
        self.assertEqual(len(callback_threads), 4)
        self.assertNotIn(main_thread, callback_threads)
        self.assertTrue(publication_threads)
        self.assertEqual(set(publication_threads), {main_thread})
        self.assertEqual(len(self.calls), calls_before)

    def test_forty_versions_need_ten_jobs_and_preserve_all_members(self):
        created = self.create(count=40, runner_batch_size=4)
        peak = 0
        while True:
            state = self.advance(created["matrix_id"])
            peak = max(peak, state["physical_inflight"])
            if state["finished"]: break
            self.complete()
        self.assertEqual(len(self.keys), 10)
        self.assertEqual(len(self.calls), 10)
        self.assertLessEqual(peak, 4)
        self.assertTrue(state["complete"])

    def test_deadline_preserves_accepted_group_and_skips_only_local_members(self):
        created = self.create(count=4, max_parallel=1)
        self.advance(created["matrix_id"])
        with patch.object(matrix.time, "time", return_value=created["deadline_at"]+1):
            state = self.advance(created["matrix_id"])
        self.assertEqual(state["counts"], {"queued": 2, "skipped": 2})
        self.complete(); state = self.advance(created["matrix_id"])
        self.assertEqual(state["counts"], {"complete": 2, "skipped": 2})
        self.assertTrue(state["finished"])


if __name__ == "__main__": unittest.main()
