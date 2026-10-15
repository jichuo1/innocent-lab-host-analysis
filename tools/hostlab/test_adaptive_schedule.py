"""Adaptive placement snapshots, advisory caches and durable admission regressions."""
import hashlib
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

import adaptive_schedule as adaptive
import analysis_plan
import hostlab
import version_matrix as matrix


def samples(count=34):
    return [{"version_code": 9000000+i, "apk_sha256": format(i+1, "064x"),
             "sample_revision": "c"*40} for i in range(count)]


def request(backend="dexsql"):
    return {"backend": backend, "tasks": [{"id": "feature", "operation": "locate", "name": "getUrlsMap"}]}


class AdaptiveTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        p = patch.object(hostlab, "STATE", self.root); p.start(); self.addCleanup(p.stop)
        p = patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": ""}); p.start(); self.addCleanup(p.stop)
        self.revision = "a"*40

    def profile(self, rows, *, filename=None, spec=None):
        spec = spec or request()
        root = adaptive.directory(); root.mkdir(parents=True, exist_ok=True)
        path = root / (filename or self.revision + "-" + analysis_plan.fingerprint(spec) + ".json")
        hostlab.write_json(path, {"schema": 1, "runner_revision": self.revision,
            "request_sha256": analysis_plan.fingerprint(spec), "rows": rows})
        return path

    def rows(self, count=34, size=200000000):
        return [{"apk_sha256": s["apk_sha256"], "size_bytes": size, "fetch_ms": 3000,
                 "analysis_ms": 1500, "observed_at": 1} for s in samples(count)]

    def test_cold_projection_balances_counts_without_profile_or_network_access(self):
        with patch.object(adaptive, "snapshot", side_effect=AssertionError("plan read a profile")), patch.dict(
                os.environ, {"HOSTLAB_SCHEDULING_PROFILE": "outside-any-profile-directory"}):
            planned = matrix.plan(samples(), request(), execution_policy="adaptive")
        self.assertEqual(planned["physical_job_count"], 4)
        self.assertEqual([len(g["sample_indices"]) for g in planned["adaptive_plan"]["groups"]], [9, 9, 8, 8])
        self.assertEqual(planned["adaptive_plan"]["profiled_samples"], 0)
        self.assertTrue(all(row["size_bytes"] is None for row in planned["adaptive_plan"]["cost_snapshot"]["rows"]))
        self.assertEqual(planned["advance_dispatch_budget"], 4)

    def test_exact_profiles_balance_cost_and_snapshot_is_self_contained(self):
        rows = self.rows(8)
        rows[0].update(fetch_ms=20000, analysis_ms=8000)
        path = self.profile(rows)
        plan = adaptive.build(samples(8), request(), self.revision, 4, 1800)
        self.assertEqual(plan["profiled_samples"], 8)
        groups = plan["groups"]
        self.assertEqual(sorted(i for g in groups for i in g["sample_indices"]), list(range(8)))
        self.assertEqual(len(groups), 4)
        self.assertLess(len(next(g["sample_indices"] for g in groups if 0 in g["sample_indices"])), 3)
        self.assertEqual(plan["cost_snapshot"]["profile_source"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        path.unlink()
        adaptive.validate_plan(plan, samples(8), request(), self.revision, 4, 1800)

    def test_group_count_size_and_prediction_caps_split_without_losing_versions(self):
        native = adaptive.projection(samples(40), request(), 1, 1800)
        self.assertTrue(all(len(g["sample_indices"]) <= 12 for g in native["groups"]))
        for backend in ("sqlite", "auto"):
            other = adaptive.projection(samples(40), request(backend), 4, 1800)
            self.assertTrue(all(len(g["sample_indices"]) <= 4 for g in other["groups"]))
            self.assertEqual(other["physical_job_count"], 10)
        self.profile(self.rows(20, size=1024**3))
        bounded = adaptive.build(samples(20), request(), self.revision, 4, 1800)
        self.assertTrue(all(g["known_input_bytes"] <= 4*1024**3 for g in bounded["groups"]))
        self.assertEqual(sorted(i for g in bounded["groups"] for i in g["sample_indices"]), list(range(20)))
        self.profile(self.rows(20))
        short = adaptive.build(samples(20), request(), self.revision, 4, 1)
        self.assertEqual(short["physical_job_count"], 20)
        self.assertTrue(all(g["prediction_exceeds_deadline"] for g in short["groups"]))

    def test_payload_byte_cap_can_split_independently_of_sample_count(self):
        import runner_group
        base = {"schema": 2, "request": analysis_plan.validate(request()), "samples": samples(1),
                "execution": adaptive.EXECUTION}
        cap = len(json.dumps(base, ensure_ascii=False).encode()) + 1
        with patch.object(runner_group, "MAX_REQUEST_BYTES", cap):
            projected = adaptive.projection(samples(8), request(), 4, 1800)
        self.assertEqual(projected["physical_job_count"], 8)
        self.assertEqual(sorted(i for g in projected["groups"] for i in g["sample_indices"]), list(range(8)))

    def test_frozen_profile_requires_dedicated_regular_file_and_records_exact_bytes(self):
        frozen = self.profile(self.rows(4), filename="frozen-calibration.json")
        with patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": str(frozen)}):
            snap = adaptive.snapshot(samples(4), request(), self.revision)
        self.assertEqual(snap["profile_source"]["kind"], "frozen")
        self.assertEqual(snap["profile_source"]["sha256"], hashlib.sha256(frozen.read_bytes()).hexdigest())
        for value in (str(self.root / "frozen-outside.json"), str(frozen.parent / "nested/frozen-x.json"),
                      "frozen-calibration.json", str(frozen.parent / "frozen-missing.json")):
            with self.subTest(value=value), patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": value}), self.assertRaises(ValueError):
                adaptive.snapshot(samples(4), request(), self.revision)
        value = json.loads(frozen.read_text()); value["runner_revision"] = "b"*40
        hostlab.write_json(frozen, value)
        with patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": str(frozen)}), self.assertRaises(ValueError):
            adaptive.snapshot(samples(4), request(), self.revision)

    def test_linked_frozen_profile_is_never_followed(self):
        target = self.profile(self.rows(1))
        link = target.parent / "frozen-linked.json"
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest("host does not permit symlink fixture: " + type(exc).__name__)
        with patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": str(link)}), self.assertRaises(ValueError):
            adaptive.snapshot(samples(1), request(), self.revision)

    def test_corrupt_live_profile_is_advisory_and_tampered_snapshot_is_rejected(self):
        path = self.profile(self.rows(2))
        value = json.loads(path.read_text()); value["rows"][0]["fetch_ms"] = float("nan")
        hostlab.write_json(path, value)
        plan = adaptive.build(samples(2), request(), self.revision, 4, 1800)
        self.assertEqual(plan["profiled_samples"], 0)
        self.assertEqual(plan["cost_snapshot"]["profile_source"]["kind"], "unavailable")
        plan["cost_snapshot"]["rows"][0]["analysis_ms"] = 100
        with self.assertRaises(ValueError): adaptive.validate_plan(plan, samples(2), request(), self.revision, 4, 1800)

    def evidence(self, sample=None, dirname="evidence"):
        payload = {"schema": 1, "request": request(), "samples": [sample] if sample else samples(1)}
        fingerprint = analysis_plan.fingerprint(payload["request"])
        root = self.root / dirname
        output = root / "samples/0"; output.mkdir(parents=True)
        sample = payload["samples"][0]
        receipt = {"schema": 1, "runner_revision": self.revision, "request_sha256": fingerprint,
                   "samples": [{"index": 0, "sample": sample, "status": "complete"}]}
        metadata = {"operation": "batch", "version_code": sample["version_code"], "apk_sha256": sample["apk_sha256"],
                    "sample_revision": sample["sample_revision"], "runner_revision": self.revision,
                    "request_sha256": fingerprint, "group_index": 0, "complete": True, "exit_code": 0,
                    "fetch_ms": 3000, "phases": {"analysis_ms": 1500}}
        result = {"complete": True, "source_unchanged": True, "sample": {"size": 200000000,
                  "sha256": sample["apk_sha256"], "version_code": sample["version_code"], "revision": sample["sample_revision"]}}
        hostlab.write_json(root / "group.json", receipt)
        hostlab.write_json(output / "job.json", metadata); hostlab.write_json(output / "result.txt", result)
        return payload, {"files": [str(root / "group.json"), str(output / "job.json"), str(output / "result.txt")]}

    def test_observe_requires_complete_source_proof_and_does_not_change_frozen_bytes(self):
        payload, downloaded = self.evidence()
        frozen = self.profile(self.rows(1), filename="frozen-calibration.json")
        before = frozen.read_bytes()
        with patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": str(frozen)}):
            self.assertEqual(adaptive.observe(payload, downloaded, self.revision)["stored"], 1)
        self.assertEqual(frozen.read_bytes(), before)
        path = Path(downloaded["files"][-1]); value = json.loads(path.read_text())
        value["source_unchanged"] = False; hostlab.write_json(path, value)
        self.assertEqual(adaptive.observe(payload, downloaded, self.revision)["stored"], 0)

    def test_profile_write_has_fixed_row_and_byte_budgets(self):
        payload, downloaded = self.evidence()
        rows = self.rows(256)
        rows[0]["apk_sha256"] = "f"*64
        self.profile(rows)
        self.assertEqual(adaptive.observe(payload, downloaded, self.revision)["stored"], 1)
        path = adaptive.directory() / (self.revision + "-" + analysis_plan.fingerprint(request()) + ".json")
        value = json.loads(path.read_text())
        self.assertEqual(len(value["rows"]), 256)
        self.assertLessEqual(path.stat().st_size, adaptive.MAX_PROFILE_BYTES)
        self.assertIn(samples(1)[0]["apk_sha256"], {r["apk_sha256"] for r in value["rows"]})
        self.assertEqual(list(adaptive.directory().glob(".profile-*.tmp")), [])

    def test_concurrent_collection_merges_verified_profile_rows_under_one_os_lock(self):
        evidence = [self.evidence(sample, "evidence"+str(index)) for index, sample in enumerate(samples(8))]
        original_replace = os.replace
        def slow_publish(source, target):
            if Path(target).parent == adaptive.directory():
                time.sleep(.02)
            return original_replace(source, target)
        with patch.object(os, "replace", side_effect=slow_publish), ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda item: adaptive.observe(*item, self.revision), evidence))
        self.assertEqual(sum(r["stored"] for r in results), 8)
        selected = adaptive.snapshot(samples(8), request(), self.revision)
        self.assertEqual(sum(row["fetch_ms"] is not None for row in selected["rows"]), 8)


class AdaptiveMatrixTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        p = patch.object(hostlab, "STATE", self.root); p.start(); self.addCleanup(p.stop)
        p = patch.dict(os.environ, {"HOSTLAB_SCHEDULING_PROFILE": ""}); p.start(); self.addCleanup(p.stop)
        self.head = "a"*40; self.jobs = {}; self.calls = []; self.keys = {}
        p = patch.object(matrix.remote_schedule, "submit_group", side_effect=self.submit)
        p.start(); self.addCleanup(p.stop)

    def gh(self, *args, **kwargs):
        return json.dumps({"object": {"sha": self.head}})

    def submit(self, rows, spec, gh, lookup, runs, **kwargs):
        self.calls.append({**kwargs, "samples": rows})
        key = kwargs["idempotency_key"]
        if key in self.keys:
            rid = self.keys[key]; run = self.jobs[rid]
            return {"request_id": rid, "status": run["status"], "conclusion": run.get("conclusion"), "reused": True}
        rid = format(len(self.keys)+1, "032x"); self.keys[key] = rid
        self.jobs[rid] = {"id": len(self.keys), "status": "queued", "conclusion": None,
                          "html_url": "https://example.invalid/"+rid, "head_sha": "a"*40,
                          "run_attempt": 1, "display_title": "hostlab-"+rid}
        return {"request_id": rid, "status": "submitted", "reused": False}

    def create(self, **kwargs):
        return matrix.create(samples(), request(), self.gh, repository="owner/repo",
                             execution_policy="adaptive", **kwargs)

    def advance(self, identifier, **kwargs):
        return matrix.advance(identifier, self.gh, self.jobs.get, lambda: [], repository="owner/repo",
                              workflow="host-analysis.yml", **kwargs)

    def test_adaptive_dispatch_fills_four_slots_and_wire_identity_is_new(self):
        created = self.create()
        saved = matrix.load(created["matrix_id"])
        self.assertEqual(saved["schema"], 3)
        state = self.advance(created["matrix_id"])
        self.assertEqual(len(self.calls), 4)
        self.assertEqual(state["physical_inflight"], 4)
        self.assertEqual(sorted(len(c["samples"]) for c in self.calls), [8, 8, 9, 9])
        self.assertTrue(all(c["execution"] == adaptive.EXECUTION for c in self.calls))
        for group in saved["groups"]:
            payload = matrix.group_payload(saved, group)
            self.assertEqual(payload["schema"], 2)
            self.assertEqual(payload["execution"], adaptive.EXECUTION)
        for size in (2, 4):
            with self.assertRaises(ValueError): matrix.plan(samples(), request(), runner_batch_size=size, execution_policy="adaptive")

    def test_repeat_key_loads_frozen_plan_without_current_profile_or_main_access(self):
        created = self.create(idempotency_key="adaptive1")
        before = matrix.path(created["matrix_id"]).read_bytes()
        with patch.object(adaptive, "build", side_effect=AssertionError("profile recomputed")), patch.dict(
                os.environ, {"HOSTLAB_SCHEDULING_PROFILE": "invalid-current-profile"}):
            repeated = matrix.create(samples(), request(), Mock(side_effect=AssertionError("main reread")),
                repository="owner/repo", execution_policy="adaptive", idempotency_key="adaptive1")
        self.assertEqual(created["matrix_id"], repeated["matrix_id"])
        self.assertEqual(matrix.path(created["matrix_id"]).read_bytes(), before)

    def test_adaptive_cost_or_group_state_tampering_is_rejected(self):
        created = self.create()
        value = matrix.load(created["matrix_id"])
        value["definition"]["adaptive_plan"]["groups"][0]["sample_indices"].reverse()
        value["definition_sha256"] = matrix.digest(value["definition"])
        value["binding_sha256"] = matrix.binding_hash(value)
        hostlab.write_json(matrix.path(created["matrix_id"]), value)
        with self.assertRaises(ValueError): matrix.load(created["matrix_id"])

    def test_adaptive_unknowns_do_not_replay_and_explicit_recovery_preserves_policy(self):
        created = self.create(reuse_completed=False)
        state = self.advance(created["matrix_id"])
        for job in self.jobs.values(): job["status"] = "pending"
        self.advance(created["matrix_id"])
        self.assertEqual(len(self.calls), 4)
        for job in self.jobs.values(): job.update(status="completed", conclusion="failure")
        def collect(group, payload, run):
            return {"members": [{"index": i, "sample": sample, "status": "failed" if i == 0 else "complete", "files": []}
                                for i, sample in enumerate(payload["samples"])]}
        self.advance(created["matrix_id"], collect_group=collect)
        original = matrix.load(created["matrix_id"])
        self.head = "b"*40
        recovered = matrix.recover(created["matrix_id"], self.gh, repository="owner/repo")
        saved = matrix.load(recovered["matrix_id"])
        self.assertEqual(saved["runner_revision"], "a"*40)
        self.assertEqual(saved["definition"]["execution_policy"], "adaptive")
        self.assertFalse(saved["definition"]["reuse_completed"])
        self.assertEqual(saved["definition"]["samples"], [e["sample"] for e in original["entries"] if e["status"] == "failed"])


if __name__ == "__main__": unittest.main()
