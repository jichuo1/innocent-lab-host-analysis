"""Shard coverage, private-source boundaries and cost-free checkpoint replay."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ai_pipeline
import ai_checkpoint
import ai_transport
import ai_review
import test_ai_review as fixtures

report, response = fixtures.report, fixtures.response


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = fixtures.DetailedReviewTest().root(self.temp.name)
        summary = json.loads((self.root / "priority-summary.json").read_text())
        for page in ("home", "player"):
            summary["page_path_matrix"][page] = {"paths": {page+"_native": {"evidence": "static_invoke_observed"}}, "protocols": {}}
        summary["ai_no_apk_access"] = True
        (self.root / "priority-summary.json").write_text(json.dumps(summary), encoding="utf-8")
        self.messages = []; self.responses = 0
        self.addCleanup(patch.stopall)
        patch("sys.stdout", new_callable=io.StringIO).start()

    def provider(self, profile, messages, tools, force_tool=None, session_id=None, **options):
        self.messages.append(copy.deepcopy(messages)); self.responses += 1
        data = json.loads(messages[1]["content"])
        if self.responses == 1:
            first = response("family_evidence", {"family": "comment_native", "side": "target"})[0]
            second = response("protocol_evidence", {"protocol": "comment_java_moss", "side": "target"})[0]["tool_calls"][0]
            second["id"] = "second"
            first["tool_calls"].append(second)
            return first, {}, "test-model"
        if "assigned_findings" in data:
            fresh = data["fresh_refresh"]
            ids = {row["page"]: row["evidence_id"] for row in data["prefetch"]}
            value = {"pages": [{"page": page, "assessment": "independently checked; runtime unknown",
                "evidence_ids": [fresh.get(page, ids.get(page))]} for page in data["assigned_pages"]],
                "findings": [{"finding_id": row["finding_id"], "disposition": "retained", "reason": "static evidence only",
                    "evidence_ids": row["evidence_ids"]} for row in data["draft"]["findings"]], "remaining_gaps": ["runtime unknown"]}
            return response("finish_review", value)
        pages = data["assigned_pages"]
        ids = {row["page"]: row["evidence_id"] for row in data["prefetch"]}
        value = report(ids, pages, finding=False)
        page = "comment" if "comment" in pages else pages[0]
        for index in range(3 if page == "comment" else 1):
            value["findings"].append({"title": page+str(index), "page": page, "level": "needs_runtime",
                "analysis": "runtime condition unknown", "alternatives": "disabled branch", "recommendation": "verify actual entry",
                "evidence_ids": ["E005" if page == "comment" else ids[page]]})
        return response("finish_report", value)

    def test_four_pages_complete_and_replay_uses_no_new_model_calls(self):
        with patch.object(ai_review, "call_api", side_effect=self.provider) as api:
            ai_review.run(self.root)
            first_count = api.call_count
            ai_review.run(self.root)
            self.assertEqual(api.call_count, first_count)
        outcome = json.loads((self.root / "ai-analysis.json").read_text())
        self.assertEqual(outcome["status"], "completed")
        self.assertGreater(outcome["cached_responses_reused"], 0)
        self.assertEqual(len(outcome["report"]["pages"]), 4)
        self.assertEqual(len(outcome["review"]["findings"]), 4)
        self.assertEqual(outcome["read_tool_calls"], 2)
        self.assertEqual((self.root / "priority-report.md").read_text().count("# AI 适配分析"), 1)

    def test_primary_auth_rejection_switches_credentials_once_and_keeps_accounting(self):
        profiles = []
        def api(profile, *args, **options):
            profiles.append(profile)
            if profile == "primary":
                raise ai_transport.ApiError("API HTTP 401", "http", False, True, http_status=401)
            return self.provider(profile, *args, **options)
        with patch.dict("os.environ", {"AI_ALLOW_FALLBACK": "true", "AI_DEFAULT_PROFILE": "primary"}), \
             patch.object(ai_review, "call_api", side_effect=api), patch.object(ai_pipeline.time, "sleep"):
            ai_review.run(self.root)
            calls = len(profiles)
            ai_review.run(self.root)
        self.assertEqual(len(profiles), calls)
        self.assertEqual(profiles.count("primary"), 1)
        self.assertTrue(all(profile == "backup" for profile in profiles[1:]))
        outcome = json.loads((self.root / "ai-analysis.json").read_text())
        self.assertEqual(outcome["status"], "completed")
        self.assertEqual(outcome["attempts"][0]["credential_fallback"], "primary_to_backup")
        self.assertTrue(outcome["attempts"][0]["billing_unknown"])
        self.assertEqual(json.loads((self.root / "ai-checkpoint.json").read_text())["transport_retries"], 1)

    def test_both_auth_rejections_stop_without_repeating_either_profile(self):
        profiles = []
        def api(profile, *args, **options):
            profiles.append(profile)
            raise ai_transport.ApiError("API HTTP 401", "http", False, True, http_status=401)
        with patch.dict("os.environ", {"AI_ALLOW_FALLBACK": "true", "AI_DEFAULT_PROFILE": "primary"}), \
             patch.object(ai_review, "call_api", side_effect=api), patch.object(ai_pipeline.time, "sleep"):
            with self.assertRaises(RuntimeError): ai_review.run(self.root)
        self.assertEqual(profiles, ["primary", "backup"])
        self.assertEqual(json.loads((self.root / "ai-analysis.json").read_text())["status"], "failed")

    def test_disabled_fallback_does_not_try_another_credential(self):
        with patch.dict("os.environ", {"AI_ALLOW_FALLBACK": "false", "AI_DEFAULT_PROFILE": "primary"}), \
             patch.object(ai_review, "call_api", side_effect=ai_transport.ApiError(
                 "API HTTP 403", "http", False, True, http_status=403)) as api:
            with self.assertRaises(RuntimeError): ai_review.run(self.root)
        self.assertEqual(api.call_count, 1)

    def test_unknown_billing_is_retained_and_no_apk_tool_is_offered(self):
        offered = []
        def api(*args, **kwargs):
            offered.extend(tool["function"]["name"] for tool in args[2])
            return self.provider(*args, **kwargs)
        with patch.object(ai_review, "call_api", side_effect=api), patch.object(ai_review.subprocess, "run") as process:
            ai_review.run(self.root)
        self.assertNotIn("decompile_class", offered)
        process.assert_not_called()
        outcome = json.loads((self.root / "ai-analysis.json").read_text())
        self.assertTrue(outcome["usage_unknown"])
        self.assertTrue(all(row["usage_unknown"] for row in outcome["attempts"]))

    def test_same_nonpriority_page_findings_are_reviewed_exactly_once(self):
        draft = {"findings": [{"finding_id": "F"+str(index), "page": "player"} for index in range(3)]}
        units = ai_pipeline.review_units(["comment", "dynamic"], draft)
        ids = [finding for unit in units for finding in unit["findings"]]
        self.assertEqual(ids, ["F0", "F1", "F2"])
        self.assertEqual(len(units), 2)

    def test_nested_provider_private_fields_never_enter_public_receipts(self):
        value = report({"comment": "E001"}, ["comment"], finding=False)
        value["pages"][0]["source"] = "private source body"
        value["pages"][0]["path_reviews"][0]["messages"] = "private source body"
        value["findings"] = [{"title": "bounded", "source": "private source body", "assessment": {"source": "private source body"}}]
        clean = ai_pipeline.public_reply(response("finish_report", value)[0])
        self.assertNotIn("private source body", json.dumps(clean))
        wrong = ai_pipeline.public_reply(response("module_source", {"path": {"source": "private source body"}})[0])
        self.assertNotIn("private source body", json.dumps(wrong))

    def test_source_candidates_are_bounded_per_page_without_changing_the_reader_allowlist(self):
        summary = json.loads((self.root / "priority-summary.json").read_text())
        summary["source_snapshot"]["source_records"] = [{"path": f"private/{index}.kt", "pages": ["home"], "markers": []}
            for index in range(669)] + [{"path": "private/Comment.kt", "pages": ["comment"], "markers": []}]
        seed = ai_pipeline.seed_for(summary)
        local = ai_pipeline.unit_seed(seed, summary, ["comment"])
        self.assertEqual(local["source_files"], ["private/Comment.kt"])
        self.assertEqual(local["source_files_total"], 670)
        self.assertEqual(len(summary["source_snapshot"]["source_records"]), 670)

    def test_provider_timeouts_stop_with_two_compensations_and_keep_unknown_receipts(self):
        with patch.object(ai_review, "call_api", side_effect=RuntimeError("API failure: TimeoutError")) as api, \
             patch.object(ai_pipeline.time, "sleep"):
            with self.assertRaises(RuntimeError): ai_review.run(self.root)
        outcome = json.loads((self.root / "ai-analysis.json").read_text())
        self.assertLessEqual(api.call_count, 3)
        self.assertTrue(all(row["billing_unknown"] for row in outcome["attempts"]))
        self.assertEqual(outcome["status"], "failed")

    def test_omitted_unit_page_is_rejected_and_cannot_complete(self):
        def api(*args, **kwargs):
            message, usage, model = self.provider(*args, **kwargs)
            for call in message.get("tool_calls", []):
                if call["function"]["name"] == "finish_report":
                    payload = json.loads(call["function"]["arguments"])
                    payload["pages"] = payload["pages"][:1]
                    call["function"]["arguments"] = json.dumps(payload)
            return message, usage, model
        with patch.object(ai_review, "call_api", side_effect=api):
            with self.assertRaises(RuntimeError): ai_review.run(self.root)
        self.assertEqual(json.loads((self.root / "ai-analysis.json").read_text())["status"], "failed")

    def test_input_binding_drift_refuses_replay_before_any_model_request(self):
        with patch.object(ai_review, "call_api", side_effect=self.provider):
            ai_review.run(self.root)
        with (self.root / "priority-target.json").open("a") as stream:
            stream.write("\n")
        with patch.object(ai_review, "call_api") as api:
            with self.assertRaises(RuntimeError): ai_review.run(self.root)
        api.assert_not_called()
        self.assertEqual(json.loads((self.root / "ai-analysis.json").read_text())["status"], "failed")

    def test_pending_receipt_blocks_replay_without_hiding_unknown_accounting(self):
        summary = json.loads((self.root / "priority-summary.json").read_text())
        binding = ai_pipeline.build_binding(self.root, summary, ai_pipeline.draft_units(summary["page_path_matrix"]))
        ledger = ai_checkpoint.Checkpoint(self.root, binding)
        ledger.claim("draft", "d0", "b"*64, "primary", "session")
        ledger.close()
        with patch.object(ai_review, "call_api") as api:
            with self.assertRaises(RuntimeError): ai_review.run(self.root)
        api.assert_not_called()
        outcome = json.loads((self.root / "ai-analysis.json").read_text())
        self.assertEqual(outcome["model_requests"], 1)
        self.assertEqual(outcome["new_model_requests"], 0)
        self.assertTrue(outcome["usage_unknown"])
        self.assertTrue(outcome["checkpoint"]["resume_blocked"])

    def test_merged_steps_and_gaps_preserve_every_unique_full_string_at_the_limit(self):
        for limit, total in ((12, 35), (20, 61)):
            with self.subTest(limit=limit):
                originals = [f"独立完整条目 {index}: 不得丢弃正文 END-{index}" for index in range(total)]
                merged, count = ai_pipeline.merge_items(originals+originals[:3], limit)
                self.assertEqual(count, total)
                self.assertLessEqual(len(merged), limit)
                for original in originals:
                    self.assertEqual("\n".join(merged).count(original), 1)
                self.assertEqual((merged, count), ai_pipeline.merge_items(originals, limit))


if __name__ == "__main__": unittest.main()
