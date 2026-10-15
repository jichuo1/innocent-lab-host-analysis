from __future__ import annotations

import contextlib
from email.message import Message
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error

import check_ai_connectivity as catalog
import probe_ai_generation as probe


SECRET = "rv_PRIVATE_CREDENTIAL_SENTINEL"
PRIVATE = "PRIVATE_RESPONSE_SENTINEL"
ENV = {"AI_API_KEY_PRIMARY": SECRET, "AI_PRIMARY_BASE_URL": "https://api.river.ai/v1", "AI_PRIMARY_MODEL": "deepseek-ai/DeepSeek-V4.1-Flash", "AI_API_KEY_BACKUP": "sk_BACKUP_SENTINEL", "AI_BACKUP_BASE_URL": "https://backup.example/v1", "AI_BACKUP_MODEL": "other-model"}


class Response(io.BytesIO):
    def __init__(self, data, content_type="application/json", chunk=8192):
        super().__init__(data)
        self.headers = {"Content-Type": content_type, "x-request-id": "req-diagnostic-1"}
        self.status = 200
        self.chunk = chunk

    def read1(self, size=-1):
        return self.read(min(size, self.chunk))


def completion(content="pong", finish="stop", usage=True, calls=None):
    row = {"choices": [{"index": 0, "finish_reason": finish, "message": {"content": content, "reasoning_content": PRIVATE, "tool_calls": calls or []}}], "model": PRIVATE}
    if usage:
        row["usage"] = {"prompt_tokens": 20, "completion_tokens": 2, "total_tokens": 22, PRIVATE: 900, "note": SECRET}
    return json.dumps(row).encode()


def tool_call(arguments='{"ok":true}'):
    return {"id": "call-probe-1", "type": "function", "function": {"name": probe.TOOL_NAME, "arguments": arguments}}


