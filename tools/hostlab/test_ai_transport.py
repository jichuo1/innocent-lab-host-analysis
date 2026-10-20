import io
import json
import os
import subprocess
import unittest
import urllib.error
from unittest.mock import patch

import ai_transport as transport


ENV = {"AI_API_KEY_PRIMARY": "transport-test-secret",
       "AI_PRIMARY_BASE_URL": "https://example.test/v1", "AI_PRIMARY_MODEL": "test-model"}


def event(value):
    return b"data: " + (value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()) + b"\n\n"


def delta(value, finish=None, **extra):
    return event(dict(choices=[{"index": 0, "delta": value, "finish_reason": finish}], **extra))


class Response(io.BytesIO):
    def __init__(self, body, content_type="text/event-stream", chunk_size=7):
        super().__init__(body)
        self.headers = {"Content-Type": content_type}
        self.chunk_size = chunk_size

    def read1(self, bound):
        return self.read(min(bound, self.chunk_size))


class TransportTest(unittest.TestCase):
    def request(self, body, content_type="text/event-stream", **kwargs):
        response = Response(body, content_type)
        with patch.dict(os.environ, ENV), patch.object(transport.urllib.request, "build_opener") as build:
            build.return_value.open.return_value = response
            result = transport._call_api("primary", [{"role": "user", "content": "代码"}], [],
                                        session_id="hostlab-test", **kwargs)
            request = build.return_value.open.call_args.args[0]
        return result, request

    def test_fragmented_tool_unicode_usage_and_hidden_reasoning(self):
        raw = b": keepalive\n\n" + delta({"role": "assistant", "reasoning_content": "private reasoning"})
        raw += delta({"tool_calls": [{"index": 0, "id": "call-1", "type": "function",
                                     "function": {"name": "finish_report", "arguments": '{"text":"'}}]})
        raw += delta({"tool_calls": [{"index": 0, "function": {"arguments": "中文"}}]})
        raw += delta({"tool_calls": [{"index": 0, "function": {"arguments": '"}'}}]}, "tool_calls",
                     model="actual-model")
        raw += event({"choices": [], "usage": {"prompt_tokens": 20, "completion_tokens": 9,
                                               "prompt_tokens_details": {"cached_tokens": 10}}})
        raw += event(b"[DONE]")
        (message, usage, model), request = self.request(raw)
        self.assertEqual(json.loads(message["tool_calls"][0]["function"]["arguments"]), {"text": "中文"})
        self.assertEqual(model, "actual-model")
        self.assertEqual(usage["prompt_tokens_details"]["cached_tokens"], 10)
        self.assertTrue(usage["_transport"]["usage_received"])
        self.assertFalse(usage["_usage_unknown"])
        self.assertNotIn("private reasoning", json.dumps(message))
        self.assertIsNone(request.get_header("X-opencode-session"))
        payload = json.loads(request.data)
        self.assertTrue(payload["stream"])
        self.assertEqual(payload["max_tokens"], 8192)
        self.assertEqual(request.get_header("User-agent"), "HostLab-AIReview/2")

    def test_session_header_is_preserved_only_for_exact_opencode_host(self):
        for base, expected in (
                ("https://opencode.ai/zen/go/v1", "hostlab-test"),
                ("https://OPENCODE.AI/zen/go/v1", "hostlab-test"),
                ("https://api.river.ai/v1", None),
                ("https://api.experientiallabs.ai/v1", None),
                ("https://api.opencode.ai/v1", None),
                ("https://opencode.ai.example.test/v1", None)):
            with self.subTest(base=base), patch.dict(os.environ, dict(ENV, AI_PRIMARY_BASE_URL=base)), patch.object(transport.urllib.request, "build_opener") as build:
                build.return_value.open.return_value = Response(delta({"content": "ok"}, "stop") + event(b"[DONE]"))
                transport._call_api("primary", [{"role": "user", "content": "synthetic"}], [], session_id="hostlab-test")
                request = build.return_value.open.call_args.args[0]
                self.assertEqual(request.get_header("X-opencode-session"), expected)
                self.assertEqual(build.return_value.open.call_count, 1)

    def test_missing_usage_is_unknown_not_zero(self):
        (message, usage, _), _ = self.request(delta({"content": "complete"}, "stop") + event(b"[DONE]"))
        self.assertEqual(message["content"], "complete")
        self.assertTrue(usage["_usage_unknown"])
        self.assertNotIn("total_tokens", usage)

    def test_zero_placeholder_usage_remains_unknown(self):
        raw = delta({"content": "ok"}, "stop", usage={"total_tokens": 0, "prompt_tokens_details": {"cached_tokens": 0}}) + event(b"[DONE]")
        (_, usage, _), _ = self.request(raw)
        self.assertTrue(usage["_usage_unknown"])
        self.assertFalse(usage["_transport"]["usage_received"])

    def test_unknown_finish_reason_cannot_enter_error_receipts(self):
        with self.assertRaises(transport.ApiError) as caught:
            self.request(delta({"content": "ok"}, "transport-test-secret") + event(b"[DONE]"))
        self.assertNotIn("secret", str(caught.exception))

    def test_truncated_reply_keeps_reported_usage_without_accepting_partial_content(self):
        raw = delta({"content": "partial"}, "length", usage={"prompt_tokens": 12, "completion_tokens": 8}) + event(b"[DONE]")
        with self.assertRaises(transport.ApiError) as caught:
            self.request(raw)
        self.assertFalse(caught.exception.billing_unknown)
        self.assertEqual(caught.exception.usage["completion_tokens"], 8)
        self.assertEqual(caught.exception.metrics["finish_reason"], "length")

    def test_content_filter_is_not_automatically_retried(self):
        with self.assertRaises(transport.ApiError) as caught:
            self.request(delta({}, "content_filter") + event(b"[DONE]"))
        self.assertFalse(caught.exception.retryable)

    def test_extended_output_scales_raw_stream_limit_but_remains_bounded(self):
        raw = b": " + b" "*90 + b"\n\n" + delta({"content": "ok"}, "stop") + event(b"[DONE]")
        with patch.object(transport, "MAX_STREAM_BYTES", 180):
            with self.assertRaises(transport.ApiError):
                self.request(raw)
            (message, _, _), _ = self.request(raw, max_output=16384)
        self.assertEqual(message["content"], "ok")

    def test_sse_envelope_overhead_does_not_count_as_assembled_content(self):
        raw = delta({"content": "中"}, "stop", metadata="x"*1200) + event(b"[DONE]")
        with patch.object(transport, "MAX_RESPONSE_BYTES", 100), patch.object(transport, "MAX_STREAM_BYTES", 4096):
            (message, usage, _), _ = self.request(raw)
        self.assertEqual(message["content"], "中")
        self.assertGreater(usage["_transport"]["response_bytes"], 100)
        self.assertEqual(usage["_transport"]["assembled_bytes"], 3)

    def test_fine_grained_tool_stream_can_exceed_old_two_mib_wire_cap(self):
        raw = delta({"tool_calls": [{"index": 0, "id": "call-1", "function": {"name": "finish_report", "arguments": '{"text":"'}}]})
        raw += delta({"tool_calls": [{"index": 0, "function": {"arguments": "中"}}]}, metadata="x"*200)*7405
        raw += delta({"tool_calls": [{"index": 0, "function": {"arguments": '"}'}}]}, "tool_calls")
        raw += event({"choices": [], "usage": {"prompt_tokens": 20, "completion_tokens": 4063}})+event(b"[DONE]")
        self.assertGreater(len(raw), 2*1024*1024)
        response = Response(raw, chunk_size=8192)
        with patch.dict(os.environ, ENV), patch.object(transport.urllib.request, "build_opener") as build:
            build.return_value.open.return_value = response
            message, usage, _ = transport._call_api("primary", [], [])
        self.assertEqual(json.loads(message["tool_calls"][0]["function"]["arguments"]), {"text": "中"*7405})
        self.assertEqual(usage["completion_tokens"], 4063)
        self.assertLess(usage["_transport"]["assembled_bytes"], 32768)
        self.assertEqual(build.return_value.open.call_count, 1)

    def test_assembled_utf8_budget_counts_content_and_all_tool_fragments(self):
        cases = [delta({"content": "中"})*4,
            delta({"tool_calls": [{"index": 0, "function": {"arguments": "中中"}}]})
            + delta({"tool_calls": [{"index": 1, "function": {"arguments": "中中"}}]})]
        for raw in cases:
            with self.subTest(raw=raw), patch.object(transport, "MAX_RESPONSE_BYTES", 10), self.assertRaisesRegex(transport.ApiError, "assembled"):
                self.request(raw+event(b"[DONE]"))

    def test_stream_event_count_remains_bounded_even_for_empty_deltas(self):
        with patch.object(transport, "MAX_STREAM_EVENTS", 2), self.assertRaisesRegex(transport.ApiError, "event count"):
            self.request(delta({})*3+event(b"[DONE]"))

    def test_json_retains_its_original_scaled_wire_budget(self):
        raw = json.dumps({"choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}], "metadata": "x"*50}).encode()
        with patch.object(transport, "MAX_RESPONSE_BYTES", 100), self.assertRaisesRegex(transport.ApiError, "API response exceeds bound"):
            self.request(raw, "application/json")
        with patch.object(transport, "MAX_RESPONSE_BYTES", 100):
            (message, _, _), _ = self.request(raw, "application/json", max_output=16384)
        self.assertEqual(message["content"], "ok")

    def test_json_assembled_content_keeps_worker_sized_budget(self):
        raw = json.dumps({"choices": [{"message": {"content": "x"*201}, "finish_reason": "stop"}]}).encode()
        with patch.object(transport, "MAX_RESPONSE_BYTES", 200), self.assertRaisesRegex(transport.ApiError, "assembled"):
            self.request(raw, "application/json", max_output=16384)

    def test_worker_wall_deadline_terminates_and_reaps_once(self):
        with patch.object(transport.subprocess, "Popen") as popen:
            worker = popen.return_value
            worker.communicate.side_effect = [subprocess.TimeoutExpired("worker", 1), (b"", None)]
            with self.assertRaises(transport.ApiError) as caught:
                transport.call_api("primary", [], [], total_timeout=1, idle_timeout=1)
        worker.kill.assert_called_once()
        self.assertEqual(worker.communicate.call_count, 2)
        self.assertTrue(caught.exception.billing_unknown)
        self.assertTrue(caught.exception.metrics["worker_terminated"])
        self.assertEqual(popen.call_count, 1)

    def test_worker_complete_response_no_replay(self):
        value = {"result": [{"role": "assistant", "content": "ok"}, {"_transport": {}}, "model"]}
        with patch.object(transport.subprocess, "Popen") as popen:
            popen.return_value.returncode = 0
            popen.return_value.communicate.return_value = (json.dumps(value).encode(), None)
            message, usage, model = transport.call_api("primary", [], [])
        self.assertEqual(message["content"], "ok")
        self.assertEqual(model, "model")
        self.assertIn("wall_ms", usage["_transport"])
        popen.return_value.kill.assert_not_called()

    def test_larger_sse_wire_budget_does_not_expand_worker_output(self):
        with patch.object(transport, "MAX_RESPONSE_BYTES", 100), patch.object(transport.subprocess, "Popen") as popen:
            popen.return_value.returncode = 0
            popen.return_value.communicate.return_value = (b"x"*101, None)
            with self.assertRaises(transport.ApiError) as caught:
                transport.call_api("primary", [], [], max_output=16384)
        self.assertEqual(caught.exception.kind, "interrupted")
        self.assertTrue(caught.exception.billing_unknown)
        self.assertEqual(popen.call_count, 1)

    def test_worker_start_failure_is_known_without_post(self):
        with patch.object(transport.subprocess, "Popen", side_effect=OSError("private path")):
            with self.assertRaises(transport.ApiError) as caught:
                transport.call_api("primary", [], [])
        self.assertFalse(caught.exception.billing_unknown)
        self.assertEqual(caught.exception.kind, "configuration")

    def test_retry_after_http_date_is_bounded(self):
        with patch.object(transport.time, "time", return_value=0):
            self.assertEqual(transport._retry_after({"Retry-After": "Thu, 01 Jan 1970 00:00:10 GMT"}), 10)
        self.assertIsNone(transport._retry_after({"Retry-After": "untrusted text"}))

    def test_real_worker_config_failure_is_known_before_post(self):
        with patch.dict(os.environ, dict(ENV, AI_PRIMARY_BASE_URL="http://invalid")):
            with self.assertRaises(transport.ApiError) as caught:
                transport.call_api("primary", [], [], total_timeout=5, idle_timeout=1)
        self.assertFalse(caught.exception.billing_unknown)
        self.assertEqual(caught.exception.kind, "configuration")

    def test_json_gateway_fallback_is_validated(self):
        raw = json.dumps({"choices": [{"message": {"content": "ok", "reasoning": "hidden"},
                                       "finish_reason": "stop"}], "usage": {"total_tokens": 3}}).encode()
        (message, usage, _), _ = self.request(raw, "application/json")
        self.assertEqual(message, {"role": "assistant", "content": "ok"})
        self.assertEqual(usage["total_tokens"], 3)
        self.assertFalse(usage["_transport"]["streaming"])

    def test_stream_requires_finish_and_done(self):
        for raw, kind in ((delta({"content": "partial"}), "interrupted"),
                          (delta({"content": "partial"}, "length") + event(b"[DONE]"), "incomplete"),
                          (delta({"content": "partial"}) + event(b"[DONE]"), "incomplete")):
            with self.subTest(kind=kind), self.assertRaises(transport.ApiError) as caught:
                self.request(raw)
            self.assertEqual(caught.exception.kind, kind)
            self.assertTrue(caught.exception.billing_unknown)

    def test_stream_rejects_malformed_duplicate_or_oversized_tools(self):
        for value in ({"tool_calls": [{"index": 16}]}, {"tool_calls": "invalid"},
                      {"content": 42}, {"tool_calls": [{"index": 0, "id": "x", "function": {"name": "f", "arguments": 42}}]}):
            with self.subTest(value=value), self.assertRaises(transport.ApiError):
                self.request(delta(value, "tool_calls") + event(b"[DONE]"))
        with patch.object(transport, "MAX_EVENT_BYTES", 20), self.assertRaises(transport.ApiError):
            self.request(b"data: " + b"x" * 30 + b"\n\n")

    def test_response_bound(self):
        with patch.object(transport, "MAX_STREAM_BYTES", 20), self.assertRaises(transport.ApiError) as caught:
            self.request(delta({"content": "too long"}, "stop") + event(b"[DONE]"))
        self.assertEqual(str(caught.exception), "API response exceeds bound")

    def test_absolute_deadline_even_with_heartbeats(self):
        ticks = iter([0, 0, 0, 0, 2, 2, 2, 2, 2])
        with patch.object(transport.time, "monotonic", side_effect=lambda: next(ticks, 2)):
            with self.assertRaises(transport.ApiError) as caught:
                self.request(b": keepalive\n\n" * 10, total_timeout=1, idle_timeout=1)
        self.assertEqual(caught.exception.kind, "timeout")

    def test_bad_config_never_posts(self):
        for base in ("http://example.test", "https://user:secret@example.test", "https://example.test/?key=x", "https:///missing"):
            with patch.dict(os.environ, dict(ENV, AI_PRIMARY_BASE_URL=base)), patch.object(transport.urllib.request, "build_opener") as build:
                with self.assertRaises(transport.ApiError) as caught:
                    transport._call_api("primary", [], [])
                self.assertFalse(caught.exception.billing_unknown)
                build.assert_not_called()

    def test_full_chat_endpoint_and_output_parameter_are_explicit(self):
        for base, extra, field in (("https://api.river.ai/v1/chat/completions/", {}, "max_tokens"),
                ("https://api.openai.com/v1/chat/completions", {}, "max_completion_tokens"),
                ("https://proxy.example/v1", {"AI_PRIMARY_OUTPUT_TOKEN_PARAMETER": "max_completion_tokens"}, "max_completion_tokens")):
            with self.subTest(base=base), patch.dict(os.environ, dict(ENV, AI_PRIMARY_BASE_URL=base, **extra)), patch.object(transport.urllib.request, "build_opener") as build:
                build.return_value.open.return_value = Response(delta({"content": "ok"}, "stop")+event(b"[DONE]"))
                transport._call_api("primary", [], [])
                request = build.return_value.open.call_args.args[0]
                self.assertEqual(request.full_url.count("/chat/completions"), 1)
                payload = json.loads(request.data)
                self.assertEqual(payload[field], 8192)
                self.assertEqual(len({"max_tokens", "max_completion_tokens"}.intersection(payload)), 1)

    def test_unsupported_endpoint_or_token_parameter_never_posts(self):
        for values in ({"AI_PRIMARY_BASE_URL": "https://example.test/v1/messages"},
                {"AI_PRIMARY_BASE_URL": "https://example.test/v1/responses"},
                {"AI_PRIMARY_OUTPUT_TOKEN_PARAMETER": "unbounded"}):
            with self.subTest(values=values), patch.dict(os.environ, dict(ENV, **values)), patch.object(transport.urllib.request, "build_opener") as build:
                with self.assertRaises(transport.ApiError) as caught:
                    transport._call_api("primary", [], [])
                self.assertFalse(caught.exception.billing_unknown)
                build.assert_not_called()

    def test_complete_usage_survives_postprocessing_protocol_rejection(self):
        calls = [{"id": "same", "type": "function", "function": {"name": "finish_report", "arguments": "{}"}}]*2
        raw = json.dumps({"choices": [{"message": {"tool_calls": calls}, "finish_reason": "tool_calls"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14}}).encode()
        with self.assertRaises(transport.ApiError) as caught:
            self.request(raw, "application/json")
        self.assertEqual(caught.exception.usage["total_tokens"], 14)
        self.assertFalse(caught.exception.billing_unknown)
        self.assertEqual(caught.exception.metrics["finish_reason"], "tool_calls")

    def test_ninth_tool_is_rejected_with_usage_instead_of_silently_dropped(self):
        calls = [{"id": "call-"+str(i), "function": {"name": "finish_report", "arguments": "{}"}} for i in range(9)]
        raw = json.dumps({"choices": [{"message": {"tool_calls": calls}, "finish_reason": "tool_calls"}], "usage": {"total_tokens": 14}}).encode()
        with self.assertRaisesRegex(transport.ApiError, "tool calls exceed") as caught:
            self.request(raw, "application/json")
        self.assertFalse(caught.exception.billing_unknown)

    def test_http_error_retry_after_and_no_secret_body(self):
        error = urllib.error.HTTPError("https://example.test", 429, "transport-test-secret", {"Retry-After": "999"}, io.BytesIO(b"secret body"))
        with patch.dict(os.environ, ENV), patch.object(transport.urllib.request, "build_opener") as build:
            build.return_value.open.side_effect = error
            with self.assertRaises(transport.ApiError) as caught:
                transport._call_api("primary", [], [])
        self.assertEqual(str(caught.exception), "API HTTP 429")
        self.assertTrue(caught.exception.retryable)
        self.assertTrue(caught.exception.billing_unknown)
        self.assertEqual(caught.exception.retry_after, 999)
        self.assertNotIn("secret", json.dumps(caught.exception.__dict__))
        self.assertEqual(build.return_value.open.call_count, 1)

    def test_timeout_never_retries_or_leaks_transport_error(self):
        with patch.dict(os.environ, ENV), patch.object(transport.urllib.request, "build_opener") as build:
            build.return_value.open.side_effect = TimeoutError("transport-test-secret")
            with self.assertRaises(transport.ApiError) as caught:
                transport._call_api("primary", [], [])
        self.assertEqual(caught.exception.kind, "timeout")
        self.assertEqual(str(caught.exception), "API timeout")
        self.assertEqual(build.return_value.open.call_count, 1)

    def test_redirect_denied(self):
        self.assertIsNone(transport.NoRedirect().redirect_request(None, None, None, None, None, None))

    def test_unavailable_tool_is_a_complete_response_for_safe_feedback(self):
        raw = delta({"tool_calls": [{"index": 0, "id": "call-1", "type": "function",
            "function": {"name": "functions.not_offered", "arguments": '{"private":"body"}'}}]}, "tool_calls")
        raw += event({"choices": [], "usage": {"total_tokens": 14}})+event(b"[DONE]")
        (message, usage, _), _ = self.request(raw)
        self.assertEqual(message["tool_calls"][0]["function"]["name"], "functions.not_offered")
        self.assertEqual(usage["_transport"]["unavailable_tool_calls"], 1)
        self.assertFalse(usage["_usage_unknown"])

    def test_completed_secret_text_redacted(self):
        (message, _, _), _ = self.request(delta({"content": "transport-test-secret"}, "stop") + event(b"[DONE]"))
        self.assertEqual(message["content"], "[REDACTED]")


if __name__ == "__main__":
    unittest.main()
