"""Long-value query and artifact paging regressions; no network or APK download."""
from contextlib import closing, redirect_stderr
import importlib.util
import io
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import dexq_cli
import hostlab
import remote_job
import remote_mcp

DEXQ = Path(__file__).resolve().parent / "dexq"
sys.path.insert(0, str(DEXQ))
spec = importlib.util.spec_from_file_location("dexq_query_test_server", DEXQ / "server.py")
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class QueryOutputTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "index.sqlite"
        self.value = "开头" + "悟空🔍" * 400 + "\t末尾\n完整\r结束"
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("CREATE TABLE strings(file_id INTEGER, string_idx INTEGER, value TEXT)")
            conn.execute("INSERT INTO strings VALUES (0, 7, ?)", (self.value,))
        self.datasets = patch.dict(server._datasets, {"fixture": {"db": str(self.db)}})
        self.datasets.start()
        self.addCleanup(self.datasets.stop)

    def query(self, sql="SELECT value FROM strings", **kwargs):
        return server.query("fixture", sql, **kwargs)

    def test_default_preview_marks_clipping_without_altering_stored_value(self):
        output = self.query()
        self.assertEqual(output.splitlines()[1], self.value[:300] + "…")
        self.assertIn("1 cell(s) truncated at 300", output)
        with closing(sqlite3.connect(self.db)) as conn:
            self.assertEqual(conn.execute("SELECT value FROM strings").fetchone()[0], self.value)

    def test_requested_long_preview_contains_the_tail_and_escapes_controls(self):
        output = self.query(max_cell_chars=3000)
        self.assertIn("\\t末尾\\n完整\\r结束", output)
        self.assertEqual(len(output.splitlines()), 3)
        self.assertNotIn("truncated", output)

    def test_larger_than_one_cell_is_reconstructable_with_sql_substr(self):
        value = "长🔍" * 10500 + "终点"
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("UPDATE strings SET value=?", (value,))
        parts = []
        for start in range(1, len(value) + 1, 8000):
            output = self.query(f"SELECT substr(value,{start},8000) FROM strings "
                                "WHERE file_id=0 AND string_idx=7", max_cell_chars=16000)
            self.assertNotIn("truncated", output)
            parts.append(output.splitlines()[1])
        self.assertEqual("".join(parts), value)

    def test_total_output_budget_keeps_complete_rows(self):
        output = self.query("WITH RECURSIVE n(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM n WHERE x<30) "
                            "SELECT x, replace(hex(zeroblob(3000)),'0','字') FROM n ORDER BY x",
                            max_cell_chars=16000)
        self.assertLessEqual(len(output), 64000)
        self.assertIn("output truncated", output)
        rows = [line for line in output.splitlines()[1:] if not line.startswith("-- ")]
        self.assertGreater(len(rows), 0)
        for line in rows:
            number, value = line.split("\t")
            self.assertTrue(number.isdigit())
            self.assertEqual(value, "字" * 6000)

    def test_row_limit_remains_separate_from_cell_limit(self):
        output = self.query("SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3", limit=2)
        self.assertEqual(output.splitlines()[1:3], ["1", "2"])
        self.assertIn("2 row(s) (truncated", output)
        self.assertNotIn("cell(s) truncated", output)

    def test_out_of_range_cell_lengths_are_rejected(self):
        for length in (-1, 0, 16001):
            with self.subTest(length=length), self.assertRaises(server.ToolError):
                self.query(max_cell_chars=length)

    def test_sql_stays_read_only_and_single_statement(self):
        for sql in ("DROP TABLE strings", "SELECT 1; SELECT 2",
                    "WITH n AS (SELECT 1) DELETE FROM strings"):
            with self.subTest(sql=sql), self.assertRaises(server.ToolError):
                self.query(sql, max_cell_chars=16000)


class CliForwardingTest(unittest.TestCase):
    def test_cell_option_reaches_the_stdio_client(self):
        with patch.object(dexq_cli.analyze, "inputs", return_value=(Path("fixture.apk"), {})), \
                patch.object(dexq_cli, "run", new_callable=AsyncMock) as run:
            dexq_cli.main(["query", "--apk", "fixture.apk", "--sql", "SELECT 1",
                           "--max-cell-chars", "16000"])
        self.assertEqual(run.call_args.args[0].max_cell_chars, 16000)

    def test_invalid_cell_option_is_rejected_before_resolving_an_apk(self):
        with patch.object(dexq_cli.analyze, "inputs") as inputs, redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                dexq_cli.main(["query", "--apk", "fixture.apk", "--sql", "SELECT 1",
                               "--max-cell-chars", "0"])
        inputs.assert_not_called()


