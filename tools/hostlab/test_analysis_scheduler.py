"""Behavioral routing, idempotency, failure isolation and lifecycle regressions."""
import asyncio
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
import zipfile
from unittest.mock import AsyncMock, patch

import analysis_batch
import analysis_plan
import hostlab
import install_dexsql
import plan_ci
import remote_schedule


def request(**changes):
    return {"tasks": [{"id": "a", "operation": "refs", "kind": "string", "target": "disable_underline"}], **changes}


class PlanTest(unittest.TestCase):
    def test_raw_sql_dialect_is_never_inferred_or_rewritten(self):
        for dialect in ("sqlite", "dexsql"):
            sql = "SELECT 'a_b; data'"
            spec = request(tasks=[{"id":"q", "operation":"query", "sql":sql, "dialect":dialect}])
            plan = analysis_plan.plan(spec)
            self.assertEqual(plan["tasks"][0]["backend"], dialect)
            self.assertFalse(plan["raw_sql_rewritten"])
            self.assertEqual(analysis_plan.validate(spec)["tasks"][0]["sql"], sql)
        with self.assertRaises(ValueError):
            analysis_plan.plan(request(backend="dexsql", tasks=[{"id":"q", "operation":"query", "sql":"SELECT 1"}]))

    def test_site_offsets_and_explicit_coordinates_preserve_their_backend(self):
        sites = request(tasks=[{"id":"s", "operation":"refs", "kind":"string", "target":"x", "detail":"sites"}])
        self.assertEqual(analysis_plan.plan(sites)["groups"][0]["backend"], "sqlite")
        sites["backend"] = "dexsql"
        with self.assertRaises(ValueError):
            analysis_plan.plan(sites)
        coordinates = request(tasks=[{"id":"d", "operation":"decode", "method":"LFoo;->bar()V", "file_id":2}])
        with self.assertRaises(ValueError):
            analysis_plan.plan(coordinates, dexsql_available=False)

    def test_only_equivalent_semantic_tasks_fall_back(self):
        plan = analysis_plan.plan(request(), dexsql_available=False)
        self.assertEqual(plan["tasks"][0]["fallback_from"], "dexsql")
        self.assertEqual(plan["tasks"][0]["backend"], "sqlite")
        with self.assertRaises(ValueError):
            analysis_plan.plan(request(backend="dexsql"), dexsql_available=False)

    def test_warm_structure_is_reused_without_creating_an_unnecessary_second_session(self):
        metadata = {"id":"m", "operation":"locate", "name":"getUrlsMap"}
        self.assertEqual(analysis_plan.plan(request(tasks=[metadata]), sqlite_cache_hit=True)["groups"][0]["backend"], "sqlite")
        combined = analysis_plan.plan(request(tasks=[metadata, request()["tasks"][0]]), sqlite_cache_hit=True)
        self.assertEqual(combined["dataset_opens"], 1)
        self.assertEqual(combined["groups"][0]["backend"], "dexsql")

    def test_malformed_or_unbounded_requests_fail_before_io(self):
        invalid = [request(tasks=[]), request(threads=True), request(timeout_seconds=601), request(schema=True),
                   request(tasks=request()["tasks"]*17), request(tasks=[{"id":"a", "operation":"unknown"}]),
                   request(tasks=[{"id":"a", "operation":"query", "sql":"DELETE FROM classes"}]),
                   request(tasks=[{"id":"a", "operation":"refs", "target":"x", "extra":"hidden"}]),
                   request(tasks=request()["tasks"]*2), request(tasks=[{"id":"a", "operation":"query", "sql":"SELECT 1", "dialect":"sqlite", "offset":2}])]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                analysis_plan.validate(value)

    def test_generated_queries_escape_data_and_keep_dex_keys(self):
        spec = analysis_plan.validate(request(tasks=[{"id":"a", "operation":"refs", "target":"x' OR 1=1 --"}]))
        sql = analysis_plan.refs_sql(spec["tasks"][0])
        self.assertIn("value='x'' OR 1=1 --'", sql)
        self.assertIn("file_id", sql)
        self.assertIn("method_idx", sql)
        fields = analysis_plan.locate_sql({"kind":"field", "name":"urls_", "owner":"LContent;"}, "dexsql")
        self.assertIn("class_fields", fields)
        self.assertIn("field_descriptor", fields)

    def test_ci_uses_existing_minimal_dependencies_only_for_strict_native_work(self):
        native = request(backend="dexsql")
        self.assertEqual(plan_ci.requirements("batch", json.dumps(native))["requirements"], "requirements-query.txt")
        self.assertEqual(plan_ci.requirements("batch", json.dumps(request()))["requirements"], "requirements.txt")
        self.assertEqual(plan_ci.requirements("query", "SELECT 1")["needs_dexsql"], "false")

    def test_actions_queue_does_not_replace_accepted_pending_sample_work(self):
        workflow=(Path(__file__).parent/"host-analysis.yml").read_text(encoding="utf-8")
        self.assertIn("  queue: max\n",workflow)
        self.assertIn("  cancel-in-progress: false\n",workflow)


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        p = patch.object(hostlab, "STATE", self.root)
        p.start(); self.addCleanup(p.stop)
        self.dispatches = []
        self.lookup = lambda _:None
        self.runs = lambda:[]

    def gh(self, args, payload=None):
        if payload is None:
            return json.dumps({"object":{"sha":"a"*40}})
        self.dispatches.append(payload)
        return ""

    def submit(self, **kwargs):
        return remote_schedule.submit(9150200, request(), self.gh, self.lookup, self.runs,
                                      repository="owner/repo", workflow="host-analysis.yml", **kwargs)

    def test_equal_unobserved_dispatch_is_reused_not_resent(self):
        a = self.submit()
        b = self.submit()
        self.assertEqual(a["request_id"], b["request_id"])
        self.assertTrue(b["reused"])
        self.assertEqual(len(self.dispatches), 1)

    def test_network_error_after_possible_dispatch_never_replays(self):
        def flaky(args, payload=None):
            if payload is not None:
                self.dispatches.append(payload)
                raise TimeoutError("unknown")
            return self.gh(args)
        a = remote_schedule.submit(9150200, request(), flaky, self.lookup, self.runs,
                                   repository="owner/repo", workflow="host-analysis.yml")
        self.assertIsNone(a["dispatched"])
        b = self.submit()
        self.assertEqual(a["request_id"], b["request_id"])
        self.assertEqual(len(self.dispatches), 1)

    def test_only_immutable_success_is_automatically_reused_after_completion(self):
        kwargs = {"apk_sha256":"b"*64, "sample_revision":"c"*40}
        a = self.submit(**kwargs)
        self.lookup = lambda _: {"status":"completed", "conclusion":"success"}
        b = self.submit(**kwargs)
        self.assertEqual(a["request_id"], b["request_id"])
        self.assertEqual(len(self.dispatches), 1)

    def test_unpinned_completed_request_fetches_current_sample_on_new_submission(self):
        a = self.submit()
        self.lookup = lambda _: {"status":"completed", "conclusion":"success"}
        self.runs = lambda:[{"display_title":"hostlab-"+a["request_id"],"status":"completed"}]
        b = self.submit()
        self.assertNotEqual(a["request_id"], b["request_id"])
        self.assertEqual(len(self.dispatches), 2)

    def test_arbitrary_sql_is_not_automatically_cached_after_completion(self):
        spec=request(tasks=[{"id":"random","operation":"query","sql":"SELECT random()","dialect":"sqlite"}])
        kwargs={"apk_sha256":"b"*64,"sample_revision":"c"*40}
        def submit():
            return remote_schedule.submit(9150200,spec,self.gh,self.lookup,self.runs,
                repository="owner/repo",workflow="host-analysis.yml",**kwargs)
        first=submit()
        self.lookup=lambda _:{"status":"completed","conclusion":"success"}
        self.runs=lambda:[{"display_title":"hostlab-"+first["request_id"],"status":"completed"}]
        second=submit()
        self.assertNotEqual(first["request_id"],second["request_id"])
        self.assertEqual(len(self.dispatches),2)

    def test_idempotency_key_cannot_be_rebound_to_another_payload(self):
        self.submit(idempotency_key="retry1")
        with self.assertRaisesRegex(ValueError, "already bound"):
            remote_schedule.submit(9140200, request(), self.gh, self.lookup, self.runs,
                repository="owner/repo",workflow="host-analysis.yml",idempotency_key="retry1")
        self.assertEqual(len(self.dispatches), 1)

    def test_pending_and_unobserved_receipts_count_toward_admission(self):
        for i in range(4):
            self.assertTrue(self.submit(idempotency_key="task"+str(i))["dispatched"])
        result = self.submit(idempotency_key="task5")
        self.assertEqual(result["status"], "capacity_full")
        self.assertEqual(len(self.dispatches), 4)

    def test_incomplete_sample_identity_fails_before_dispatch(self):
        with self.assertRaises(ValueError):
            self.submit(apk_sha256="b"*64)
        self.assertEqual(self.dispatches, [])

    def test_os_lock_releases_after_process_exit_and_existing_lock_file_is_reusable(self):
        path = self.root / "lock"
        first = remote_schedule.admission_lock(path)
        self.assertIsNotNone(first)
        self.assertIsNone(remote_schedule.admission_lock(path))
        first.close()
        script = "import os,sys; import remote_schedule; handle=remote_schedule.admission_lock(__import__('pathlib').Path(sys.argv[1])); assert handle; os._exit(0)"
        subprocess.run([sys.executable,"-c",script,str(path)], cwd=Path(__file__).parent, check=True, timeout=15)
        acquired = remote_schedule.admission_lock(path)
        self.assertIsNotNone(acquired)
        acquired.close()


