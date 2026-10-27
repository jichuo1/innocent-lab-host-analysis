"""Deterministic versus progressable failures, and the replay gate they drive."""
import tempfile
from pathlib import Path
import unittest

import analysis_plan
import analyze
import retry_policy


class ClassifyTest(unittest.TestCase):
    def test_rejections_that_cannot_change_on_replay_are_deterministic(self):
        for kind in ("invalid_query", "invalid_input", "impl_defined", "output_too_large",
                     "class_not_found", "decompile_empty", "not_found"):
            with self.subTest(kind=kind):
                self.assertEqual(retry_policy.classify([kind]), "deterministic")

    def test_budget_stops_resume_instead_of_blocking_the_next_attempt(self):
        # A partial page keeps its cursor: refusing the replay would make completion impossible.
        for kind in ("page_budget", "row_budget", "byte_budget", "resume_pending"):
            with self.subTest(kind=kind):
                self.assertEqual(retry_policy.classify([kind]), "progressable")

    def test_transport_and_capacity_failures_stay_replayable(self):
        for kind in ("backend_request_failed", "page_request_failed", "timeout",
                     "analysis_deadline_or_session_failure", "backend_session_failed_or_deadline",
                     "disk_capacity", "runner_interrupted_before_member", "native_page_budget_retry"):
            with self.subTest(kind=kind):
                self.assertEqual(retry_policy.classify([kind]), "progressable")

    def test_mixed_unknown_and_empty_reasons_never_claim_determinism(self):
        self.assertEqual(retry_policy.classify([]), "unknown")
        self.assertEqual(retry_policy.classify([None, "Free text with spaces"]), "unknown")
        self.assertEqual(retry_policy.classify(["invalid_query", "backend_request_failed"]), "progressable")
        self.assertEqual(retry_policy.classify(["invalid_query", "some_new_word"]), "unknown")

    def test_reasons_are_deduplicated_bounded_machine_words(self):
        words = retry_policy.reasons(["row_budget", "row_budget", "SELECT * FROM classes", "byte_budget", None])
        self.assertEqual(words, ["row_budget", "byte_budget"])
        self.assertEqual(len(retry_policy.reasons(["r" + str(i) for i in range(40)])), retry_policy.MAX_REASONS)


class CommandFailureTest(unittest.TestCase):
    def test_schema_errors_are_reported_without_copying_the_statement(self):
        text = "Tool 'query' failed: 'Error executing tool query: sql error: no such table: class_methods'"
        failure = retry_policy.command_failure("query", 1, text)
        self.assertEqual(failure["kind"], "invalid_query")
        self.assertEqual(failure["hint"], "native table names require backend=dexsql")
        self.assertNotIn("Tool 'query' failed", str(failure))
        self.assertNotIn("hint", retry_policy.command_failure("query", 1, text, "dexsql"))

    def test_absent_class_and_timeout_are_separated_from_unknown_commands(self):
        missing = retry_policy.command_failure(
            "decompile", 1, 'Exception in thread "main" java.lang.ClassNotFoundException: kntr.a.B')
        self.assertEqual(missing["kind"], "class_not_found")
        self.assertEqual(retry_policy.command_failure("query", 124, "")["kind"], "timeout")
        self.assertEqual(retry_policy.command_failure("info", 1, "")["kind"], "command_failed")
        self.assertNotEqual(retry_policy.classify(["command_failed"]), "deterministic")

    def test_child_output_is_only_scanned_inside_the_bounded_prefix(self):
        padded = "x" * 100000 + " no such table: classes"
        self.assertEqual(retry_policy.command_failure("query", 1, padded)["kind"], "command_failed")
        self.assertEqual(retry_policy.command_failure("query", 1, "no such table: classes")["kind"], "invalid_query")


