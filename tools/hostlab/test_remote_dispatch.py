"""Versioned workflow dispatch, stable legacy receipts and monotonic status evidence."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import hostlab
import remote_dispatch
import remote_mcp
import remote_schedule


def request():
    return {"backend": "dexsql", "tasks": [{"id": "i", "operation": "info"}]}


class DispatchTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        p = patch.object(hostlab, "STATE", self.root); p.start(); self.addCleanup(p.stop)

    def test_new_api_returns_run_id_and_maps_without_run_list_discovery(self):
        def gh(args, payload=None):
            if payload is None:
                return json.dumps({"object": {"sha": "a"*40}})
            self.assertIn("X-GitHub-Api-Version: 2026-03-10", args)
            rid = payload["inputs"]["request_id"]
            saved = json.loads((self.root/"remote-requests"/(rid+".json")).read_text())
            self.assertEqual(saved["status"], "dispatch_unknown")
            self.assertIn("queued_at", saved)
            return json.dumps({"workflow_run_id": 123, "run_url": "https://api.github.com/unused"})
        result = remote_schedule.submit(9150200, request(), gh, lambda _: None, lambda: [],
            repository="owner/repo", workflow="host-analysis.yml")
        self.assertEqual(result["run_id"], 123)
        self.assertEqual(result["status"], "submitted")
        self.assertEqual(result["dispatch"]["response_kind"], "workflow_run_id")
        self.assertGreaterEqual(result["dispatch"]["elapsed_ms"], 0)
        with patch.object(remote_mcp, "runs", side_effect=AssertionError("unnecessary recent runs")), patch.object(
                remote_mcp, "gh", return_value=json.dumps({"id": 123, "status": "queued"})) as getter:
            remote_mcp.lookup(result["request_id"])
        self.assertTrue(getter.call_args.args[0][-1].endswith("/123"))

    def test_legacy_empty_response_remains_successful_and_does_not_fake_run_mapping(self):
        rid = "a"*32
        result = remote_dispatch.dispatch("owner/repo", "host-analysis.yml", {"request_id": rid}, Mock(return_value=""))
        self.assertTrue(result["dispatched"])
        self.assertEqual(result["dispatch"]["response_kind"], "legacy_empty")
        self.assertNotIn("run_id", result)
        self.assertFalse((self.root/"remote-job-map"/(rid+".json")).exists())

    def test_ambiguous_or_malformed_post_never_retries_and_always_returns_original_id(self):
        for response in ("not JSON", "{}", '{"workflow_run_id":true}', '{"workflow_run_id":0}', "[]"):
            sender = Mock(return_value=response)
            result = remote_dispatch.dispatch("owner/repo", "host-analysis.yml", {"request_id": "a"*32}, sender)
            self.assertEqual(result["request_id"], "a"*32)
            self.assertEqual(result["status"], "dispatch_unknown")
            self.assertIsNone(result["dispatched"])
            sender.assert_called_once()
        sender = Mock(side_effect=TimeoutError("private URL or credential must not appear"))
        result = remote_dispatch.dispatch("owner/repo", "host-analysis.yml", {"request_id": "b"*32}, sender)
        self.assertEqual(result["request_id"], "b"*32)
        self.assertNotIn("private URL", json.dumps(result))
        self.assertEqual(result["dispatch"]["error_type"], "TimeoutError")
        sender.assert_called_once()

    def test_legacy_submit_returns_stable_unknown_id_and_journals_before_post(self):
        def gh(args, payload=None):
            rid = payload["inputs"]["request_id"]
            saved = json.loads((self.root/"remote-requests"/(rid+".json")).read_text())
            self.assertEqual(saved["status"], "dispatch_unknown")
            raise TimeoutError("unknown outcome")
        with patch.object(remote_mcp, "gh", side_effect=gh):
            result = json.loads(remote_mcp.submit_job(9150200, "regenerate_ai", "123456"))
        self.assertEqual(result["status"], "dispatch_unknown")
        self.assertIsNone(result["dispatched"])
        self.assertTrue((self.root/"remote-requests"/(result["request_id"]+".json")).is_file())

    def test_legacy_new_response_and_missing_map_recover_from_receipt_without_listing(self):
        with patch.object(remote_mcp, "gh", return_value='{"workflow_run_id":123}'):
            result = json.loads(remote_mcp.submit_job(9150200, "query", "SELECT 1"))
        (self.root/"remote-job-map"/(result["request_id"]+".json")).unlink()
        with patch.object(remote_mcp, "runs", side_effect=AssertionError("unnecessary discovery")), patch.object(
                remote_mcp, "gh", return_value='{"id":123,"status":"queued"}'):
            observed = remote_mcp.lookup(result["request_id"])
        self.assertEqual(observed["id"], 123)


class ObservationTest(unittest.TestCase):
    def final(self):
        return {"request_id": "a"*32, "status": "completed", "conclusion": "success", "run_id": 123,
                "run_attempt": 1, "run_updated_at": "2026-10-15T12:01:00Z"}

    def test_older_same_attempt_status_and_lower_attempt_cannot_regress_completion(self):
        old = self.final()
        for run in ({"id": 123, "run_attempt": 1, "status": "queued", "updated_at": "2026-10-15T12:00:59Z"},
                    {"id": 123, "run_attempt": 1, "status": "pending", "updated_at": "2026-10-15T12:01:00Z"},
                    {"id": 123, "run_attempt": 0, "status": "queued"}):
            result = remote_schedule.reconcile(old, run)
            self.assertEqual(result["status"], "completed")
        result = remote_schedule.reconcile({**old, "run_attempt": 2},
            {"id": 123, "run_attempt": 1, "status": "queued", "updated_at": "2026-10-15T12:02:00Z"})
        self.assertEqual(result["run_attempt"], 2)
        self.assertFalse(remote_schedule.active_receipt(result))

    def test_real_higher_attempt_reopens_active_state_and_old_attempt_cannot_close_it(self):
        run = {"id": 123, "run_attempt": 2, "status": "in_progress", "updated_at": "2026-10-15T12:02:00Z"}
        result = remote_schedule.reconcile(self.final(), run)
        self.assertEqual(result["status"], "in_progress")
        self.assertEqual(result["run_attempt"], 2)
        self.assertTrue(remote_schedule.active_receipt(result))
        stale = remote_schedule.reconcile(result,
            {"id": 123, "run_attempt": 1, "status": "completed", "updated_at": "2026-10-15T12:01:00Z"})
        self.assertEqual(stale["status"], "in_progress")

    def test_missing_evidence_and_newer_unnumbered_active_observation_keep_a_slot(self):
        for run in ({"id": 123, "status": "pending"}, {"status": "queued"},
                    {"id": 123, "run_attempt": 1, "status": "queued", "updated_at": "2026-10-15T12:02:00Z"}):
            result = remote_schedule.reconcile(self.final(), run)
            self.assertEqual(result["status"], "completed")
            self.assertEqual(remote_schedule.public_status(result), "status_unconfirmed")
            self.assertTrue(remote_schedule.active_receipt(result))

    def test_public_legacy_status_is_monotonic_even_if_scheduler_lock_is_busy(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(hostlab, "STATE", Path(temporary)):
            old = self.final()
            hostlab.write_json(hostlab.STATE/"remote-requests"/(old["request_id"]+".json"), old)
            stale = {"id": 123, "run_attempt": 1, "status": "queued", "updated_at": "2026-10-15T12:00:59Z"}
            with patch.object(remote_mcp, "lookup", return_value=stale), patch.object(remote_schedule, "observe", return_value=None):
                status = json.loads(remote_mcp.job_status(old["request_id"]))
            self.assertEqual(status["status"], "completed")
            self.assertEqual(status["conclusion"], "success")
            self.assertTrue(status["stale_observation_ignored"])

    def test_admission_uses_reconciled_attempts_instead_of_stale_active_list_entries(self):
        for higher in (False, True):
            with self.subTest(higher_attempt=higher), tempfile.TemporaryDirectory() as temporary, patch.object(
                    hostlab, "STATE", Path(temporary)):
                observed = []
                for index in range(4):
                    rid = format(index+1, "032x")
                    receipt = {**self.final(), "request_id": rid, "run_id": index+1,
                               "status": "completed" if index == 0 else "queued"}
                    hostlab.write_json(hostlab.STATE/"analysis-schedule"/(str(index)+".json"), receipt)
                    observed.append({"id": index+1, "display_title": "hostlab-"+rid, "status": "pending",
                        "run_attempt": 2 if higher and index == 0 else 1,
                        "updated_at": "2026-10-15T12:02:00Z" if higher else "2026-10-15T12:00:59Z"})
                sender = Mock(return_value="")
                result = remote_schedule.submit(9150200, request(), sender, lambda _: None, lambda: observed,
                    repository="owner/repo", workflow="host-analysis.yml", runner_revision="a"*40)
                if higher:
                    self.assertEqual(result["status"], "capacity_full")
                    sender.assert_not_called()
                else:
                    self.assertEqual(result["status"], "submitted")
                    sender.assert_called_once()


if __name__ == "__main__": unittest.main()
