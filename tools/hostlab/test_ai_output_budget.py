"""64k model output must survive transport, public receipts and explicit recovery."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ai_checkpoint as checkpoint
import ai_pipeline
import ai_recovery
import ai_review
import ai_transport
import probe_ai_generation
import remote_artifacts
from test_ai_transport import Response, ENV, delta, event


class OutputBudgetTest(unittest.TestCase):
    def test_all_new_review_and_recovery_forms_use_64k_with_original_call_limits(self):
        for recovery, calls, retries in ((None, 16, 2), ("extended-v1", 24, 4),
                                         ("completion-v2", 32, 4), ("completion-v3", 40, 6)):
            summary = {"ai_recovery_policy": recovery} if recovery else {}
            policy = ai_pipeline.execution_policy(summary)
            self.assertEqual(policy["max_output"], 65536)
            self.assertEqual(policy["max_requests"], calls)
            self.assertEqual(policy["transport_retries"], retries)
            self.assertEqual(checkpoint.policy_limits({"policy": policy}), policy)
        self.assertEqual(ai_review.MAX_OUTPUT, 65536)
        self.assertTrue(all(tokens == 8192 for _, tokens in probe_ai_generation.STAGES))

    def test_versioned_budget_rejects_unbounded_or_mismatched_caps(self):
        policy = ai_pipeline.execution_policy({})
        for change in ({"max_output": 65537}, {"max_output": 8192}, {"output_budget": "unknown"},
                       {"max_requests": 17}, {"total_timeout": 601}):
            value = {**policy, **change}
            with self.subTest(change=change), self.assertRaises(checkpoint.CheckpointError):
                checkpoint.policy_limits({"policy": value})

    def test_large_unicode_tool_output_survives_sse_and_checkpoint_reload(self):
        arguments = json.dumps({"overview": "中文"*60000}, ensure_ascii=False)
        raw = delta({"tool_calls": [{"index": 0, "id": "finish", "type": "function",
            "function": {"name": "finish_report", "arguments": arguments}}]}, "tool_calls") + event(b"[DONE]")
        response = Response(raw, chunk_size=32768)
        with patch.dict("os.environ", ENV), patch.object(ai_transport.urllib.request, "build_opener") as build:
            build.return_value.open.return_value = response
            message, usage, model = ai_transport._call_api("primary", [], [])
            self.assertEqual(json.loads(build.return_value.open.call_args.args[0].data)["max_tokens"], 65536)
        self.assertEqual(message["tool_calls"][0]["function"]["arguments"], arguments)
        with tempfile.TemporaryDirectory() as folder:
            binding = {"policy": ai_pipeline.execution_policy({})}
            ledger = checkpoint.Checkpoint(Path(folder), binding)
            try:
                token = ledger.claim("draft", "d0", "b"*64, "primary", "session")
                ledger.received(token, "b"*64, ai_pipeline.public_reply(message), {"total_tokens": 65536}, model)
            finally:
                ledger.close()
            saved = json.loads((Path(folder)/"ai-checkpoint.json").read_text(encoding="utf-8"))
            checkpoint.validate(saved)
            self.assertEqual(saved["responses"]["b"*64]["clean"], message)
            self.assertEqual(saved["attempts"][0]["usage"]["total_tokens"], 65536)

    def test_large_checkpoint_artifact_limit_matches_ledger_limit_only_for_allowlisted_paths(self):
        limits = remote_artifacts.limits("frozen-report-v1")
        self.assertEqual(remote_artifacts.file_limit("remote-output/ai-checkpoint.json", limits), checkpoint.MAX_BYTES)
        self.assertEqual(remote_artifacts.file_limit("remote-output/unrelated.json", limits), limits["file_bytes"])

    def test_original_static_binding_can_only_gain_a_verified_manifest_and_disable_apk_access(self):
        old = {"schema": 1, "static_files": {"priority-target.json": "a"*64},
               "static_manifest_sha256": None, "sample": {}, "baseline": None, "no_apk_access": False,
               "code": {name: "b"*64 for name in ai_recovery.BOUND_CODE},
               "policy": {"max_requests": 16, "transport_retries": 2, "deadline_seconds": 1800,
                   "initial_profile": "primary", "allow_fallback": True, "max_output": 8192,
                   "total_timeout": 240, "idle_timeout": 45, "stream": True}}
        new = copy.deepcopy(old)
        new.update(no_apk_access=True, static_manifest_sha256="c"*64)
        new["static_files"]["static-manifest.json"] = "c"*64
        new["policy"] = ai_pipeline.execution_policy({"ai_recovery_policy": "extended-v1"})
        ai_recovery._binding(old, new)
        old["code"]["ai_review.py"], new["code"]["ai_review.py"] = ai_recovery.FROZEN_REVIEWER_MIGRATION
        ai_recovery._binding(old, new)
        for field, value in (("no_apk_access", False), ("static_manifest_sha256", "d"*64), ("sample", {"changed": True})):
            changed = copy.deepcopy(new); changed[field] = value
            with self.subTest(field=field), self.assertRaises(checkpoint.CheckpointError):
                ai_recovery._binding(old, changed)
        changed = copy.deepcopy(new); changed["code"]["ai_review.py"] = "e"*64
        with self.assertRaises(checkpoint.CheckpointError):
            ai_recovery._binding(old, changed)


if __name__ == "__main__":
    unittest.main()