class ExecutionTest(unittest.IsolatedAsyncioTestCase):
    async def test_failed_session_is_closed_and_remaining_tasks_are_not_replayed(self):
        with tempfile.TemporaryDirectory() as temp:
            apk = Path(temp)/"app.apk"
            with zipfile.ZipFile(apk,"w") as archive: archive.writestr("classes.dex",b"fixture")
            client = SimpleNamespace(call_tool=AsyncMock())
            context = SimpleNamespace(__aenter__=None)
            class Context:
                async def __aenter__(self): return client
                async def __aexit__(self,*args): return False
            async def opened(session):
                session.dataset="opened"
                session.files={0:"classes.dex"}
                return {"backend":"sqlite"}
            with patch.object(analysis_batch,"Client",return_value=Context()), \
                 patch.object(analysis_batch.install_dexsql,"status",return_value={"available":False}), \
                 patch.object(analysis_batch.Session,"open",opened), \
                 patch.object(analysis_batch.Session,"execute",side_effect=TimeoutError("deadline")) as execute:
                spec=request(backend="sqlite",tasks=[{"id":"a","operation":"info"},{"id":"b","operation":"info"}])
                report=await analysis_batch.execute(apk,spec,roots=[temp])
            self.assertFalse(report["complete"])
            self.assertEqual([t["status"] for t in report["tasks"]],["error","skipped"])
            self.assertEqual(execute.call_count,1)
            client.call_tool.assert_awaited_once_with("close_dataset",{"dataset_id":"opened"})

    async def test_partial_native_page_remains_partial_and_uint64_stays_exact(self):
        raw={"statements":[{"columns":[{"name":"n"}],"rows":[[{"type":"uint64","value":"18446744073709551615"}]],
                            "truncated":True,"next_offset":1}]}
        session=analysis_batch.Session(None,"dexsql",Path("unused.apk"),float("inf"))
        session.dataset="d"
        session.call=AsyncMock(return_value=raw)
        response=await session.sql("SELECT 1",1)
        self.assertTrue(response["partial"])
        self.assertEqual(response["rows"][0][0],"18446744073709551615")

    async def test_child_environment_does_not_forward_runner_credentials(self):
        with patch.dict(os.environ,{"HF_TOKEN":"secret","GH_TOKEN":"secret","AI_API_KEY":"secret"}):
            env=analysis_batch.child_environment(Path("app.apk"),2)
        self.assertNotIn("HF_TOKEN",env)
        self.assertNotIn("GH_TOKEN",env)
        self.assertNotIn("AI_API_KEY",env)

    async def test_skipped_or_duplicate_dex_members_cannot_be_reported_complete(self):
        with self.assertRaisesRegex(analysis_batch.BackendError,"complete physical"):
            analysis_batch.verify_inventory({"classes.dex","classes2.dex"},{0:"classes2.dex"})
        analysis_batch.verify_inventory({"classes.dex"},{0:"classes.dex",1:"classes.dex#2"})
        with tempfile.TemporaryDirectory() as temp:
            apk=Path(temp)/"ambiguous.apk"
            import warnings
            with warnings.catch_warnings(), zipfile.ZipFile(apk,"w") as archive:
                warnings.simplefilter("ignore")
                archive.writestr("classes.dex",b"one")
                archive.writestr("classes.dex",b"two")
            with self.assertRaisesRegex(ValueError,"unambiguous"):
                analysis_batch.archive_inventory(apk)

    async def test_transport_wrapping_preserves_the_input_coverage_failure(self):
        cause=analysis_batch.BackendError("incomplete",{"missing":["classes.dex"]})
        wrapped=ExceptionGroup("transport",[ExceptionGroup("task",[cause])])
        self.assertEqual(analysis_batch.failure(wrapped),{"error":"BackendError","message":"incomplete","detail":{"missing":["classes.dex"]}})