class ExceptionKindTest(unittest.TestCase):
    def test_recorded_exception_type_names_become_bounded_kinds(self):
        self.assertEqual(retry_policy.exception_kind("ValueError"), "invalid_input")
        self.assertEqual(retry_policy.exception_kind("TimeoutError"), "timeout")
        self.assertEqual(retry_policy.exception_kind("OSError"), "harness_failed")
        self.assertEqual(retry_policy.exception_kind("SomeNewError"), "harness_failed")
        self.assertEqual(retry_policy.exception_kind(None), "harness_failed")
        self.assertEqual(retry_policy.classify([retry_policy.exception_kind("ValueError")]), "deterministic")


class ReplayGateTest(unittest.TestCase):
    def receipt(self, **changes):
        return {"status": "completed", "conclusion": "failure", "retry_class": "deterministic",
                "created_at": 1000.0, **changes}

    def test_only_a_recent_deterministic_failure_of_the_same_receipt_blocks_replay(self):
        self.assertTrue(retry_policy.blocks_replay(self.receipt(), now=1001.0))
        self.assertFalse(retry_policy.blocks_replay(self.receipt(), now=1000.0 + retry_policy.REPLAY_WINDOW_SECONDS + 1))
        self.assertFalse(retry_policy.blocks_replay(self.receipt(conclusion="success"), now=1001.0))
        self.assertFalse(retry_policy.blocks_replay(self.receipt(retry_class="progressable"), now=1001.0))
        self.assertFalse(retry_policy.blocks_replay(self.receipt(retry_class="transient"), now=1001.0))
        self.assertFalse(retry_policy.blocks_replay(self.receipt(status="dispatch_unknown"), now=1001.0))
        self.assertFalse(retry_policy.blocks_replay({}, now=1001.0))
        self.assertFalse(retry_policy.blocks_replay(None))
        self.assertFalse(retry_policy.blocks_replay(self.receipt(created_at="yesterday"), now=1001.0))

    def test_job_json_annotations_drive_the_receipt_class(self):
        word = {"failure_reasons": ["page_budget"]}
        self.assertEqual(retry_policy.classification([word]), {"retry_class": "progressable",
                                                              "failure_reasons": ["page_budget"]})
        self.assertEqual(retry_policy.classification([{"failure": {"kind": "class_not_found"}}])["retry_class"],
                         "deterministic")
        self.assertIsNone(retry_policy.classification([{"complete": True}]))
        self.assertEqual(retry_policy.classification([word, {"failure": {"kind": "timeout"}}])["retry_class"],
                         "progressable")


class DecompileCauseTest(unittest.TestCase):
    def test_empty_source_keeps_a_bounded_cause_instead_of_a_bare_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "decompile.log"
            log.write_text('Exception in thread "main" java.lang.ClassNotFoundException: kntr.a.B\n',
                           encoding="utf-8")
            missing = analyze.decompile_failure(1, log)
            self.assertEqual(missing["kind"], "class_not_found")
            self.assertNotIn("kntr.a.B", str(missing))
            log.write_text("INFO quiet run\n", encoding="utf-8")
            self.assertEqual(analyze.decompile_failure(0, log)["kind"], "decompile_empty")
            self.assertEqual(analyze.decompile_failure(124, log)["kind"], "timeout")
            self.assertEqual(analyze.decompile_failure(1, Path(directory) / "missing.log")["kind"],
                             "command_failed")
        self.assertEqual(retry_policy.classify(["class_not_found"]), "deterministic")


class CliBackendTest(unittest.TestCase):
    def test_single_commands_never_guess_a_schema(self):
        self.assertEqual(analysis_plan.cli_backend("query"), {"backend": "sqlite",
                                                             "reason": "explicit_legacy_backend"})
        self.assertEqual(analysis_plan.cli_backend("decode", "dexsql"),
                         {"backend": "dexsql", "reason": "explicit_native_backend"})
        with self.assertRaisesRegex(ValueError, "unavailable"):
            analysis_plan.cli_backend("query", "dexsql", dexsql_available=False)
        for requested in ("auto", "", "DEXSQL"):
            with self.subTest(requested=requested), self.assertRaises(ValueError):
                analysis_plan.cli_backend("query", requested)
        with self.assertRaises(ValueError):
            analysis_plan.cli_backend("audit", "dexsql")


if __name__ == "__main__":
    unittest.main()
