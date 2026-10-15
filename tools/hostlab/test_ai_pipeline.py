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
import ai_recovery
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

    def test_forced_submission_only_offers_the_finish_tool(self):
        offered = []
        def api(profile, messages, tools, **options):
            if options.get("force_tool"):
                offered.append([row["function"]["name"] for row in tools])
                self.assertEqual(offered[-1], [options["force_tool"]])
            return self.provider(profile, messages, tools, **options)
        with patch.object(ai_review, "call_api", side_effect=api):
            ai_review.run(self.root)
        self.assertTrue(offered)

    def test_missing_review_finding_id_has_precise_feedback_and_retains_validation(self):
        corrupted = False
        observed_feedback = []
        def api(*args, **options):
            nonlocal corrupted
            messages = args[1]
            observed_feedback.extend(row["content"] for row in messages if row["role"] == "tool")
            message, usage, model = self.provider(*args, **options)
            for call in message.get("tool_calls", []):
                if call["function"]["name"] == "finish_review" and not corrupted:
                    data = json.loads(call["function"]["arguments"])
                    for row in data["findings"]:
                        row.pop("finding_id")
                    call["function"]["arguments"] = json.dumps(data)
                    corrupted = True
            return message, usage, model
        with patch.object(ai_review, "call_api", side_effect=api):
            ai_review.run(self.root)
        outcome = json.loads((self.root / "ai-analysis.json").read_text())
        self.assertEqual(outcome["status"], "completed")
        self.assertTrue(any("requires a non-empty finding_id" in value and "F001" in value for value in observed_feedback))
        self.assertFalse(any("TypeError" in value for value in observed_feedback))
        self.assertEqual(len(outcome["review"]["findings"]), 4)

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

    def test_schemas_bound_values_to_the_assigned_matrix_without_oneof(self):
        matrix = {"home": {"paths": {"home_new": {"evidence": "static_invoke_observed"}}},
                  "search": {"paths": {"search_native": {"evidence": "absent"}}}}
        schema = ai_pipeline.draft_tool(3, matrix)["function"]["parameters"]
        page = schema["properties"]["pages"]["items"]["properties"]
        paths = page["path_reviews"]["items"]["properties"]
        finding = schema["properties"]["findings"]["items"]["properties"]
        self.assertEqual(page["page"]["enum"], ["home", "search"])
        self.assertEqual(paths["path"]["enum"], ["home_new", "search_native"])
        self.assertEqual(paths["status"]["enum"], ["static_invoke_observed", "absent"])
        self.assertNotIn("search_kotlin_moss", paths["path"]["enum"])
        self.assertEqual(set(finding["level"]["enum"]), ai_review.CLAIM_LEVELS)
        self.assertNotIn("info", finding["level"]["enum"])
        review = ai_pipeline.review_tool({"pages": ["search"], "findings": ["F003"]})["function"]["parameters"]
        item = review["properties"]["findings"]["items"]["properties"]
        self.assertEqual(item["finding_id"]["enum"], ["F003"])
        self.assertEqual(set(item["disposition"]["enum"]), {"retained", "revised", "rejected", "needs_more_evidence"})
        self.assertEqual(set(item["revision"]["properties"]["level"]["enum"]), ai_review.CLAIM_LEVELS)
        self.assertNotIn("oneOf", json.dumps([schema, review]))

    def extended_fixture(self, *, invalid_import=False):
        """A real public ledger shape: nine billed/unknown calls, four reads, two units."""
        origin = self.root / "origin"; origin.mkdir()
        for name in ("priority-summary.json", "priority-target.json", "priority-baseline.json", "priority-report.md"):
            (origin/name).write_bytes((self.root/name).read_bytes())
        summary = json.loads((origin/"priority-summary.json").read_text())
        counts = {"comment": 5, "dynamic": 3, "home": 2, "search": 2, "player": 2,
                  "follow": 2, "space": 2, "setting": 2, "download": 2, "other": 3}
        summary["page_path_matrix"] = {page: {"paths": {page+"_"+str(index):
            {"evidence": "static_invoke_observed"} for index in range(count)}, "protocols": {}}
            for page, count in counts.items()}
        (origin/"static-manifest.json").write_text("{}", encoding="utf-8")
        summary["static_manifest_sha256"] = ai_pipeline.hostlab.digest(origin/"static-manifest.json")
        (origin/"priority-summary.json").write_text(json.dumps(summary), encoding="utf-8")
        evidence = ai_review.Evidence(origin, summary)
        ai_review.prefetch_evidence(evidence, summary)
        for name, args in [("family_evidence", {"family": "comment_0", "side": "target"}),
                ("protocol_evidence", {"protocol": "comment_java_moss", "side": "target"}),
                ("family_evidence", {"family": "search_0", "side": "target"}),
                ("protocol_evidence", {"protocol": "search_kotlin_moss", "side": "target"})]:
            evidence.run_tool(name, args)
        units = ai_pipeline.draft_units(summary["page_path_matrix"])
        binding = ai_pipeline.build_binding(origin, summary, units)
        ledger = ai_checkpoint.Checkpoint(origin, binding)
        ids = fixtures.page_evidence_ids(origin)
        for index in range(9):
            unit = "d0" if index < 3 else "d1" if index < 8 else "d2"
            token = ledger.claim("draft", unit, f"{index+1:064x}", "primary" if index == 0 else "backup",
                                 "old-session", transport_retry=index in (1, 5))
            if index in (0, 4, 8):
                ledger.failed(token, ai_transport.ApiError("API timeout", "timeout", True, True))
            else:
                clean = ai_pipeline.public_reply(response("finish_report", {"overview": "old public receipt"})[0])
                ledger.received(token, f"{index+1:064x}", clean, {"total_tokens": 20}, "test-model")
        for index, pages in enumerate(units[:2]):
            value = self.matrix_report(summary, pages, ids, count=3, deep="E011" if index == 0 else None)
            if invalid_import and index == 1:
                value["pages"][0]["path_reviews"] = value["pages"][0]["path_reviews"][:1]
            ledger.save_unit("d"+str(index), value)
        ledger.value["elapsed_seconds"] = 485.0
        ai_checkpoint.atomic(ledger.path, ledger.value)
        ledger.close()
        (origin/"ai-evidence.json").write_text(json.dumps({"E000": ai_pipeline.seed_for(summary),
            "tools": evidence.public_journal()}), encoding="utf-8")
        target = self.root / "recovery"; target.mkdir()
        for name in ("priority-summary.json", "priority-target.json", "priority-baseline.json", "priority-report.md", "static-manifest.json"):
            (target/name).write_bytes((origin/name).read_bytes())
        inputs = ai_recovery.restore_inputs(target, [str(origin/"ai-checkpoint.json"), str(origin/"ai-evidence.json")], 123)
        summary.update(ai_recovery_policy="extended-v1", ai_recovery_inputs=inputs, checkpoint_from_run=123)
        (target/"priority-summary.json").write_text(json.dumps(summary), encoding="utf-8")
        return target, summary, json.loads((origin/"ai-checkpoint.json").read_text())

    @staticmethod
    def matrix_report(summary, pages, ids, *, count=1, deep=None):
        value = {"overview": "static only; runtime unknown", "pages": [], "findings": [], "next_steps": ["verify actual entry"]}
        for page in pages:
            value["pages"].append({"page": page, "assessment": "static comparison only", "evidence_ids": [ids[page]],
                "path_reviews": [{"path": path, "status": row["evidence"], "change": "unknown", "impact": "unknown",
                    "verification": "verify actual entry", "evidence_ids": [ids[page]]}
                    for path, row in summary["page_path_matrix"][page]["paths"].items()]})
        value["findings"] = [{"title": pages[0]+str(index), "page": pages[0], "level": "needs_runtime",
            "analysis": "runtime condition unknown", "alternatives": "disabled branch", "recommendation": "verify actual entry",
            "evidence_ids": [deep or ids[pages[0]]]} for index in range(count)]
        return value

    def test_extended_recovery_preserves_nine_calls_and_completes_eight_units_then_replays_without_posts(self):
        target, summary, original = self.extended_fixture()
        seen = []
        def api(profile, messages, tools, force_tool=None, session_id=None, **options):
            seen.append(copy.deepcopy(messages))
            self.assertEqual(profile, "backup")
            self.assertEqual(options["max_output"], 16384)
            self.assertLessEqual(options["total_timeout"], 240)
            data = json.loads(messages[1]["content"])
            if len(seen) == 1:
                current = json.loads((target/"ai-checkpoint.json").read_text())
                self.assertEqual(current["transport_retries"], 3)
                self.assertTrue(current["attempts"][-1]["transport_retry"])
                self.assertEqual(current["attempts"][-1]["unit"], "d2")
            ids = {row["page"]: row["evidence_id"] for row in data["prefetch"]}
            if "assigned_findings" in data:
                fresh = data["fresh_refresh"]
                return response("finish_review", {"pages": [{"page": page, "assessment": "independent static review",
                    "evidence_ids": [fresh.get(page, ids[page])]} for page in data["assigned_pages"]],
                    "findings": [{"finding_id": row["finding_id"], "disposition": "retained", "reason": "runtime unknown",
                        "evidence_ids": row["evidence_ids"]} for row in data["draft"]["findings"]], "remaining_gaps": ["verify runtime"]})
            self.assertNotIn("comment", data["assigned_pages"])
            self.assertNotIn("home", data["assigned_pages"])
            return response("finish_report", self.matrix_report(summary, data["assigned_pages"], ids))
        with patch.object(ai_review, "call_api", side_effect=api):
            ai_review.run(target)
            first = json.loads((target/"ai-analysis.json").read_text())
            ai_review.run(target)
        self.assertEqual(len(seen), 8)
        self.assertEqual(first["new_model_requests"], 8)
        self.assertEqual(first["limits"]["hard_cap"], 24)
        self.assertEqual(first["limits"]["transport_retry_allowance"], 4)
        self.assertEqual(first["limits"]["review_logical_units"], 5)
        self.assertEqual(first["reused_units"], 2)
        self.assertEqual(first["imported_units"], 2)
        self.assertEqual(first["read_tool_calls"], 4)
        self.assertEqual(len(first["report"]["pages"]), 10)
        self.assertEqual(sum(len(page["path_reviews"]) for page in first["report"]["pages"]), 25)
        final = json.loads((target/"ai-analysis.json").read_text())
        self.assertEqual(final["status"], "completed")
        self.assertEqual(final["new_model_requests"], 0)
        self.assertEqual(final["cached_responses_reused"], 8)
        saved = json.loads((target/"ai-checkpoint.json").read_text())
        self.assertEqual(saved["attempts"][:9], original["attempts"])
        self.assertEqual(saved["units"]["d0"], original["units"]["d0"])
        self.assertEqual(saved["units"]["d1"], original["units"]["d1"])
        self.assertEqual(len(saved["attempts"]), 17)
        self.assertEqual(saved["transport_retries"], 3)
        self.assertGreaterEqual(saved["elapsed_seconds"], 485)
        self.assertTrue(final["usage_unknown"])
        review_messages = [json.loads(rows[1]["content"]) for rows in seen if "assigned_findings" in json.loads(rows[1]["content"])]
        self.assertEqual(len(review_messages), 5)
        self.assertEqual(set(review_messages[0]["fresh_refresh"]), {"comment", "dynamic"})

    def test_invalid_imported_unit_fails_before_any_new_request(self):
        target, _, original = self.extended_fixture(invalid_import=True)
        origin_bytes = (target/"ai-resume-checkpoint.json").read_bytes()
        with patch.object(ai_review, "call_api") as api:
            with self.assertRaises(RuntimeError):
                ai_review.run(target)
        api.assert_not_called()
        self.assertEqual((target/"ai-resume-checkpoint.json").read_bytes(), origin_bytes)
        saved = json.loads((target/"ai-checkpoint.json").read_text())
        self.assertEqual(saved["attempts"], original["attempts"])
        self.assertEqual(saved["transport_retries"], 2)
        self.assertTrue(saved["recovery"]["resume_transport_retry_pending"])

    def test_extended_policy_needs_verified_checkpoint_and_unknown_policy_is_rejected(self):
        for policy in ("extended-v1", "extended-v2"):
            with self.subTest(policy=policy):
                summary = json.loads((self.root/"priority-summary.json").read_text())
                summary["ai_recovery_policy"] = policy
                (self.root/"priority-summary.json").write_text(json.dumps(summary), encoding="utf-8")
                with patch.object(ai_review, "call_api") as api:
                    with self.assertRaises(RuntimeError):
                        ai_review.run(self.root)
                api.assert_not_called()


if __name__ == "__main__": unittest.main()