class InstallerTest(unittest.TestCase):
    def test_git_line_endings_preserve_license_validation_and_content_changes_fail(self):
        here=install_dexsql.HERE
        licenses={name:(here/"vendor/dexsql"/name).read_bytes().replace(b"\r\n",b"\n") for name in install_dexsql.LICENSE_HASHES}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            vendor=root/"vendor/dexsql"; vendor.mkdir(parents=True)
            target=root/"installed/dexsql"; target.parent.mkdir(); target.write_bytes(b"verified fixture")
            def export(args,**kwargs):
                path=Path(args[-1])
                self.assertFalse(path.exists(),"native extractor rejects existing paths")
                path.write_text("third party notices",encoding="utf-8")
            for newline in (b"\n",b"\r\n"):
                for name,data in licenses.items(): (vendor/name).write_bytes(data.replace(b"\n",newline))
                with patch.dict(os.environ,{},clear=True), patch.object(install_dexsql,"HERE",root), \
                     patch.object(install_dexsql,"executable",return_value=target), \
                     patch.object(install_dexsql,"verify",return_value=target), \
                     patch.object(install_dexsql.subprocess,"run",side_effect=export):
                    self.assertEqual(install_dexsql.install(),target)
            (vendor/"LICENSE").write_bytes(licenses["LICENSE"]+b"changed")
            with patch.dict(os.environ,{},clear=True), patch.object(install_dexsql,"HERE",root), \
                 patch.object(install_dexsql,"executable",return_value=target), self.assertRaises(RuntimeError):
                install_dexsql.install()

    def test_explicit_unverified_override_cannot_be_executed_or_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            bad=Path(directory)/"not-dexsql.exe"; bad.write_bytes(b"wrong binary")
            with patch.dict(os.environ,{"HOSTLAB_DEXSQL":str(bad)}), patch.object(install_dexsql.urllib.request,"urlopen") as download:
                with self.assertRaises(RuntimeError): install_dexsql.install()
                self.assertFalse(install_dexsql.status()["available"])
                download.assert_not_called()
            self.assertEqual(bad.read_bytes(),b"wrong binary")


if __name__ == "__main__":
    unittest.main()