class RemoteQueryInputTest(unittest.TestCase):
    def test_legacy_dispatch_omits_new_default_input(self):
        with patch.object(remote_mcp, "gh") as gh:
            remote_mcp.submit_job(9140200, "query", "SELECT 1")
        self.assertNotIn("max_cell_chars", gh.call_args.args[1]["inputs"])

    def test_requested_cell_limit_is_a_structured_dispatch_input(self):
        sql = "SELECT 'literal; shell text stays data'"
        with patch.object(remote_mcp, "gh") as gh:
            remote_mcp.submit_job(9140200, "query", sql, max_cell_chars=12000)
        self.assertEqual(gh.call_args.args[1]["inputs"]["max_cell_chars"], "12000")
        self.assertEqual(gh.call_args.args[1]["inputs"]["argument"], sql)

    def test_invalid_limits_and_unrelated_operations_do_not_dispatch(self):
        with patch.object(remote_mcp, "gh") as gh:
            for operation, size in (("query", 0), ("query", 16001), ("info", 12000)):
                with self.subTest(operation=operation, size=size), self.assertRaises(remote_mcp.ToolError):
                    remote_mcp.submit_job(9140200, operation, max_cell_chars=size)
        gh.assert_not_called()

    def test_runner_forwards_cell_limit_and_records_dexq_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = {"version_code": 9140200, "sha256": "a" * 64,
                      "path": "apks/tv.danmaku.bili/9140200/" + "a" * 64 + "/base.apk"}
            env = {"HOSTLAB_VERSION": "9140200", "HOSTLAB_OPERATION": "query",
                   "HOSTLAB_ARGUMENT": "SELECT 'long value'", "HOSTLAB_MAX_CELL_CHARS": "12000"}
            with patch.dict(os.environ, env, clear=True), patch.object(hostlab, "STATE", root), \
                    patch.object(hostlab, "CONFIG", root / "config.json"), \
                    patch.object(hostlab, "api_private", return_value=(None, "b" * 40)), \
                    patch.object(hostlab, "manifest", return_value={"samples": [sample]}), \
                    patch.object(remote_job.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run:
                self.assertEqual(remote_job.main(), 0)
            command = run.call_args.args[0]
            self.assertEqual(command[command.index("--max-cell-chars") + 1], "12000")
            self.assertEqual(command[command.index("--sql") + 1], env["HOSTLAB_ARGUMENT"])
            job = json.loads((root / "remote-output/job.json").read_text(encoding="utf-8"))
            self.assertEqual(job["max_cell_chars"], 12000)
            self.assertEqual(job["apk_sha256"], sample["sha256"])
            self.assertEqual(job["tools"]["dexq/server.py"], hostlab.digest(DEXQ / "server.py"))

    def test_runner_rejects_invalid_input_before_remote_access(self):
        for size in ("", "0", "-1", "16001", "1;anything"):
            env = {"HOSTLAB_VERSION": "9140200", "HOSTLAB_OPERATION": "query",
                   "HOSTLAB_MAX_CELL_CHARS": size}
            with self.subTest(size=size), patch.dict(os.environ, env, clear=True), \
                    patch.object(hostlab, "api_private") as api, self.assertRaises(RuntimeError):
                remote_job.main()
            api.assert_not_called()


class RemoteResultPagingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / "remote-results/123"
        self.out.mkdir(parents=True)
        self.value = "前" + "悟空🔍\n" * 4000 + "END完整结束"
        (self.out / "result.txt").write_text(self.value, encoding="utf-8", newline="\n")
        (self.out / "job.json").write_text('{"exit_code":0}', encoding="utf-8")
        for fixture in (patch.object(hostlab, "STATE", self.root),
                        # These tests isolate rendering; verified-cache behavior has real ZIP tests.
                        patch("remote_artifacts.get", side_effect=lambda *args, **kwargs: {
                            "root":str(self.out),"files":[str(p) for p in self.out.rglob("*") if p.is_file()],
                            "cache_hit":True,"artifact":{},"integrity":"test_rendering_fixture","elapsed_ms":0,"run_attempt":1}),
                        patch.object(remote_mcp, "repository_report", return_value=None),
                        patch.object(remote_mcp, "lookup", return_value={"id": 123, "status": "completed",
                                                                         "html_url": "https://example.invalid/run/123"})):
            fixture.start()
            self.addCleanup(fixture.stop)

    def result(self, offset=0):
        return json.loads(remote_mcp.job_result("a" * 32, result_offset=offset))

    def test_all_pages_reconstruct_the_unicode_result_without_redispatch(self):
        reconstructed = []
        offset = 0
        with patch.object(remote_mcp, "gh") as gh:
            while True:
                response = self.result(offset)
                page = response["result_page"]
                start = len(page["file"]) + 1
                reconstructed.append(response["text"][start:start + page["chars"]])
                self.assertLessEqual(len(response["text"]), 24000)
                self.assertEqual(page["offset"], offset)
                self.assertEqual(page["total_chars"], len(self.value))
                if page["next_offset"] is None:
                    break
                self.assertGreater(page["next_offset"], offset)
                offset = page["next_offset"]
        self.assertEqual("".join(reconstructed), self.value)
        gh.assert_not_called()

    def test_small_results_and_eof_return_no_next_page(self):
        (self.out / "result.txt").write_text("short", encoding="utf-8")
        response = self.result()
        self.assertIn("short", response["text"])
        self.assertIsNone(response["result_page"]["next_offset"])
        self.assertFalse(response["text_truncated"])
        eof = self.result(100)
        self.assertEqual(eof["result_page"]["chars"], 0)
        self.assertIsNone(eof["result_page"]["next_offset"])

    def test_large_other_previews_cannot_displace_the_result_page(self):
        (self.out / "class.java").write_text("x" * 20000, encoding="utf-8")
        (self.out / "summary.json").write_text("y" * 20000, encoding="utf-8")
        response = self.result()
        self.assertTrue(response["text_truncated"])
        self.assertTrue(response["text"].startswith("result.txt\n" + self.value[:8000]))

    def test_negative_offsets_and_missing_result_are_explicit_errors(self):
        with self.assertRaises(remote_mcp.ToolError):
            self.result(-1)
        (self.out / "result.txt").unlink()
        with self.assertRaises(remote_mcp.ToolError):
            self.result(8000)
        self.assertIsNone(self.result()["result_page"])

    def test_ambiguous_result_files_do_not_return_a_misleading_cursor(self):
        nested = self.out / "nested"
        nested.mkdir()
        (nested / "result.txt").write_text("different source", encoding="utf-8")
        with self.assertRaises(remote_mcp.ToolError):
            self.result()


if __name__ == "__main__":
    unittest.main()
