"""Pagination budgets, durable recovery, immutable evidence and failure isolation."""
import asyncio
import copy
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import AsyncMock, patch
import zipfile

import analysis_batch as batch
import analysis_checkpoint as checkpoints
import analysis_paging as paging
import analysis_plan
import hostlab
import remote_schedule
import runner_group

SQL = "SELECT descriptor FROM classes ORDER BY descriptor"
NATIVE = {"available": True, "version": "0.1.0", "sha256": "a" * 64}
TOOLS = {**{name: "b" * 64 for name in checkpoints.STABLE_TOOLS}, **checkpoints.LEGACY}


def task(**changes):
    return {"id": "classes", "operation": "query", "sql": SQL, "dialect": "dexsql", "limit": 2, **changes}


def request(tasks=None, **changes):
    return analysis_plan.validate({"backend": "dexsql", "threads": 2, "timeout_seconds": 10,
                                   "tasks": tasks or [task()], **changes})


def page(sql, offset, limit, total=5):
    rows = [[{"type": "utf8", "value": f"LClass{i:03d};"}] for i in range(offset, min(offset + limit, total))]
    end = offset + len(rows)
    item = {"kind": "query", "sql": sql, "columns": [{"name": "descriptor", "data_type": "utf8", "nullable": False}],
            "rows": rows, "offset": offset, "next_offset": end if end < total else None,
            "truncated": end < total, "total_rows": total, "execute_ms": .1}
    return {"columns": ["descriptor"], "rows": [[r[0]["value"]] for r in rows],
            "partial": end < total, "typed_result": {"dataset_id": "dataset-1", "statements": [item], "diagnostics": []}}


class Transport:
    async def __aenter__(self): return self
    async def __aexit__(self, *args): return None