class AiDiagnosticsTest(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, ENV, clear=True)
        env.start()
        self.addCleanup(env.stop)
        guard = patch.object(catalog.urllib.request, "build_opener", side_effect=AssertionError("unmocked network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.output = Path(temp.name)

    def assert_private_absent(self, value):
        text = json.dumps(value)
        for secret in (SECRET, PRIVATE, ENV["AI_API_KEY_BACKUP"]):
            self.assertNotIn(secret, text)

    def attempt_with(self, response, stage="minimal_chat", include_usage=True):
        opener = Mock()
        opener.open.return_value = response
        with patch.object(probe.urllib.request, "build_opener", return_value=opener):
            result = probe.attempt("primary", stage, 5, include_usage)
        self.assert_private_absent(result)
        return result, opener

    def test_credential_shape_is_boolean_only_and_prefix_is_advisory(self):
        shape = catalog.credential_shape(' "Bearer ' + SECRET + '"\n')
        self.assertTrue(all(type(value) is bool for value in shape.values()))
        self.assertTrue(shape["padding"])
        self.assertTrue(shape["control"])
        self.assertTrue(shape["quoted"])
        self.assertTrue(catalog.credential_shape("Bearer abc")["bearer_prefix"])
        with patch.dict(os.environ, {"AI_API_KEY_PRIMARY": "legacy_credential"}):
            self.assertEqual("legacy_credential", catalog.configuration("primary")["key"])
        self.assert_private_absent(shape)

    def test_config_reads_current_variables_and_rejects_unsafe_urls(self):
        with patch.dict(os.environ, {"AI_PRIMARY_BASE_URL": "https://api.river.ai/v1/chat/completions"}):
            self.assertEqual("https://api.river.ai/v1", catalog.configuration("primary")["base"])
        for value in ("http://api.river.ai/v1", "https://u:p@api.river.ai/v1", "https://api.river.ai/v1?key=x", "https://api.river.ai/v1#x"):
            with self.subTest(url=value), patch.dict(os.environ, {"AI_PRIMARY_BASE_URL": value}):
                with self.assertRaises(ValueError):
                    catalog.configuration("primary")

    def test_catalog_raw_key_preserved_and_padding_has_only_one_explicit_variant(self):
        raw = " " + SECRET + " "
        calls = []
        def request(url, key=None):
            calls.append((url, key))
            if key == raw:
                return {"http": 401}, None
            if key is None:
                return {"http": 200}, {"data": []}
            return {"http": 200}, {"data": [{"id": ENV["AI_PRIMARY_MODEL"]}, {"id": PRIVATE}]}
        with patch.dict(os.environ, {"AI_API_KEY_PRIMARY": raw}), patch.object(catalog, "request", side_effect=request):
            result = catalog.check("primary")
        self.assertEqual([raw, None, SECRET], [key for _, key in calls])
        self.assertEqual(3, len(calls))
        self.assertFalse(result["catalog_accessible"])
        self.assertTrue(result["padding_variant"]["accessible"])
        self.assertEqual("trimmed_catalog_only", result["padding_variant"]["variant"])
        self.assertFalse(result["generation_tested"])
        self.assertFalse(result["padding_variant"]["canonical_key_used_for_generation"])
        self.assert_private_absent(result)

    def test_anonymous_catalog_200_is_not_credential_or_generation_proof(self):
        with patch.object(catalog, "request", return_value=({"http": 200}, {"data": [{"id": ENV["AI_PRIMARY_MODEL"]}]})) as request:
            result = catalog.check("primary")
        self.assertEqual(2, request.call_count)
        self.assertEqual("not_proven_by_catalog", result["key_validation"])
        self.assertFalse(result["generation_tested"])

    def test_auth_error_classification_is_fixed_and_request_id_cannot_echo_key(self):
        for message, code, category in (("invalid api key " + SECRET, "invalid_api_key", "invalid_key"), ("credential revoked " + PRIVATE, "revoked_api_key", "expired_or_revoked"), ("model access denied " + PRIVATE, "permission_denied", "account_or_model_access"), (PRIVATE, PRIVATE, "unclassified")):
            with self.subTest(category=category):
                result = catalog.error_summary(401, json.dumps({"error": {"code": code, "message": message}}).encode(), {"x-request-id": SECRET})
                self.assertEqual(category, result["classification"])
                self.assertIsNone(result["request_id"])
                self.assert_private_absent(result)
        self.assertEqual("req-42", catalog.safe_request_id({"x-request-id": "req-42"}))
        self.assertIsNone(catalog.safe_request_id({"x-request-id": "bad\nvalue"}))

    def test_http_error_body_read_is_bounded_and_never_saved(self):
        body = Mock()
        body.read.return_value = json.dumps({"error": {"code": "invalid_api_key", "message": SECRET + PRIVATE}}).encode()
        error = urllib.error.HTTPError("https://api.river.ai/v1/models", 401, PRIVATE, {"x-request-id": "req-safe"}, body)
        opener = Mock()
        opener.open.side_effect = error
        with patch.object(catalog.urllib.request, "build_opener", return_value=opener):
            result, parsed = catalog.request("https://api.river.ai/v1/models", SECRET)
        body.read.assert_called_once_with(4096)
        self.assertIsNone(parsed)
        self.assertEqual("invalid_key", result["classification"])
        self.assert_private_absent(result)

    def test_reasoning_none_only_applies_to_river_deepseek(self):
        config = catalog.configuration("primary")
        self.assertEqual("none", probe.payload(config, "minimal_chat", True)["reasoning_effort"])
        for host, model in (("api.river.ai", "zai-org/GLM-5.3-Flash"), ("another.example", "deepseek-ai/DeepSeek-V4.1-Flash")):
            config["endpoint"]["host"] = host
            config["model"] = model
            self.assertNotIn("reasoning_effort", probe.payload(config, "minimal_chat", True))
        config = catalog.configuration("primary")
        self.assertNotIn("stream_options", probe.payload(config, "stream", False))
        self.assertEqual({"include_usage": True}, probe.payload(config, "stream", True)["stream_options"])

    def test_minimal_chat_has_small_body_and_sanitized_completion(self):
        result, opener = self.attempt_with(Response(completion()))
        request = opener.open.call_args.args[0]
        sent = json.loads(request.data)
        self.assertEqual("https://api.river.ai/v1/chat/completions", request.full_url)
        self.assertEqual("Bearer " + SECRET, request.get_header("Authorization"))
        self.assertEqual(128, sent["max_tokens"])
        self.assertFalse(sent["stream"])
        self.assertNotIn("tools", sent)
        self.assertNotIn("response_format", sent)
        self.assertIsNone(request.get_header("X-opencode-session"))
        self.assertEqual("complete", result["status"])
        self.assertFalse(result["billing_unknown"])
        self.assertEqual(22, result["usage"]["total_tokens"])
        self.assertEqual(1, opener.open.call_count)

    def test_stream_handles_fragmented_sse_and_never_exposes_hidden_reasoning(self):
        events = [{"choices": [{"index": 0, "delta": {"reasoning_content": PRIVATE}}]}, {"choices": [{"index": 0, "delta": {"content": "po"}}]}, {"choices": [{"index": 0, "delta": {"content": "ng"}, "finish_reason": "stop"}]}, {"choices": [], "usage": {"total_tokens": 9, PRIVATE: 1, "secret": SECRET}}]
        data = b"".join(b"data: " + json.dumps(event).encode() + b"\r\n\r\n" for event in events) + b"data: [DONE]\r\n\r\n"
        result, _ = self.attempt_with(Response(data, "text/event-stream", chunk=3), "stream")
        self.assertEqual("complete", result["status"])
        self.assertEqual({"total_tokens": 9}, result["usage"])
        self.assertIsNotNone(result["ttfb_ms"])
        self.assertFalse(result["validation"]["tool_executed"])

    def test_forced_safe_tool_validates_arguments_without_executing(self):
        result, opener = self.attempt_with(Response(completion(None, "tool_calls", calls=[tool_call()])), "forced_tool")
        self.assertEqual("complete", result["status"])
        self.assertFalse(result["validation"]["tool_executed"])
        sent = json.loads(opener.open.call_args.args[0].data)
        self.assertEqual({"type": "function", "function": {"name": probe.TOOL_NAME}}, sent["tool_choice"])
        self.assertEqual(1024, sent["max_tokens"])
        invalid, _ = self.attempt_with(Response(completion(None, "tool_calls", calls=[tool_call('{"ok":true,"body":"' + PRIVATE + '"}')])), "forced_tool")
        self.assertEqual("incomplete", invalid["status"])

    def test_unrecognized_finish_and_incomplete_stream_are_not_complete(self):
        result, _ = self.attempt_with(Response(completion(finish=SECRET)))
        self.assertEqual("unrecognized", result["finish_reason"])
        self.assertEqual("incomplete", result["status"])
        result, _ = self.attempt_with(Response(b'data: {"choices":[{"delta":{"content":"pong"},"finish_reason":"stop"}]}\n\n', "text/event-stream"), "stream")
        self.assertEqual("protocol_unknown", result["status"])

    def test_missing_or_zero_usage_remains_unknown(self):
        result, _ = self.attempt_with(Response(completion(usage=False)))
        self.assertEqual("complete", result["status"])
        self.assertTrue(result["billing_unknown"])
        self.assertEqual({}, probe.safe_usage({"total_tokens": False, PRIVATE: 99, "secret": SECRET}))

    def test_probe_auth_error_preserves_unknown_billing_without_free_message(self):
        body = Mock()
        body.read.return_value = json.dumps({"error": {"code": "invalid_api_key", "message": SECRET + PRIVATE}}).encode()
        error = urllib.error.HTTPError("https://api.river.ai/v1/chat/completions", 401, PRIVATE, {"x-request-id": SECRET}, body)
        opener = Mock()
        opener.open.side_effect = error
        with patch.object(probe.urllib.request, "build_opener", return_value=opener):
            result = probe.attempt("primary", "minimal_chat", 5)
        body.read.assert_called_once_with(4096)
        self.assertEqual("auth_failed", result["status"])
        self.assertTrue(result["billing_unknown"])
        self.assert_private_absent(result)

    def test_claim_is_durable_before_each_post_and_default_never_calls_backup(self):
        def worker(profile, stage, timeout, include_usage):
            ledger = json.loads((self.output / "ledger.json").read_text())
            self.assertEqual("pending", ledger["attempts"][-1]["status"])
            self.assertTrue(ledger["attempts"][-1]["billing_unknown"])
            self.assertEqual("primary", profile)
            self.assertLessEqual(timeout, 50)
            return {"stage": stage, "status": "complete", "billing_unknown": False}
        with patch.object(probe, "run_worker", side_effect=worker) as dispatch:
            report = probe.run(self.output)
        self.assertEqual(3, dispatch.call_count)
        self.assertEqual("complete", report["status"])
        self.assertEqual(3, report["new_model_requests"])
        self.assertEqual(["minimal_chat", "stream", "forced_tool"], [row["stage"] for row in report["profiles"][0]["stages"]])
        self.assert_private_absent(report)
        self.assert_private_absent(json.loads((self.output / "ledger.json").read_text()))

    def test_auth_or_unsupported_parameter_or_incomplete_stops_dependency_chain(self):
        for status in ("auth_failed", "capability_unknown", "incomplete", "protocol_unknown", "deadline_unknown"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                with patch.object(probe, "run_worker", return_value={"stage": "minimal_chat", "status": status, "billing_unknown": True}) as dispatch:
                    report = probe.run(Path(directory))
                self.assertEqual(1, dispatch.call_count)
                self.assertEqual("failed", report["status"])
                self.assertEqual(1, report["new_model_requests"])

    def test_stream_failure_does_not_start_forced_tool(self):
        with patch.object(probe, "run_worker", side_effect=[{"stage": "minimal_chat", "status": "complete", "billing_unknown": False}, {"stage": "stream", "status": "capability_unknown", "http": 400, "billing_unknown": True}]) as dispatch:
            report = probe.run(self.output)
        self.assertEqual(2, dispatch.call_count)
        self.assertEqual("failed", report["status"])

    def test_existing_unknown_ledger_is_never_replayed_or_echoed(self):
        path = self.output / "ledger.json"
        original = json.dumps({"attempts": [{"status": "pending", "billing_unknown": True}], "untrusted": SECRET + PRIVATE})
        path.write_text(original)
        with patch.object(probe, "run_worker") as dispatch:
            report = probe.run(self.output)
        dispatch.assert_not_called()
        self.assertEqual(0, report["new_model_requests"])
        self.assertEqual("existing_ledger_no_automatic_replay", report["reason"])
        self.assertEqual(original, path.read_text())
        self.assert_private_absent(report)

    def test_global_deadline_is_shared_across_all_profiles(self):
        clock = [0.0]
        def worker(profile, stage, timeout, include_usage):
            clock[0] += timeout
            return {"stage": stage, "status": "complete", "billing_unknown": False}
        with patch.dict(os.environ, {"HOSTLAB_PROBE_PROFILE": "all"}), patch.object(probe.time, "monotonic", side_effect=lambda: clock[0]), patch.object(probe, "run_worker", side_effect=worker) as dispatch:
            report = probe.run(self.output)
        self.assertEqual(4, dispatch.call_count)
        self.assertLessEqual(report["runtime_seconds"], 180)
        self.assertEqual("complete", report["profiles"][0]["status"])
        self.assertEqual("failed", report["profiles"][1]["status"])

    def test_worker_timeout_is_killed_reaped_and_unknown_without_retry(self):
        process = Mock()
        process.communicate.side_effect = [subprocess.TimeoutExpired("worker", 1), (b"", b"")]
        with patch.object(probe.subprocess, "Popen", return_value=process) as start:
            result = probe.run_worker("primary", "minimal_chat", 1, True)
        process.kill.assert_called_once()
        self.assertEqual(2, process.communicate.call_count)
        self.assertEqual(1, start.call_count)
        self.assertEqual("deadline_unknown", result["status"])
        self.assertTrue(result["billing_unknown"])
        self.assert_private_absent(start.call_args.args)
        self.assert_private_absent(result)
        self.assertNotIn(SECRET.encode(), process.communicate.call_args_list[0].args[0])

    def test_all_profiles_is_still_capped_at_three_posts_each(self):
        def worker(profile, stage, timeout, include_usage):
            return {"stage": stage, "status": "complete", "billing_unknown": True}
        with patch.dict(os.environ, {"HOSTLAB_PROBE_PROFILE": "all"}), patch.object(probe, "run_worker", side_effect=worker) as dispatch:
            report = probe.run(self.output)
        self.assertEqual(6, dispatch.call_count)
        self.assertEqual(3, sum(call.args[0] == "primary" for call in dispatch.call_args_list))
        self.assertEqual(3, sum(call.args[0] == "backup" for call in dispatch.call_args_list))
        self.assertEqual("complete", report["status"])

    def test_probe_preserves_padding_and_blocks_control_without_silent_repair(self):
        with patch.dict(os.environ, {"AI_API_KEY_PRIMARY": " " + SECRET + " "}):
            result, opener = self.attempt_with(Response(completion()))
        self.assertEqual("Bearer  " + SECRET + " ", opener.open.call_args.args[0].get_header("Authorization"))
        with patch.dict(os.environ, {"AI_API_KEY_PRIMARY": SECRET + "\u200b"}):
            self.assertTrue(catalog.credential_shape(os.environ["AI_API_KEY_PRIMARY"])["control"])
            result = probe.attempt("primary", "minimal_chat", 5)
        self.assertEqual("configuration_failed", result["status"])
        self.assertFalse(result["billing_unknown"])
        self.assert_private_absent(result)

    def test_unsupported_400_is_unknown_and_response_size_is_bounded(self):
        body = Mock()
        body.read.return_value = json.dumps({"error": {"code": "unsupported_parameter", "message": PRIVATE + SECRET}}).encode()
        error = urllib.error.HTTPError("https://api.river.ai/v1/chat/completions", 400, PRIVATE, {}, body)
        opener = Mock()
        opener.open.side_effect = error
        with patch.object(probe.urllib.request, "build_opener", return_value=opener):
            result = probe.attempt("primary", "stream", 5)
        self.assertEqual("capability_unknown", result["status"])
        self.assertEqual(1, opener.open.call_count)
        self.assertTrue(result["billing_unknown"])
        self.assert_private_absent(result)
        result, _ = self.attempt_with(Response(b"x" * (probe.MAX_RESPONSE_BYTES + 1)))
        self.assertEqual("protocol_unknown", result["status"])

    def test_bad_selection_or_cli_does_not_dispatch(self):
        with patch.dict(os.environ, {"HOSTLAB_PROBE_PROFILE": "unknown"}), patch.object(probe, "run_worker") as dispatch:
            report = probe.run(self.output)
        dispatch.assert_not_called()
        self.assertEqual("invalid_probe_selection", report["reason"])
        for module in (catalog, probe):
            with self.subTest(module=module.__name__), patch.object(module.sys, "argv", ["diagnostic.py", "--help"]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(2, module.main())


if __name__ == "__main__":
    unittest.main()
