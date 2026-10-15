"""Durable AI admission never hides unknown work or reuses a changed binding."""
import copy
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import ai_checkpoint as checkpoint


class CheckpointTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.binding = {"source_sha256": "a"*64, "policy": {
            "max_requests": 16, "transport_retries": 2, "deadline_seconds": 1800,
            "initial_profile": "primary", "allow_fallback": True, "max_output": 8192,
            "total_timeout": 240, "idle_timeout": 45, "stream": True}}

    def test_only_fixed_default_and_explicit_recovery_limits_are_supported(self):
        self.assertEqual(checkpoint.policy_limits(self.binding)["max_requests"], 16)
        extended = copy.deepcopy(self.binding)
        extended["policy"].update(max_requests=24, transport_retries=4, max_output=16384, recovery_policy="extended-v1")
        self.assertEqual(checkpoint.policy_limits(extended)["max_requests"], 24)
        for update in ({"max_requests": 17}, {"max_output": 16384}, {"transport_retries": 4},
                       {"recovery_policy": "extended-v2"}, {"deadline_seconds": 1801}, {"stream": 1}):
            value = copy.deepcopy(self.binding); value["policy"].update(update)
            with self.subTest(update=update), self.assertRaises(checkpoint.CheckpointError):
                checkpoint.policy_limits(value)

    def opened(self, **options):
        value = checkpoint.Checkpoint(self.root, self.binding, **options)
        self.addCleanup(value.close)
        return value

    def error(self):
        return SimpleNamespace(reason="API timeout", kind="timeout", retryable=True, billing_unknown=True,
            http_status=None, retry_after=2, metrics={"total_ms": 100, "first_event_ms": 20, "private_header": "secret"})

    def test_unknown_is_persisted_before_post_and_restart_needs_explicit_permission(self):
        value = self.opened()
        value.claim("draft", "d0", "b"*64, "primary", "session")
        saved = json.loads((self.root / "ai-checkpoint.json").read_text())
        self.assertEqual(saved["attempts"][0]["status"], "attempt_unknown")
        value.close()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "explicit"):
            self.opened()
        resumed = self.opened(resume_unknown=True)
        self.assertTrue(resumed.value["attempts"][0]["billing_unknown"])
        self.assertEqual(resumed.value["attempts"][0]["status"], "authorized_replay")
        resumed.claim("draft", "d0", "b"*64, "primary", "session")
        self.assertEqual(len(resumed.value["attempts"]), 2)

    def test_changed_source_binding_does_not_reuse_receipts(self):
        value = self.opened(); value.close()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "binding changed"):
            checkpoint.Checkpoint(self.root, {**self.binding, "source_sha256": "c"*64})

    def test_completed_response_and_unit_are_immutable_receipts(self):
        value = self.opened()
        token = value.claim("draft", "d0", "b"*64, "primary", "session")
        clean = {"role": "assistant", "content": None}
        value.received(token, "b"*64, clean, {"prompt_tokens": 2}, "model")
        unit = {"overview": "verified"}
        value.save_unit("d0", unit)
        unit["overview"] = "changed in caller"
        value.save()
        self.assertEqual(value.cached("b"*64)["clean"], clean)
        self.assertEqual(value.value["units"]["d0"]["result"]["overview"], "verified")

    def test_missing_usage_is_unknown_even_when_semantic_response_is_valid(self):
        value = self.opened()
        token = value.claim("draft", "d0", "b"*64, "primary", "session")
        value.received(token, "b"*64, {"role": "assistant", "content": None}, {"_usage_unknown": True}, "m")
        self.assertTrue(value.value["attempts"][0]["billing_unknown"])
        self.assertTrue(value.value["attempts"][0]["usage_unknown"])

    def test_failed_length_keeps_known_usage_but_never_backfills_old_unknown_calls(self):
        value = self.opened()
        old = value.claim("draft", "d0", "a"*64, "primary", "session")
        value.failed(old, self.error())
        original = copy.deepcopy(value.value["attempts"][0])
        token = value.claim("draft", "d0", "b"*64, "backup", "session")
        error = self.error()
        error.usage = {"prompt_tokens": 12, "completion_tokens": 8192, "private_body": "secret"}
        error.metrics["finish_reason"] = "length"
        value.failed(token, error)
        self.assertEqual(value.value["attempts"][0], original)
        saved = value.value["attempts"][-1]
        self.assertEqual(saved["usage"], {"prompt_tokens": 12, "completion_tokens": 8192})
        self.assertFalse(saved["usage_unknown"])
        self.assertFalse(saved["billing_unknown"])
        self.assertEqual(saved["metrics"]["finish_reason"], "length")

    def test_failed_zero_placeholders_or_auxiliary_usage_stay_unknown_after_restart(self):
        cases = (
            {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            {"prompt_tokens_details": {}, "completion_tokens_details": {}},
            {"prompt_tokens_details": {"cached_tokens": 0}, "server_counter": 5},
        )
        for usage in cases:
            with self.subTest(usage=usage), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                value = checkpoint.Checkpoint(root, self.binding)
                token = value.claim("draft", "d0", "b"*64, "primary", "session")
                error = self.error()
                error.usage = copy.deepcopy(usage)
                value.failed(token, error)
                row = value.value["attempts"][0]
                self.assertEqual(usage, row["usage"])
                self.assertTrue(row["usage_unknown"])
                self.assertTrue(row["billing_unknown"])
                value.close()
                resumed = checkpoint.Checkpoint(root, self.binding)
                try:
                    saved = resumed.value["attempts"][0]
                    self.assertEqual(usage, saved["usage"])
                    self.assertTrue(saved["usage_unknown"])
                    self.assertTrue(saved["billing_unknown"])
                finally:
                    resumed.close()

    def test_circuit_is_persistent_and_does_not_spend_retry_without_admission(self):
        value = self.opened()
        for index in range(2):
            token = value.claim("draft", "d0", format(index+1, "064x"), "primary", "session")
            value.failed(token, self.error())
        before = value.value["transport_retries"]
        with self.assertRaisesRegex(checkpoint.CheckpointError, "circuit"):
            value.claim("draft", "d0", "b"*64, "primary", "session", transport_retry=True)
        self.assertEqual(before, value.value["transport_retries"])
        value.close()
        resumed = self.opened()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "circuit"):
            resumed.claim("draft", "d0", "b"*64, "primary", "session")
        self.assertNotIn("private_header", resumed.value["attempts"][0]["metrics"])
        self.assertEqual(resumed.value["attempts"][0]["metrics"]["first_event_ms"], 20)
        with patch.object(checkpoint.time, "time", return_value=resumed.value["providers"]["primary"]["open_until"]+1):
            resumed.claim("draft", "d0", "c"*64, "primary", "session")
        self.assertEqual(resumed.value["attempts"][-1]["status"], "attempt_unknown")

    def test_global_request_cap_still_applies_after_restart(self):
        value = self.opened()
        for index in range(16):
            request = format(index+1, "064x")
            token = value.claim("draft", "d0", request, "primary", "session")
            value.received(token, request, {"role": "assistant", "content": None}, {"prompt_tokens": 1}, "m")
        value.close()
        resumed = self.opened()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "request budget"):
            resumed.claim("review", "r0", "e"*64, "primary", "other-session")

    def test_unit_digest_or_private_response_body_tampering_is_rejected(self):
        value = self.opened()
        token = value.claim("draft", "d0", "b"*64, "primary", "session")
        value.received(token, "b"*64, {"role": "assistant", "content": None}, {}, "m")
        value.save_unit("d0", {"overview": "verified"})
        changed = copy.deepcopy(value.value)
        changed["units"]["d0"]["result"]["overview"] = "tampered"
        with self.assertRaisesRegex(checkpoint.CheckpointError, "digest"):
            checkpoint.validate(changed)
        changed = copy.deepcopy(value.value)
        changed["responses"]["b"*64]["clean"]["content"] = "private source body"
        saved = changed["responses"]["b"*64]
        saved["response_sha256"] = checkpoint.digest({key: saved[key] for key in ("clean", "usage", "model")})
        with self.assertRaisesRegex(checkpoint.CheckpointError, "public"):
            checkpoint.validate(changed)

    def test_valid_shape_response_argument_or_usage_changes_fail_content_digest(self):
        value = self.opened()
        token = value.claim("draft", "d0", "b"*64, "primary", "session")
        clean = {"role": "assistant", "content": None, "tool_calls": [{"id": "finish-1", "type": "function",
            "function": {"name": "finish_report", "arguments": json.dumps({"overview": "original"})}}]}
        value.received(token, "b"*64, clean, {"total_tokens": 3}, "m")
        for kind in ("arguments", "usage"):
            changed = copy.deepcopy(value.value)
            saved = changed["responses"]["b"*64]
            if kind == "arguments":
                saved["clean"]["tool_calls"][0]["function"]["arguments"] = json.dumps({"overview": "changed"})
            else:
                saved["usage"]["total_tokens"] = 4
            with self.subTest(kind=kind), self.assertRaisesRegex(checkpoint.CheckpointError, "response content digest"):
                checkpoint.validate(changed)

    def test_accepted_unit_cannot_be_overwritten_by_a_different_replayed_result(self):
        value = self.opened()
        value.save_unit("d0", {"overview": "accepted"})
        before = value.path.read_bytes()
        value.save_unit("d0", {"overview": "accepted"})
        with self.assertRaisesRegex(checkpoint.CheckpointError, "unit changed"):
            value.save_unit("d0", {"overview": "different replay"})
        self.assertEqual(value.value["units"]["d0"]["result"], {"overview": "accepted"})
        # The harmless identical replay may advance elapsed time; a rejected
        # result must leave the last accepted disk receipt unchanged.
        accepted_bytes = value.path.read_bytes()
        with self.assertRaises(checkpoint.CheckpointError):
            value.save_unit("d0", {"overview": "another change"})
        self.assertEqual(value.path.read_bytes(), accepted_bytes)

    def test_crash_pending_request_reserves_active_time_on_authorized_resume(self):
        value = self.opened()
        value.claim("draft", "d0", "b"*64, "primary", "session")
        value.value["attempts"][0]["started_at"] -= 150
        value.save(); value.close()
        resumed = self.opened(resume_unknown=True)
        self.assertGreaterEqual(resumed.value["elapsed_seconds"], 150)

    def test_restoration_only_accepts_one_valid_public_ledger(self):
        value = self.opened(); value.close()
        source = self.root / "ai-checkpoint.json"
        target = self.root / "restored"
        restored = checkpoint.restore_checkpoint(target, [source])
        self.assertTrue(restored["restored"])
        with self.assertRaisesRegex(checkpoint.CheckpointError, "ambiguous"):
            checkpoint.restore_checkpoint(target, [source, target / "ai-checkpoint.json"])
        self.assertEqual(list(target.glob(".ai-checkpoint-*.tmp")), [])

    def test_global_transport_compensation_budget_survives_restart(self):
        value = self.opened()
        for index in range(2):
            request_hash = format(index+1, "064x")
            token = value.claim("draft", "d0", request_hash, "primary", "session", transport_retry=True)
            value.received(token, request_hash, {"role": "assistant", "content": None}, {"total_tokens": 1}, "m")
        value.close()
        resumed = self.opened()
        before = len(resumed.value["attempts"])
        with self.assertRaisesRegex(checkpoint.CheckpointError, "compensation"):
            resumed.claim("review", "r0", "e"*64, "backup", "session", transport_retry=True)
        self.assertEqual(resumed.value["transport_retries"], 2)
        self.assertEqual(len(resumed.value["attempts"]), before)

    def test_authorized_resume_retains_prior_time_and_only_reserves_one_request_deadline(self):
        with patch.object(checkpoint.time, "time", return_value=1000), patch.object(checkpoint.time, "monotonic", return_value=10):
            value = self.opened()
            value.record_elapsed(77)
            value.claim("draft", "d0", "b"*64, "primary", "session")
            value.close()
        with patch.object(checkpoint.time, "time", return_value=2000), patch.object(checkpoint.time, "monotonic", return_value=20):
            resumed = self.opened(resume_unknown=True)
            self.assertEqual(resumed.value["elapsed_seconds"], 77+240)
            self.assertEqual(len(resumed.value["attempts"]), 1)
            self.assertTrue(resumed.value["attempts"][0]["replay_authorized"])
            self.assertEqual(resumed.value["transport_retries"], 0)
            resumed.record_elapsed(15)
            resumed.close()
            another = self.opened()
            self.assertEqual(another.value["elapsed_seconds"], 77+240+15)

    def test_restore_rejects_missing_different_or_linked_public_ledgers(self):
        value = self.opened(); value.close()
        source = self.root/"ai-checkpoint.json"
        with self.assertRaisesRegex(checkpoint.CheckpointError, "ambiguous"):
            checkpoint.restore_checkpoint(self.root/"empty", [])
        target = self.root/"restored"
        checkpoint.restore_checkpoint(target, [source])
        changed = json.loads(source.read_text())
        changed["elapsed_seconds"] = 123
        checkpoint.atomic(target/"ai-checkpoint.json", changed)
        with self.assertRaisesRegex(checkpoint.CheckpointError, "different"):
            checkpoint.restore_checkpoint(target, [source])
        linked_root = self.root/"linked"; linked_root.mkdir()
        linked = linked_root/"ai-checkpoint.json"
        try:
            os.link(source, linked)
        except OSError as exc:
            self.skipTest("filesystem does not support hardlink fixture: "+type(exc).__name__)
        with self.assertRaisesRegex(checkpoint.CheckpointError, "unlinked"):
            checkpoint.restore_checkpoint(self.root/"linked-restore", [linked])


if __name__ == "__main__": unittest.main()
