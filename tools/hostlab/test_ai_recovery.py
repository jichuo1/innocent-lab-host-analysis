"""Recovery changes budgets once; public evidence and paid history remain immutable."""
import copy
import hashlib
import json
from pathlib import Path
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
        self.summary = {"page_path_matrix": {page: {} for page in ("p0", "p1", "p2")}}
        self.journal = copy.deepcopy(document["tools"][:3])
        self.ids = {"E000", *[row["id"] for row in self.journal]}
        self.calls = 0
        self.limit = 6

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

    def opened(self):
        value = checkpoint.Checkpoint(self.output, self.new_binding)
        self.addCleanup(value.close)
        return value

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


if __name__ == "__main__": unittest.main()
