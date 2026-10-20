"""Recovery changes budgets once; public evidence and paid history remain immutable."""
import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

import ai_checkpoint as checkpoint
import ai_recovery as recovery


def policy():
    return {"max_requests": 16, "transport_retries": 2, "deadline_seconds": 1800,
            "initial_profile": "primary", "allow_fallback": True, "max_output": 8192,
            "total_timeout": 240, "idle_timeout": 45, "stream": True}


class FakeEvidence:
    def __init__(self, document):
        self.document = copy.deepcopy(document)
        prefetched = []
        for row in document["tools"]:
            if row["tool"] != "page_evidence":
                break
            prefetched.append(row)
        self.summary = {"page_path_matrix": {row["args"]["page"]: {} for row in prefetched}}
        self.journal = copy.deepcopy(prefetched)
        self.ids = {"E000", *[row["id"] for row in self.journal]}
        self.calls = 0
        self.limit = 8

    def public_journal(self):
        return copy.deepcopy(self.journal)

    def run_tool(self, name, args):
        if self.calls >= self.limit:
            raise RuntimeError("tool budget")
        self.calls += 1
        row = copy.deepcopy(self.document["tools"][len(self.journal)])
        if row["tool"] != name or row["args"] != args:
            raise RuntimeError("tool mismatch")
        self.journal.append(row); self.ids.add(row["id"])
        return row["result"]

    def server_read(self, name, args):
        calls = self.calls
        result = self.run_tool(name, args)
        self.calls = calls
        return result


class AiRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.artifact = self.root/"artifact"; self.artifact.mkdir()
        self.output = self.root/"output"; self.output.mkdir()
        files = {}
        for name in ("priority-target.json", "priority-baseline.json", "static-manifest.json"):
            raw = json.dumps({"frozen": name}).encode()
            (self.output/name).write_bytes(raw)
            files[name] = hashlib.sha256(raw).hexdigest()
        self.binding = {"schema": 1, "static_files": files, "static_manifest_sha256": files["static-manifest.json"],
            "sample": {"sha256": "a"*64}, "baseline": {"sha256": "b"*64}, "matrix_sha256": "c"*64,
            "source_snapshot": {"binding": {"path": "source-snapshots/immutable/context.json"}},
            "prompt_version": "fixed-v6", "code": {name: "a"*64 for name in recovery.BOUND_CODE},
            "provider_config_sha256": {"primary": "b"*64, "backup": "c"*64},
            "draft_units": [["p0"], ["p1"], ["p2"]], "no_apk_access": True, "policy": policy()}
        self.new_binding = copy.deepcopy(self.binding)
        self.new_binding["code"].update({name: "d"*64 for name in recovery.MUTABLE_CODE})
        self.new_binding["policy"].update(max_requests=24, transport_retries=4, max_output=16384, recovery_policy="extended-v1")
        attempts = [{"id": format(index+1, "032x"), "request_sha256": format(index+1, "064x"),
            "profile": "backup", "stage": "draft", "unit": "d2" if index == 8 else "d0", "status": "failed",
            "retryable": True, "billing_unknown": True, "transport_retry": index in {1, 5}} for index in range(9)]
        self.original = {"schema": 1, "binding": self.binding, "binding_sha256": checkpoint.digest(self.binding),
            "attempts": attempts, "units": {}, "responses": {}, "providers": {"backup": {"failures": 1, "open_until": 0}},
            "transport_retries": 2, "elapsed_seconds": 485.734, "created_at": 100}
        for index in range(2):
            result = {"pages": [{"page": "p"+str(index)}], "findings": [], "overview": "accepted"}
            self.original["units"]["d"+str(index)] = {"result": result, "result_sha256": checkpoint.digest(result)}
        response = {"clean": {"role": "assistant", "content": None}, "usage": {"_usage_unknown": True}, "model": "model"}
        self.original["responses"]["a"*64] = {**response, "response_sha256": checkpoint.digest(response)}
        self.document = {"E000": {}, "tools": []}
        for index, (tool, args) in enumerate([("page_evidence", {"page": page}) for page in ("p0", "p1", "p2")]
                + [("protocol_evidence", {"protocol": "p", "side": "target"}), ("module_source", {"path": "src/Frozen.kt"})], 1):
            eid = "E"+str(index).zfill(3)
            self.document["tools"].append({"id": eid, "tool": tool, "args": args, "result": {"evidence_id": eid}})
        self.write_inputs()
        self.summary = {"ai_recovery_policy": "extended-v1", "checkpoint_from_run": 987,
                        "ai_recovery_inputs": recovery.restore_inputs(self.output, list(self.artifact.iterdir()), 987)}

    def write_inputs(self):
        for name, value in (("ai-checkpoint.json", self.original), ("ai-evidence.json", self.document)):
            (self.artifact/name).write_text(json.dumps(value), encoding="utf-8")

    def prepare(self, binding=None, evidence=None):
        return recovery.prepare_recovery(self.output, self.summary, binding or self.new_binding,
                                         evidence or FakeEvidence(self.document))

    def test_first_review_resume_requires_complete_drafts_and_retains_budget(self):
        result = {"pages":[{"page":"p2"}],"findings":[],"overview":"accepted"}
        self.original["units"]["d2"]={"result":result,"result_sha256":checkpoint.digest(result)}
        for row,profile in zip(self.original["attempts"][-2:],["primary","backup"]):
            row.update(stage="review",unit="r0",kind="incomplete",profile=profile,metrics={"finish_reason":"length"})
        self.write_inputs()
        old=self.output;self.output=self.root/"first-review";self.output.mkdir()
        for name in self.binding["static_files"]:(self.output/name).write_bytes((old/name).read_bytes())
        self.summary["ai_recovery_inputs"]=recovery.restore_inputs(self.output,list(self.artifact.iterdir()),987)
        self.prepare()
        value=self.opened()
        self.assertEqual(value.value["attempts"],self.original["attempts"])
        self.assertEqual(value.value["recovery"]["adopted_units"],["d0","d1","d2"])
        import ai_pipeline
        runner=ai_pipeline.Coordinator(value,None,profile="primary",deadline=1e12)
        self.assertEqual(runner.profile,"primary")
        value.claim("review","r0","e"*64,"primary","session")
        self.assertEqual(value.value["transport_retries"],3)

    def test_first_review_resume_rejects_missing_draft(self):
        self.original["attempts"][-1].update(stage="review",unit="r0")
        self.write_inputs()
        old=self.output;self.output=self.root/"missing-draft";self.output.mkdir()
        for name in self.binding["static_files"]:(self.output/name).write_bytes((old/name).read_bytes())
        self.summary["ai_recovery_inputs"]=recovery.restore_inputs(self.output,list(self.artifact.iterdir()),987)
        with self.assertRaisesRegex(checkpoint.CheckpointError,"every draft"):
            self.prepare()

    def opened(self):
        value = checkpoint.Checkpoint(self.output, self.new_binding)
        self.addCleanup(value.close)
        return value

    def completion_fixture(self):
        """A complete v1 parent: 21 paid attempts, five drafts, r0, and review boundary 14."""
        parent = self.root/"completion-parent"; parent.mkdir()
        origin = self.root/"completion-origin"; origin.mkdir()
        target = self.root/"completion-output"; target.mkdir()
        old = copy.deepcopy(self.original)
        pages = ["comment", "dynamic", "home", "search", "detail", "pgc", "player", "danmaku", "story", "mine"]
        old["binding"]["draft_units"] = [pages[index:index+2] for index in range(0, len(pages), 2)]
        old["binding_sha256"] = checkpoint.digest(old["binding"])
        for index in range(2):
            result = {"pages": [{"page": page} for page in old["binding"]["draft_units"][index]],
                      "findings": [], "overview": "accepted"}
            old["units"]["d"+str(index)] = {"result": result, "result_sha256": checkpoint.digest(result)}
        document = {"E000": {}, "tools": []}
        tools = [("page_evidence", {"page": page}) for page in pages]
        tools += [("protocol_evidence", {"protocol": "p"+str(index)}) for index in range(4)]
        tools += [("page_evidence", {"page": page}) for page in ("comment", "dynamic")]
        tools += [("protocol_evidence", {"protocol": "review"+str(index)}) for index in range(2)]
        for index, (tool, args) in enumerate(tools, 1):
            eid = "E"+str(index).zfill(3)
            document["tools"].append({"id": eid, "tool": tool, "args": args, "result": {"evidence_id": eid}})
        ancestor_document = {**document, "tools": document["tools"][:12]}
        (origin/"ai-checkpoint.json").write_text(json.dumps(old), encoding="utf-8")
        (origin/"ai-evidence.json").write_text(json.dumps(ancestor_document), encoding="utf-8")
        for name in self.binding["static_files"]:
            (parent/name).write_bytes((self.output/name).read_bytes())
            (target/name).write_bytes((self.output/name).read_bytes())
        v1 = copy.deepcopy(old["binding"])
        v1["code"].update({name: "d"*64 for name in recovery.MUTABLE_CODE})
        v1["policy"].update(max_requests=24, transport_retries=4, max_output=16384, recovery_policy="extended-v1")
        inputs = recovery.restore_inputs(parent, list(origin.iterdir()), 987)
        summary = {"ai_recovery_policy": "extended-v1", "checkpoint_from_run": 987, "ai_recovery_inputs": inputs}
        recovery.prepare_recovery(parent, summary, v1, FakeEvidence(ancestor_document))
        value = checkpoint.Checkpoint(parent, v1)
        try:
            for index in range(10, 21):
                request = format(index, "064x")
                token = value.claim("draft" if index < 19 else "review", "d2" if index < 19 else "r0",
                                    request, "backup", "paid-parent")
                value.received(token, request, {"role": "assistant", "content": None},
                               {"_usage_unknown": True} if index == 10 else {"total_tokens": index}, "model")
            for index in range(2, 5):
                value.save_unit("d"+str(index), {"pages": [{"page": page} for page in v1["draft_units"][index]],
                    "findings": [], "overview": "accepted"})
            value.save_unit("r0", {"pages": [{"page": page} for page in pages[:2]], "findings": [], "remaining_gaps": []})
            token = value.claim("review", "r1", "f"*64, "backup", "paid-parent")
            value.failed(token, SimpleNamespace(reason="API total deadline exceeded", kind="timeout", retryable=True,
                billing_unknown=True, http_status=None, retry_after=None, metrics={"total_ms": 6672.12}))
            value.record_elapsed(1800.013845373)
        finally:
            value.close()
        (parent/"ai-evidence.json").write_text(json.dumps(document), encoding="utf-8")
        original = json.loads((parent/"ai-checkpoint.json").read_text())
        v2 = copy.deepcopy(v1)
        v2["code"].update({name: "e"*64 for name in recovery.MUTABLE_CODE})
        v2["policy"].update(max_requests=32, deadline_seconds=3600, recovery_policy="completion-v2")
        inputs = recovery.restore_inputs(target, list(parent.iterdir()), 988, policy="completion-v2")
        summary = {"ai_recovery_policy": "completion-v2", "checkpoint_from_run": 988, "ai_recovery_inputs": inputs}
        return SimpleNamespace(parent=parent, target=target, original=original, binding=v2,
                               document=document, summary=summary)

    def prepare_completion(self, fixture, *, root=None, summary=None, document=None):
        return recovery.prepare_recovery(root or fixture.target, summary or fixture.summary, fixture.binding,
                                         FakeEvidence(document or fixture.document))

    def final_fixture(self):
        """The v2 parent has 23 attempts, all drafts, r0/r1, and a timed-out r2."""
        previous = self.completion_fixture(); self.prepare_completion(previous)
        value = checkpoint.Checkpoint(previous.target, previous.binding)
        try:
            token = value.claim("review", "r1", "b"*64, "backup", "paid-v2-parent")
            value.received(token, "b"*64, {"role": "assistant", "content": None},
                {"prompt_tokens": 3240, "completion_tokens": 12629,
                 "completion_tokens_details": {"reasoning_tokens": 9316}}, "model")
            value.save_unit("r1", {"pages": [{"page": page} for page in ("home", "search")],
                "findings": [], "remaining_gaps": []})
            token = value.claim("review", "r2", "c"*64, "backup", "paid-v2-parent")
            value.failed(token, SimpleNamespace(reason="API total deadline exceeded", kind="timeout", retryable=True,
                billing_unknown=True, http_status=None, retry_after=None, metrics={"total_ms": 240049.431}))
            value.record_elapsed(2279.517702325)
        finally:
            value.close()
        (previous.target/"ai-evidence.json").write_text(json.dumps(previous.document), encoding="utf-8")
        original = json.loads((previous.target/"ai-checkpoint.json").read_text())
        target = self.root/"final-output"; target.mkdir()
        for name in self.binding["static_files"]:
            (target/name).write_bytes((self.output/name).read_bytes())
        v3 = copy.deepcopy(previous.binding)
        v3["code"].update({name: "f"*64 for name in recovery.MUTABLE_CODE})
        v3["policy"].update(max_requests=40, transport_retries=6, deadline_seconds=4800, total_timeout=600,
                            adaptive_timeout=True, recovery_policy="completion-v3")
        inputs = recovery.restore_inputs(target, list(previous.target.iterdir()), 989, policy="completion-v3")
        summary = {"ai_recovery_policy": "completion-v3", "checkpoint_from_run": 989, "ai_recovery_inputs": inputs}
        return SimpleNamespace(parent=previous.target, target=target, original=original, binding=v3,
                               document=previous.document, summary=summary)

    def test_migrate_preserves_nine_attempts_unknown_usage_two_units_and_elapsed(self):
        origin = (self.output/"ai-resume-checkpoint.json").read_bytes()
        evidence = FakeEvidence(self.document)
        result = self.prepare(evidence=evidence)
        value = self.opened()
        self.assertEqual(value.value["attempts"], self.original["attempts"])
        self.assertEqual(value.value["responses"], self.original["responses"])
        self.assertEqual(value.value["units"], self.original["units"])
        self.assertEqual(value.value["elapsed_seconds"], 485.734)
        self.assertEqual(value.value["transport_retries"], 2)
        self.assertEqual(result["imported_units"], ["d0", "d1"])
        self.assertEqual(result["adopted_attempt_count"], 9)
        self.assertEqual(evidence.journal, self.document["tools"])
        self.assertEqual(evidence.calls, 2)
        self.assertEqual(origin, (self.output/"ai-resume-checkpoint.json").read_bytes())

    def test_explicit_wire_limit_correction_preserves_nonretryable_unknown_receipt(self):
        self.original["attempts"][-1].update(kind="protocol", reason="API response exceeds bound",
            retryable=False, http_status=None, metrics={"response_bytes": 2097273, "events": 7513})
        self.write_inputs()
        fresh = self.root/"wire-output"; fresh.mkdir()
        for name in self.binding["static_files"]:
            (fresh/name).write_bytes((self.output/name).read_bytes())
        self.output = fresh
        self.summary["ai_recovery_inputs"] = recovery.restore_inputs(self.output, list(self.artifact.iterdir()), 987)
        self.prepare()
        value = self.opened()
        self.assertEqual(value.value["attempts"], self.original["attempts"])
        self.assertFalse(value.value["attempts"][-1]["retryable"])
        self.assertTrue(value.value["attempts"][-1]["billing_unknown"])
        self.assertEqual(value.value["elapsed_seconds"], self.original["elapsed_seconds"])
        value.claim("draft", "d2", "b"*64, "backup", "session")
        self.assertEqual(value.value["transport_retries"], 3)

    def test_wire_recovery_rejects_unrelated_protocol_or_unchanged_transport(self):
        self.original["attempts"][-1].update(kind="protocol", reason="API response exceeds bound",
            retryable=False, http_status=None, metrics={"response_bytes": 2097273, "events": 7513})
        self.assertTrue(recovery._corrected_wire_stop(self.original, self.new_binding))
        for update in ({"reason": "API response malformed"}, {"kind": "http"}, {"http_status": 400},
                {"metrics": {"response_bytes": 2097152, "events": 7513}},
                {"metrics": {"response_bytes": 2105345, "events": 7513}},
                {"metrics": {"response_bytes": 2097273, "events": 0}},
                {"metrics": {"response_bytes": True, "events": 7513}}):
            changed = copy.deepcopy(self.original); changed["attempts"][-1].update(update)
            with self.subTest(update=update):
                self.assertFalse(recovery._corrected_wire_stop(changed, self.new_binding))
        unchanged = copy.deepcopy(self.new_binding)
        unchanged["code"]["ai_transport.py"] = self.binding["code"]["ai_transport.py"]
        self.assertFalse(recovery._corrected_wire_stop(self.original, unchanged))

    def test_compensation_consumed_atomically_once_for_original_d2_and_not_recharged(self):
        self.prepare()
        value = self.opened()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "reserved"):
            value.claim("draft", "d3", "b"*64, "backup", "session")
        self.assertEqual(value.value["transport_retries"], 2)
        token = value.claim("draft", "d2", "b"*64, "backup", "session")
        self.assertEqual(value.value["transport_retries"], 3)
        self.assertTrue(value.value["attempts"][-1]["transport_retry"])
        self.assertNotIn("next_retry_unit", value.value["recovery"])
        value.received(token, "b"*64, {"role": "assistant", "content": None}, {}, "m")
        result = {"pages": [{"page": "p2"}], "findings": []}
        value.save_unit("d2", result)
        value.close()
        metadata = self.prepare()
        self.assertEqual(metadata["imported_units"], ["d0", "d1"])
        self.assertEqual(metadata["adopted_attempt_count"], 9)
        resumed = self.opened()
        self.assertEqual(resumed.value["transport_retries"], 3)
        self.assertIn("d2", resumed.value["units"])
        resumed.claim("draft", "d3", "c"*64, "backup", "session")
        self.assertEqual(resumed.value["transport_retries"], 3)

    def test_unknown_source_prompt_provider_acceptance_plan_enum_and_path_changes_reject(self):
        for field, value in (("source_snapshot", {}), ("prompt_version", "changed"),
                             ("provider_config_sha256", {}), ("draft_units", [["p1"]]), ("sample", {}),
                             ("matrix_sha256", "e"*64), ("new_unapproved_field", True)):
            changed = copy.deepcopy(self.new_binding); changed[field] = value
            with self.subTest(field=field), self.assertRaises(checkpoint.CheckpointError):
                self.prepare(changed)
        for field in ("ai_review.py", "ai_prompts.py"):
            changed = copy.deepcopy(self.new_binding); changed["code"][field] = "e"*64
            with self.subTest(code=field), self.assertRaises(checkpoint.CheckpointError):
                self.prepare(changed)
        for update in ({"recovery_policy": "extended-v2"}, {"stream": False}, {"max_output": 32768}, {"max_requests": 25}):
            changed = copy.deepcopy(self.new_binding); changed["policy"].update(update)
            with self.subTest(policy=update), self.assertRaises(checkpoint.CheckpointError):
                self.prepare(changed)
        changed = copy.deepcopy(self.new_binding); changed["static_files"]["../outside.json"] = "a"*64
        with self.assertRaises(checkpoint.CheckpointError):
            self.prepare(changed)
        self.assertFalse((self.output/"ai-checkpoint.json").exists())

    def test_original_unit_or_response_tampering_and_static_damage_reject(self):
        path = self.output/"ai-resume-checkpoint.json"
        original = path.read_bytes()
        for field in ("units", "responses"):
            value = json.loads(original)
            if field == "units":
                value["units"]["d0"]["result"]["overview"] = "damaged"
            else:
                value["responses"]["a"*64]["usage"] = {"total_tokens": 0}
            raw = json.dumps(value).encode(); path.write_bytes(raw)
            self.summary["ai_recovery_inputs"]["checkpoint_sha256"] = hashlib.sha256(raw).hexdigest()
            with self.subTest(field=field), self.assertRaises(checkpoint.CheckpointError):
                self.prepare()
        path.write_bytes(original)
        self.summary["ai_recovery_inputs"]["checkpoint_sha256"] = hashlib.sha256(original).hexdigest()
        (self.output/"priority-target.json").write_text("same path wrong frozen bytes", encoding="utf-8")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "static bytes"):
            self.prepare()

    def test_journal_drift_and_private_source_body_reject_without_adopting_ids(self):
        evidence = FakeEvidence(self.document)
        evidence.document["tools"][-1]["result"]["changed"] = True
        with self.assertRaisesRegex(checkpoint.CheckpointError, "public tool replay"):
            self.prepare(evidence=evidence)
        self.assertEqual(len(evidence.journal), 3)
        self.assertEqual(evidence.calls, 0)
        private = copy.deepcopy(self.document); private["tools"][-1]["result"]["source"] = "private source body"
        (self.artifact/"ai-evidence.json").write_text(json.dumps(private), encoding="utf-8")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "private"):
            recovery.restore_inputs(self.root/"private", list(self.artifact.iterdir()), 987)

    def test_extended_artifact_restore_uses_ancestor_prefix_and_preserves_paid_history(self):
        self.prepare()
        value = self.opened()
        token = value.claim("draft", "d2", "b"*64, "backup", "session")
        value.received(token, "b"*64, {"role": "assistant", "content": None}, {"_usage_unknown": True}, "m")
        value.close()
        files = list(self.output.iterdir())
        target = self.root/"resumed"
        metadata = recovery.restore_inputs(target, files, 988)
        for name in self.new_binding["static_files"]:
            (target/name).write_bytes((self.output/name).read_bytes())
        summary = {**self.summary, "checkpoint_from_run": 988, "ai_recovery_inputs": metadata}
        proof = recovery.prepare_recovery(target, summary, self.new_binding, FakeEvidence(self.document))
        self.assertEqual(proof["imported_units"], ["d0", "d1"])
        self.assertEqual(proof["adopted_attempt_count"], 9)
        restored = json.loads((target/"ai-checkpoint.json").read_text())
        self.assertEqual(len(restored["attempts"]), 10)
        self.assertEqual(restored["transport_retries"], 3)
        self.assertFalse(restored["recovery"]["resume_transport_retry_pending"])

    def test_default_stays_strict_and_extension_does_not_reset_caps(self):
        self.assertEqual(recovery.prepare_recovery(self.output, {}, self.binding, None),
                         {"migrated": False, "imported_units": []})
        with self.assertRaises(checkpoint.CheckpointError):
            checkpoint.Checkpoint(self.root/"unproven", self.new_binding)
        self.prepare(); value = self.opened()
        for index in range(2):
            request = format(100+index, "064x")
            token = value.claim("draft", "d2", request, "backup", "s", transport_retry=True)
            value.received(token, request, {"role": "assistant", "content": None}, {}, "m")
        self.assertEqual(value.value["transport_retries"], 4)
        with self.assertRaisesRegex(checkpoint.CheckpointError, "compensation"):
            value.claim("draft", "d2", "e"*64, "backup", "s", transport_retry=True)
        for index in range(24-len(value.value["attempts"])):
            request = format(200+index, "064x")
            token = value.claim("draft", "d2", request, "backup", "s")
            value.received(token, request, {"role": "assistant", "content": None}, {}, "m")
        value.close(); resumed = self.opened()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "request budget"):
            resumed.claim("draft", "d2", "f"*64, "backup", "s")
        self.assertEqual(len(resumed.value["attempts"]), 24)

    def test_completion_adopts_full_latest_parent_and_preserves_all_paid_accounting(self):
        fixture = self.completion_fixture()
        metadata = self.prepare_completion(fixture)
        value = json.loads((fixture.target/"ai-checkpoint.json").read_text())
        for name in ("attempts", "units", "responses", "providers", "transport_retries", "elapsed_seconds", "created_at"):
            with self.subTest(field=name):
                self.assertEqual(value[name], fixture.original[name])
        self.assertEqual(len(value["attempts"]), 21)
        self.assertEqual(value["transport_retries"], 3)
        self.assertGreater(value["elapsed_seconds"], 1800)
        self.assertEqual(metadata["imported_units"], ["d"+str(index) for index in range(5)])
        self.assertEqual(metadata["imported_review_units"], ["r0"])
        self.assertEqual(metadata["original_review_start"], 14)
        self.assertEqual(metadata["adopted_attempt_count"], 21)
        self.assertEqual(value["recovery"]["parent_recovery"], fixture.original["recovery"])
        self.assertEqual(value["recovery"]["original_binding"], fixture.original["binding"])
        self.assertEqual(value["recovery"]["old_limits"]["max_requests"], 24)
        self.assertEqual(value["recovery"]["new_limits"]["max_requests"], 32)
        self.assertEqual((fixture.target/"ai-completion-checkpoint.json").read_bytes(),
                         (fixture.parent/"ai-checkpoint.json").read_bytes())
        self.assertFalse((fixture.target/"ai-resume-checkpoint.json").exists())

    def test_completion_review_compensation_spends_remaining_slot_once_and_keeps_request_cap(self):
        fixture = self.completion_fixture(); self.prepare_completion(fixture)
        value = checkpoint.Checkpoint(fixture.target, fixture.binding)
        try:
            for stage, unit in (("draft", "r1"), ("review", "r0"), ("review", "r2")):
                with self.subTest(stage=stage, unit=unit), self.assertRaisesRegex(checkpoint.CheckpointError, "reserved"):
                    value.claim(stage, unit, "a"*64, "backup", "continuation")
            self.assertEqual(len(value.value["attempts"]), 21)
            self.assertEqual(value.value["transport_retries"], 3)
            token = value.claim("review", "r1", "a1"*32, "backup", "continuation")
            value.received(token, "a1"*32, {"role": "assistant", "content": None}, {"total_tokens": 7}, "m")
            value.save_unit("r1", {"pages": [], "findings": [], "remaining_gaps": []})
        finally:
            value.close()
        metadata = self.prepare_completion(fixture)
        self.assertEqual(metadata["imported_review_units"], ["r0", "r1"])
        self.assertEqual(metadata["adopted_attempt_count"], 21)
        resumed = checkpoint.Checkpoint(fixture.target, fixture.binding)
        try:
            self.assertEqual(resumed.value["transport_retries"], 4)
            with self.assertRaisesRegex(checkpoint.CheckpointError, "compensation"):
                resumed.claim("review", "r2", "b"*64, "backup", "continuation", transport_retry=True)
            for index in range(10):
                request = format(index+100, "064x")
                token = resumed.claim("review", "r2", request, "backup", "continuation")
                resumed.received(token, request, {"role": "assistant", "content": None}, {}, "m")
            self.assertEqual(len(resumed.value["attempts"]), 32)
            with self.assertRaisesRegex(checkpoint.CheckpointError, "request budget"):
                resumed.claim("review", "r2", "c"*64, "backup", "continuation")
            self.assertEqual(resumed.value["attempts"][:21], fixture.original["attempts"])
        finally:
            resumed.close()

    def test_same_completion_resume_restores_active_reviews_and_new_evidence_without_recharging(self):
        fixture = self.completion_fixture(); self.prepare_completion(fixture)
        value = checkpoint.Checkpoint(fixture.target, fixture.binding)
        try:
            token = value.claim("review", "r1", "b"*64, "backup", "continuation")
            value.received(token, "b"*64, {"role": "assistant", "content": None}, {"_usage_unknown": True}, "m")
            value.save_unit("r1", {"pages": [], "findings": [], "remaining_gaps": ["E019"]})
        finally:
            value.close()
        current = copy.deepcopy(fixture.document)
        current["tools"].append({"id": "E019", "tool": "protocol_evidence", "args": {"protocol": "continued"},
                                  "result": {"evidence_id": "E019"}})
        (fixture.target/"ai-evidence.json").write_text(json.dumps(current), encoding="utf-8")
        target = self.root/"completion-resumed"
        inputs = recovery.restore_inputs(target, list(fixture.target.iterdir()), 989, policy="completion-v2")
        self.assertIn("active_evidence_sha256", inputs)
        for name in self.binding["static_files"]:
            (target/name).write_bytes((self.output/name).read_bytes())
        summary = {**fixture.summary, "checkpoint_from_run": 989, "ai_recovery_inputs": inputs}
        metadata = self.prepare_completion(fixture, root=target, summary=summary, document=current)
        restored = json.loads((target/"ai-checkpoint.json").read_text())
        self.assertEqual(metadata["imported_review_units"], ["r0", "r1"])
        self.assertEqual(metadata["restored_tool_rows"], 19)
        self.assertEqual(metadata["original_review_start"], 14)
        self.assertEqual(len(restored["attempts"]), 22)
        self.assertEqual(restored["transport_retries"], 4)
        self.assertEqual(restored["attempts"][:21], fixture.original["attempts"])
        self.assertEqual(restored["recovery"]["parent_recovery"], fixture.original["recovery"])
        self.assertFalse(restored["recovery"]["resume_transport_retry_pending"])

    def test_completion_rejects_missing_drafts_nonprefix_reviews_and_unchanged_budget_bypass(self):
        fixture = self.completion_fixture()
        for change in ("draft", "reviews", "gap", "failed_unit", "compensation", "no_fresh", "default"):
            value = copy.deepcopy(fixture.original); document = copy.deepcopy(fixture.document)
            if change == "draft":
                del value["units"]["d4"]
            elif change == "reviews":
                del value["units"]["r0"]
            elif change == "gap":
                value["units"]["r2"] = value["units"].pop("r0")
            elif change == "failed_unit":
                value["attempts"][-1]["unit"] = "r4"
            elif change == "compensation":
                value["transport_retries"] = 4
            elif change == "no_fresh":
                document["tools"][14]["args"]["page"] = "home"
            else:
                value["binding"]["policy"] = policy()
            with self.subTest(change=change), self.assertRaises(checkpoint.CheckpointError):
                recovery._completion_parent(value, document)
        with self.assertRaises(checkpoint.CheckpointError):
            checkpoint.Checkpoint(self.root/"unproven-completion", fixture.binding)
        with self.assertRaises(checkpoint.CheckpointError):
            recovery._binding(self.binding, fixture.binding)
        for key in ("source_snapshot", "provider_config_sha256", "draft_units", "prompt_version", "matrix_sha256", "static_files"):
            changed = copy.deepcopy(fixture.binding); changed[key] = {} if isinstance(changed[key], dict) else "changed"
            with self.subTest(binding=key), self.assertRaises(checkpoint.CheckpointError):
                recovery._binding(fixture.original["binding"], changed)
        for name in ("ai_review.py", "ai_prompts.py"):
            changed = copy.deepcopy(fixture.binding); changed["code"][name] = "f"*64
            with self.subTest(code=name), self.assertRaises(checkpoint.CheckpointError):
                recovery._binding(fixture.original["binding"], changed)
        self.assertFalse((fixture.target/"ai-checkpoint.json").exists())

    def test_completion_restart_rejects_changed_history_parent_metadata_and_evidence(self):
        fixture = self.completion_fixture(); self.prepare_completion(fixture)
        path = fixture.target/"ai-checkpoint.json"
        raw = path.read_bytes()
        for field in ("attempts", "responses", "units", "providers", "elapsed", "parent_recovery"):
            value = json.loads(raw)
            if field == "attempts":
                value["attempts"][0]["billing_unknown"] = False
            elif field == "responses":
                saved = value["responses"]["a"*64]; saved["usage"] = {"total_tokens": 1}
                saved["response_sha256"] = checkpoint.digest({key: saved[key] for key in ("clean", "usage", "model")})
            elif field == "units":
                saved = value["units"]["d0"]; saved["result"]["overview"] = "changed"
                saved["result_sha256"] = checkpoint.digest(saved["result"])
            elif field == "providers":
                value["providers"]["backup"]["failures"] = 0
            elif field == "elapsed":
                value["elapsed_seconds"] = 0
            else:
                value["recovery"]["parent_recovery"]["parent_run"] += 1
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.subTest(field=field), self.assertRaises(checkpoint.CheckpointError):
                recovery.restore_inputs(self.root/("changed-"+field), list(fixture.target.iterdir()), 989,
                                        policy="completion-v2")
        path.write_bytes(raw)
        changed = copy.deepcopy(fixture.document); changed["tools"][0]["result"]["drift"] = True
        (fixture.target/"ai-evidence.json").write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "evidence changed"):
            recovery.restore_inputs(self.root/"changed-evidence", list(fixture.target.iterdir()), 989,
                                    policy="completion-v2")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "explicit completion"):
            recovery.restore_inputs(self.root/"implicit-completion", list(fixture.target.iterdir()), 989)

    def test_final_adopts_all_twenty_three_attempts_seven_units_and_nested_provenance(self):
        fixture = self.final_fixture()
        metadata = self.prepare_completion(fixture)
        value = json.loads((fixture.target/"ai-checkpoint.json").read_text())
        for name in ("attempts", "responses", "units", "providers", "transport_retries", "elapsed_seconds", "created_at"):
            with self.subTest(field=name):
                self.assertEqual(value[name], fixture.original[name])
        self.assertEqual(len(value["attempts"]), 23)
        self.assertEqual(len(value["units"]), 7)
        self.assertEqual(value["transport_retries"], 4)
        self.assertGreater(value["elapsed_seconds"], 2279)
        self.assertEqual(metadata["adopted_attempt_count"], 23)
        self.assertEqual(metadata["imported_review_units"], ["r0", "r1"])
        self.assertEqual(metadata["original_review_start"], 14)
        self.assertEqual(value["recovery"]["parent_recovery"], fixture.original["recovery"])
        self.assertEqual(value["recovery"]["parent_recovery"]["policy"], "completion-v2")
        self.assertEqual(value["recovery"]["parent_recovery"]["parent_recovery"]["policy"], "extended-v1")
        self.assertEqual(value["recovery"]["old_limits"]["max_requests"], 32)
        self.assertEqual(value["recovery"]["new_limits"]["max_requests"], 40)
        self.assertEqual(value["recovery"]["next_retry_unit"], "r2")
        self.assertTrue(value["attempts"][-1]["billing_unknown"])
        self.assertTrue(value["attempts"][0]["billing_unknown"])
        self.assertEqual(value["attempts"][-2]["usage"]["completion_tokens_details"]["reasoning_tokens"], 9316)
        self.assertEqual((fixture.target/"ai-final-checkpoint.json").read_bytes(),
                         (fixture.parent/"ai-checkpoint.json").read_bytes())
        self.assertFalse((fixture.target/"ai-completion-checkpoint.json").exists())

    def test_final_pending_r2_spends_fifth_compensation_then_sixth_and_caps_at_forty(self):
        fixture = self.final_fixture(); self.prepare_completion(fixture)
        value = checkpoint.Checkpoint(fixture.target, fixture.binding)
        try:
            for stage, unit in (("draft", "r2"), ("review", "r1"), ("review", "r3")):
                with self.subTest(stage=stage, unit=unit), self.assertRaisesRegex(checkpoint.CheckpointError, "reserved"):
                    value.claim(stage, unit, "d1"*32, "backup", "final")
            self.assertEqual(value.value["transport_retries"], 4)
            for index in range(2):
                request = format(400+index, "064x")
                token = value.claim("review", "r2", request, "backup", "final", transport_retry=index == 1)
                value.received(token, request, {"role": "assistant", "content": None}, {"total_tokens": 1}, "m")
                self.assertEqual(value.value["transport_retries"], 5+index)
            value.save_unit("r2", {"pages": [], "findings": [], "remaining_gaps": []})
        finally:
            value.close()
        metadata = self.prepare_completion(fixture)
        self.assertEqual(metadata["adopted_attempt_count"], 23)
        self.assertEqual(metadata["imported_review_units"], ["r0", "r1", "r2"])
        resumed = checkpoint.Checkpoint(fixture.target, fixture.binding)
        try:
            self.assertEqual(resumed.value["transport_retries"], 6)
            with self.assertRaisesRegex(checkpoint.CheckpointError, "compensation"):
                resumed.claim("review", "r3", "d"*64, "backup", "final", transport_retry=True)
            for index in range(40-len(resumed.value["attempts"])):
                request = format(500+index, "064x")
                token = resumed.claim("review", "r3", request, "backup", "final")
                resumed.received(token, request, {"role": "assistant", "content": None}, {}, "m")
            with self.assertRaisesRegex(checkpoint.CheckpointError, "request budget"):
                resumed.claim("review", "r3", "e"*64, "backup", "final")
            self.assertEqual(len(resumed.value["attempts"]), 40)
            self.assertEqual(resumed.value["attempts"][:23], fixture.original["attempts"])
        finally:
            resumed.close()

    def test_same_final_restore_preserves_new_review_evidence_and_does_not_recharge(self):
        fixture = self.final_fixture(); self.prepare_completion(fixture)
        value = checkpoint.Checkpoint(fixture.target, fixture.binding)
        try:
            token = value.claim("review", "r2", "d"*64, "backup", "final")
            value.received(token, "d"*64, {"role": "assistant", "content": None}, {"_usage_unknown": True}, "m")
            value.save_unit("r2", {"pages": [], "findings": [], "remaining_gaps": ["E019"]})
        finally:
            value.close()
        current = copy.deepcopy(fixture.document)
        current["tools"].append({"id": "E019", "tool": "protocol_evidence", "args": {"protocol": "final-read"},
                                  "result": {"evidence_id": "E019"}})
        (fixture.target/"ai-evidence.json").write_text(json.dumps(current), encoding="utf-8")
        target = self.root/"final-resumed"
        inputs = recovery.restore_inputs(target, list(fixture.target.iterdir()), 990, policy="completion-v3")
        for name in self.binding["static_files"]:
            (target/name).write_bytes((self.output/name).read_bytes())
        summary = {**fixture.summary, "checkpoint_from_run": 990, "ai_recovery_inputs": inputs}
        metadata = self.prepare_completion(fixture, root=target, summary=summary, document=current)
        restored = json.loads((target/"ai-checkpoint.json").read_text())
        self.assertEqual(metadata["adopted_attempt_count"], 23)
        self.assertEqual(metadata["imported_review_units"], ["r0", "r1", "r2"])
        self.assertEqual(metadata["original_review_start"], 14)
        self.assertEqual(metadata["restored_tool_rows"], 19)
        self.assertEqual(len(restored["attempts"]), 24)
        self.assertEqual(restored["transport_retries"], 5)
        self.assertFalse(restored["recovery"]["resume_transport_retry_pending"])
        self.assertEqual(restored["attempts"][:23], fixture.original["attempts"])
        self.assertEqual(restored["recovery"]["parent_recovery"], fixture.original["recovery"])
        changed = json.loads((target/"ai-checkpoint.json").read_text())
        changed["recovery"]["parent_recovery"]["parent_run"] += 1
        (target/"ai-checkpoint.json").write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "immutable parent"):
            recovery.restore_inputs(self.root/"final-tampered", list(target.iterdir()), 991, policy="completion-v3")

    def test_final_rejects_skips_downgrades_unknown_generations_and_changed_same_policy(self):
        fixture = self.final_fixture()
        for old in (self.binding, self.new_binding, fixture.binding):
            new = fixture.binding if old != fixture.binding else fixture.original["binding"]
            with self.subTest(old=old["policy"].get("recovery_policy")), self.assertRaises(checkpoint.CheckpointError):
                recovery._binding(old, new)
        for policy in (None, "extended-v1", "completion-v4"):
            with self.subTest(policy=policy), self.assertRaises(checkpoint.CheckpointError):
                recovery.restore_inputs(self.root/("invalid-final-"+str(policy)), list(fixture.parent.iterdir()), 990,
                                        policy=policy)
        changed = copy.deepcopy(fixture.binding); changed["code"]["ai_pipeline.py"] = "1"*64
        with self.assertRaisesRegex(checkpoint.CheckpointError, "binding changed"):
            recovery._binding(fixture.binding, changed)
        for field in ("ai_review.py", "ai_prompts.py"):
            changed = copy.deepcopy(fixture.binding); changed["code"][field] = "1"*64
            with self.subTest(code=field), self.assertRaises(checkpoint.CheckpointError):
                recovery._binding(fixture.original["binding"], changed)
        changed = copy.deepcopy(fixture.original); changed["transport_retries"] = 6
        with self.assertRaisesRegex(checkpoint.CheckpointError, "remaining compensation"):
            recovery._completion_parent(changed, fixture.document, "completion-v3")
        with self.assertRaises(checkpoint.CheckpointError):
            checkpoint.Checkpoint(self.root/"unproven-final", fixture.binding)


if __name__ == "__main__": unittest.main()