class PagingTest(unittest.IsolatedAsyncioTestCase):
    async def run_query(self, spec=None, *, total=5, seed=None, change=None):
        calls = []
        async def sql(text, limit, offset):
            calls.append((offset, limit))
            result = page(text, offset, limit, total)
            if change: change(result, len(calls))
            return result
        session = batch.Session(None, "dexsql", Path("fixture.apk"), time.monotonic() + 10)
        session.sql = sql
        snapshots = []
        result = await session.execute(analysis_plan.validate({"tasks": [spec or task()]})["tasks"][0],
                                       seed=seed, progress=lambda value: snapshots.append(copy.deepcopy(value)))
        return result, calls, snapshots

    async def test_all_pages_are_merged_without_rewriting_sql(self):
        result, calls, snapshots = await self.run_query()
        self.assertEqual([(0, 2), (2, 2), (4, 1)], calls)
        self.assertEqual(5, len(result["rows"]))
        self.assertFalse(result["partial"])
        self.assertEqual([2, 4, 5], [len(p["rows"]) for p in snapshots])
        self.assertEqual("complete", result["pagination"]["stop_reason"])
        self.assertEqual(5, len(paging.statement(result)["rows"]))

    async def test_legacy_prefix_150_fetches_only_eight_remaining_rows(self):
        result, calls, _ = await self.run_query(task(limit=150), total=158, seed=page(SQL, 0, 150, 158))
        self.assertEqual([(150, 8)], calls)
        self.assertEqual(158, len(result["rows"]))
        self.assertEqual((150, 8, 1), tuple(result["pagination"][k] for k in ("reused_rows", "fetched_rows", "pages_this_run")))
        self.assertEqual([{"offset": 150, "limit": 8, "rows": 8, "next_offset": None}], result["pagination"]["requests_this_run"])

    async def test_page_budget_is_per_attempt_and_resume_never_replays_prefix(self):
        spec = task(pagination={"max_pages": 1})
        first, calls, _ = await self.run_query(spec)
        self.assertTrue(first["partial"])
        self.assertEqual("page_budget", first["pagination"]["stop_reason"])
        second, calls, _ = await self.run_query(spec, seed=first)
        self.assertEqual([(2, 2)], calls)
        self.assertEqual(4, len(second["rows"]))
        third, calls, _ = await self.run_query(spec, seed=second)
        self.assertEqual([(4, 1)], calls)
        self.assertFalse(third["partial"])

    async def test_row_budget_shrinks_the_next_backend_request(self):
        result, calls, _ = await self.run_query(task(pagination={"max_rows": 3}))
        self.assertEqual([(0, 2), (2, 1)], calls)
        self.assertEqual(3, len(result["rows"]))
        self.assertEqual("row_budget", result["pagination"]["stop_reason"])

    async def test_byte_budget_does_not_admit_an_oversized_page(self):
        def inflate(result, number):
            result["rows"][0][0] = "x" * 2000
            result["typed_result"]["statements"][0]["rows"][0][0]["value"] = "x" * 2000
        result, calls, _ = await self.run_query(task(pagination={"max_bytes": 1024}), change=inflate)
        self.assertEqual([(0, 2)], calls)
        self.assertEqual([], result["rows"])
        self.assertTrue(result["partial"])
        self.assertEqual("byte_budget", result["pagination"]["stop_reason"])

    async def test_invalid_cursor_schema_and_total_are_never_admitted(self):
        for field, value in (("next_offset", 0), ("total_rows", 8), ("columns", [{"name": "descriptor", "data_type": "int", "nullable": False}])):
            def change(result, number):
                if number == 2:
                    result["typed_result"]["statements"][0][field] = value
            with self.subTest(field=field), self.assertRaises(paging.PageError):
                await self.run_query(change=change)

    async def test_partial_without_outer_stable_order_does_not_continue(self):
        for sql in ("SELECT 'ORDER BY' FROM classes", "SELECT * FROM (SELECT * FROM classes ORDER BY descriptor)",
                    "SELECT * FROM classes ORDER BY random()"):
            result, calls, _ = await self.run_query(task(sql=sql))
            self.assertEqual([(0, 2)], calls)
            self.assertTrue(result["partial"])
            self.assertIn(result["pagination"]["stop_reason"], {"query_requires_stable_outer_order", "query_volatile_order_or_values"})
        self.assertIsNone(paging.continuation_reason("SELECT descriptor AS random FROM classes ORDER /* comment */ BY descriptor"))
        self.assertEqual("query_volatile_order_or_values", paging.continuation_reason('SELECT descriptor FROM classes ORDER BY "random"()'))

    async def test_sqlite_preserves_legacy_single_call_and_exact_sql(self):
        session = batch.Session(None, "sqlite", Path("fixture.apk"), time.monotonic() + 10)
        expected = {"legacy_text": "fixture", "rows": [["1"]], "columns": ["v"], "partial": False}
        session.sql = AsyncMock(return_value=expected)
        spec = analysis_plan.validate({"tasks": [{"id": "legacy", "operation": "query", "sql": "SELECT 1"}]})["tasks"][0]
        self.assertEqual(expected, await session.execute(spec))
        session.sql.assert_awaited_once_with("SELECT 1", 100, 0)

    async def test_empty_result_beyond_end_is_a_successful_empty_range(self):
        result, calls, _ = await self.run_query(task(offset=10))
        self.assertEqual([(10, 2)], calls)
        self.assertFalse(result["partial"])
        self.assertEqual([], result["rows"])

    async def test_long_sql_metadata_can_be_abbreviated_without_changing_the_query(self):
        sql = "SELECT descriptor FROM classes WHERE length('" + "x" * 3000 + "')>0 ORDER BY descriptor"
        def abbreviate(result, number):
            item = result["typed_result"]["statements"][0]
            item.update(sql="SELECT descriptor FROM classes ...", sql_truncated=True)
        result, calls, _ = await self.run_query(task(sql=sql), change=abbreviate)
        self.assertFalse(result["partial"])
        self.assertEqual(5, len(result["rows"]))
        self.assertEqual(3, len(calls))

    async def test_native_offset_budget_is_respected(self):
        result, calls, _ = await self.run_query(task(offset=99000, limit=1000, pagination={"max_rows": 2000}), total=100200)
        self.assertEqual([(99000, 1000)], calls)
        self.assertTrue(result["partial"])
        self.assertEqual("backend_offset_budget", result["pagination"]["stop_reason"])

    async def test_later_page_diagnostics_are_preserved_once(self):
        def add(result, number):
            result["typed_result"]["diagnostics"] = [{"code": "shared"}, {"code": f"page{number}"}]
        result, _, _ = await self.run_query(change=add)
        self.assertEqual(["shared", "page1", "page2", "page3"], [v["code"] for v in result["typed_result"]["diagnostics"]])


class RecoveryTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.apk = self.root / "sample.apk"
        with zipfile.ZipFile(self.apk, "w") as z: z.writestr("classes.dex", b"fixture")
        self.sample = {"version_code": 9150200, "sha256": hostlab.digest(self.apk), "revision": "c" * 40}
        self.calls = []
        self.effects = None
        async def opened(session):
            session.files = {0: "classes.dex"}; session.dataset = "dataset-1"
            return {"backend": "dexsql", "files": {0: "classes.dex"}}
        async def sql(session, text, limit, offset):
            self.calls.append((offset, limit))
            if self.effects is not None: return await self.effects(text, limit, offset)
            return page(text, offset, limit, 158)
        for manager in (patch.object(batch, "Client", side_effect=lambda *a, **k: Transport()),
                        patch.object(batch.Session, "open", opened), patch.object(batch.Session, "sql", sql),
                        patch.object(batch.Session, "call", new_callable=AsyncMock),
                        patch.object(batch.install_dexsql, "status", return_value=NATIVE),
                        patch.object(batch.install_dexsql, "verify", return_value=self.root / "native")):
            manager.start(); self.addCleanup(manager.stop)

    def origin(self):
        tasks = [{"id": f"done{i}", "operation": "decode", "method": f"LFoo;->m{i}()V"} for i in range(11)] + [task(limit=150)]
        req = request(tasks)
        entries = [{"id": t["id"], "backend": "dexsql", "status": "complete", "result": {"smali": t["method"], "partial": False}} for t in req["tasks"][:-1]]
        entries.append({"id": "classes", "backend": "dexsql", "status": "partial", "result": page(SQL, 0, 150, 158)})
        report = {"schema": 1, "scope": "offline_static_only", "sample": self.sample,
                  "plan": analysis_plan.plan(req), "sessions": [{"backend": "dexsql", "files": {0: "classes.dex"}}],
                  "tasks": entries, "complete": False, "source_unchanged": True,
                  "backend_versions": {"dexsql": NATIVE},
                  "resume_origin": {"run_id": 1, "attempt": 1, "artifact_id": 2, "reused_complete_tasks": 11}}
        job = {"operation": "batch", "version_code": 9150200, "apk_sha256": self.sample["sha256"],
               "sample_revision": self.sample["revision"], "request_sha256": checkpoints.work_hash(req), "tools": TOOLS,
               "complete": False, "exit_code": 2, "backend_versions": report["backend_versions"]}
        return req, report, job

    async def execute(self, req, resume=None):
        def write(report, sealed): checkpoints.save(self.root / "checkpoint.json", report, req, TOOLS, sealed=sealed)
        return await batch.execute(self.apk, req, roots=[self.root], sample=self.sample, resume=resume, checkpoint=write)

    async def test_eleven_completed_payloads_are_unchanged_and_only_missing_eight_are_queried(self):
        req, old, job = self.origin()
        previous = checkpoints.validate(old, job, req, self.sample, TOOLS, NATIVE)
        result = await self.execute(req, previous)
        self.assertTrue(result["complete"])
        self.assertEqual([(150, 8)], self.calls)
        self.assertEqual(12, len(result["tasks"]))
        for before, after in zip(old["tasks"][:-1], result["tasks"][:-1]):
            self.assertEqual(checkpoints.checksum(before["result"]), checkpoints.checksum(after["result"]))
            self.assertTrue(after["checkpoint_reused"])
        self.assertTrue(checkpoints.read_json(self.root / "checkpoint.json")["payload"]["sealed"])
        self.assertEqual({"reused_complete_tasks": 11, "admitted_query_pages": 1, "new_query_rows": 8}, result["execution"])

    async def test_completed_checkpoint_runs_zero_queries_and_keeps_historical_result_payload(self):
        req, old, job = self.origin()
        first = await self.execute(req, old)
        self.calls.clear()
        second = await self.execute(req, first)
        self.assertTrue(second["complete"])
        self.assertEqual([], self.calls)
        self.assertEqual({"reused_complete_tasks": 12, "admitted_query_pages": 0, "new_query_rows": 0}, second["execution"])
        self.assertEqual(checkpoints.checksum(first["tasks"][-1]["result"]), checkpoints.checksum(second["tasks"][-1]["result"]))

    async def test_interruption_keeps_admitted_page_and_resumes_without_replay(self):
        async def fail(text, limit, offset):
            if offset: raise ConnectionError("private transport detail")
            return page(text, offset, limit)
        self.effects = fail
        req = request()
        first = await self.execute(req)
        self.assertFalse(first["complete"])
        self.assertEqual(2, len(first["tasks"][0]["result"]["rows"]))
        self.assertEqual(2, first["tasks"][0]["result"]["pagination"]["next_offset"])
        sealed = checkpoints.read_json(self.root / "checkpoint.json")
        self.assertTrue(sealed["payload"]["sealed"])
        self.effects = lambda text, limit, offset: asyncio.sleep(0, result=page(text, offset, limit))
        first["resume_origin"] = {"run_id": 1, "attempt": 1, "artifact_id": 2, "reused_complete_tasks": 0}
        self.calls.clear()
        second = await self.execute(req, first)
        self.assertTrue(second["complete"])
        self.assertEqual([(2, 2), (4, 1)], self.calls)

    async def test_deadline_preserves_partial_cursor_and_still_verifies_source(self):
        async def slow(text, limit, offset):
            if offset: await asyncio.sleep(5)
            return page(text, offset, limit)
        self.effects = slow
        result = await self.execute(request(timeout_seconds=1))
        self.assertFalse(result["complete"])
        self.assertTrue(result["source_unchanged"])
        self.assertEqual("partial", result["tasks"][0]["status"])
        self.assertEqual(2, result["tasks"][0]["result"]["pagination"]["next_offset"])

    async def test_deadline_before_first_page_keeps_task_in_denominator(self):
        async def slow(text, limit, offset):
            await asyncio.sleep(5)
        self.effects = slow
        result = await self.execute(request(timeout_seconds=1))
        self.assertFalse(result["complete"])
        self.assertEqual(1, len(result["tasks"]))
        self.assertEqual("skipped", result["tasks"][0]["status"])
        self.assertTrue(result["source_unchanged"])

    async def test_source_mutation_never_seals_or_completes(self):
        async def change(text, limit, offset):
            with self.apk.open("ab") as stream: stream.write(b"changed")
            return page(text, offset, limit, 1)
        self.effects = change
        result = await self.execute(request())
        self.assertFalse(result["complete"])
        self.assertFalse(result["source_unchanged"])
        self.assertFalse(checkpoints.read_json(self.root / "checkpoint.json")["payload"]["sealed"])

    async def test_unverified_resume_request_never_starts_backend_or_replays_work(self):
        req = request(resume={"run_id": 1, "attempt": 1, "request_id": "a" * 32})
        with self.assertRaisesRegex(ValueError, "verified_resume_checkpoint_required"):
            await self.execute(req)
        self.assertEqual([], self.calls)

    def test_authenticated_import_checks_attempt_and_uses_verified_artifact_cache(self):
        req, report, job = self.origin()
        req["resume"] = {"run_id": 1, "attempt": 1, "request_id": "a" * 32}
        job.update(workflow_revision="d" * 40, runner_revision="e" * 40)
        folder = self.root / "source"
        hostlab.write_json(folder / "remote-output/job.json", job)
        hostlab.write_json(folder / "remote-output/result.txt", report)
        archive = {"root": str(folder), "artifact": {"id": 2, "digest": "sha256:" + "f" * 64}}
        import remote_artifacts
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "jichuo1/innocent-lab-host-analysis"}), \
             patch.object(checkpoints, "gh", return_value=json.dumps({"run_attempt": 1, "head_sha": "d" * 40})), \
             patch.object(remote_artifacts, "get", return_value=archive) as get:
            loaded = checkpoints.load_actions(req, self.sample, TOOLS, NATIVE)
            self.assertEqual(11, loaded["resume_origin"]["reused_complete_tasks"])
            self.assertEqual(1, get.call_count)
        with patch.object(checkpoints, "gh", return_value=json.dumps({"run_attempt": 2})), \
             patch.object(remote_artifacts, "get") as get:
            with self.assertRaisesRegex(ValueError, "attempt_changed"):
                checkpoints.load_actions(req, self.sample, TOOLS, NATIVE)
            get.assert_not_called()

    def test_read_retries_are_bounded_and_never_dispatch_analysis(self):
        import subprocess
        req, _, _ = self.origin()
        req["resume"] = {"run_id": 1, "attempt": 1, "request_id": "a" * 32}
        with patch.object(checkpoints, "gh", side_effect=subprocess.TimeoutExpired("gh api", 1)) as api, \
             patch.object(checkpoints.time, "sleep"):
            with self.assertRaisesRegex(ValueError, "checkpoint_read_failed"):
                checkpoints.load_actions(req, self.sample, TOOLS, NATIVE)
            self.assertEqual(3, api.call_count)

    def test_identity_tools_native_and_result_flags_fail_closed(self):
        req, report, job = self.origin()
        for location, key, value in (("job", "apk_sha256", "0" * 64), ("job", "sample_revision", "0" * 40),
                                     ("job", "request_sha256", "0" * 64), ("report", "source_unchanged", False)):
            r, j = copy.deepcopy(report), copy.deepcopy(job)
            (j if location == "job" else r)[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                checkpoints.validate(r, j, req, self.sample, TOOLS, NATIVE)
        changed = copy.deepcopy(job); changed["tools"]["analyze.py"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "engine_tools"):
            checkpoints.validate(report, changed, req, self.sample, TOOLS, NATIVE)
        with self.assertRaisesRegex(ValueError, "native_backend"):
            checkpoints.validate(report, job, req, self.sample, TOOLS, {**NATIVE, "sha256": "0" * 64})

    def test_seal_tampering_and_unsealed_checkpoint_are_rejected(self):
        req, report, job = self.origin()
        checkpoints.save(self.root / "checkpoint.json", report, req, TOOLS, sealed=True)
        record = checkpoints.read_json(self.root / "checkpoint.json")
        self.assertEqual(report, checkpoints.validate(report, job, req, self.sample, TOOLS, NATIVE, checkpoint=record))
        record["payload"]["report"]["tasks"][0]["result"]["smali"] = "damaged"
        with self.assertRaises(ValueError):
            checkpoints.validate(report, job, req, self.sample, TOOLS, NATIVE, checkpoint=record)
        checkpoints.save(self.root / "checkpoint.json", report, req, TOOLS, sealed=False)
        with self.assertRaises(ValueError):
            checkpoints.validate(report, job, req, self.sample, TOOLS, NATIVE,
                                 checkpoint=checkpoints.read_json(self.root / "checkpoint.json"))

    def test_job_and_result_cannot_be_mixed_or_claim_missing_tasks_complete(self):
        req, report, job = self.origin()
        wrong = copy.deepcopy(report)
        wrong["plan"]["request_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "binding_mismatch"):
            checkpoints.validate(wrong, job, req, self.sample, TOOLS, NATIVE)
        wrong = copy.deepcopy(report); wrong["complete"] = True
        forged_job = {**job, "complete": True, "exit_code": 0}
        with self.assertRaisesRegex(ValueError, "completion_claim"):
            checkpoints.validate(wrong, forged_job, req, self.sample, TOOLS, NATIVE)

    def test_summary_contains_counts_cursor_and_reason_but_no_sql_or_exception_body(self):
        req, report, _ = self.origin()
        report["tasks"][-1]["result"] = paging.QueryPages(req["tasks"][-1], report["tasks"][-1]["result"]).stopped("resume_pending")
        target = self.root / "summary.md"
        checkpoints.summary(target, report, error=ValueError("secret request body"))
        text = target.read_text()
        self.assertIn("150 / 158", text)
        self.assertIn("150 / 0", text)
        self.assertIn("resume_pending", text)
        self.assertNotIn(SQL, text)
        self.assertNotIn("secret request body", text)


class ProtocolTest(unittest.TestCase):
    def test_equal_resume_dispatch_is_idempotent_even_after_failure(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(hostlab, "STATE", Path(directory)):
            payloads = []
            def gh(args, payload=None):
                if payload is not None: payloads.append(payload)
                return "" if payload is not None else json.dumps({"object": {"sha": "d" * 40}})
            req = request(resume={"run_id": 1, "attempt": 1, "request_id": "a" * 32})
            kwargs = dict(repository="owner/repo", workflow="host-analysis.yml", apk_sha256="b" * 64, sample_revision="c" * 40)
            first = remote_schedule.submit(9150200, req, gh, lambda _: None, lambda: [], **kwargs)
            second = remote_schedule.submit(9150200, req, gh, lambda _: {"status": "completed", "conclusion": "failure"}, lambda: [], **kwargs)
            self.assertEqual(first["request_id"], second["request_id"])
            self.assertEqual(1, len(payloads))
            self.assertFalse(second["dispatched"])

    def test_bad_pagination_and_resume_fields_are_rejected_before_io(self):
        for spec in (task(pagination={"max_pages": 0}), task(pagination={"max_pages": True}),
                     task(pagination={"max_bytes": 1048577}), task(pagination={"max_rows": 10001}),
                     task(pagination={"unknown": 1}), task(dialect="sqlite", pagination={"max_pages": 2})):
            with self.subTest(spec=spec), self.assertRaises(ValueError): request([spec])
        for binding in ({"run_id": 1}, {"run_id": True, "attempt": 1, "request_id": "a" * 32}):
            with self.assertRaises(ValueError): request(resume=binding)

    def test_resume_work_fingerprint_and_single_sample_contract(self):
        req = request()
        resumed = request(resume={"run_id": 1, "attempt": 1, "request_id": "a" * 32})
        self.assertEqual(analysis_plan.fingerprint(req), checkpoints.work_hash(resumed))
        self.assertNotEqual(analysis_plan.fingerprint(req), analysis_plan.fingerprint(resumed))
        samples = [{"version_code": 1, "apk_sha256": "a" * 64, "sample_revision": "b" * 40}]
        with self.assertRaisesRegex(ValueError, "single pinned sample"):
            runner_group.validate({"schema": 1, "request": resumed, "samples": samples})

    def test_resume_without_exact_sample_is_not_dispatched(self):
        gh = unittest.mock.Mock()
        with self.assertRaisesRegex(ValueError, "exact APK"):
            remote_schedule.submit(1, request(resume={"run_id": 1, "attempt": 1, "request_id": "a" * 32}),
                gh, lambda _: None, lambda: [], repository="owner/repo", workflow="host-analysis.yml")
        gh.assert_not_called()


if __name__ == "__main__": unittest.main()
