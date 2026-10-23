"""Explicit, bounded migration of verified public AI receipts; never replay a POST."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import time
import uuid

import ai_checkpoint as checkpoint
import hostlab
import remote_schedule

POLICY = "extended-v1"
FILES = {"ai-checkpoint.json": "ai-resume-checkpoint.json", "ai-evidence.json": "ai-resume-evidence.json"}
COMPLETION_POLICY = "completion-v2"
COMPLETION_FILES = {"ai-checkpoint.json": "ai-completion-checkpoint.json",
                    "ai-evidence.json": "ai-completion-evidence.json"}
FINAL_POLICY = "completion-v3"
FINAL_FILES = {"ai-checkpoint.json": "ai-final-checkpoint.json", "ai-evidence.json": "ai-final-evidence.json"}
RECOVERY_FILES = {POLICY: FILES, COMPLETION_POLICY: COMPLETION_FILES, FINAL_POLICY: FINAL_FILES}
MUTABLE_CODE = {"ai_pipeline.py", "ai_checkpoint.py", "ai_transport.py"}
BOUND_CODE = MUTABLE_CODE | {"ai_prompts.py", "ai_review.py"}
# This exact change only replaces the decompiler subprocess wrapper. Frozen recovery
# disables that tool; validators and prompts are unchanged. No arbitrary reviewer drift.
FROZEN_REVIEWER_MIGRATION = (
    "5fece6d07a49eafb993cb3da530b1564c03844efe701706df58fa0a108c4ecfb",
    "c11e3134bc28797b27a3394976cc46ca03192a483d5c9ca943149265cc5732e3",
)


def _read(path):
    checkpoint.regular(path)
    raw = path.read_bytes()
    try:
        return raw, json.loads(raw)
    except (ValueError, UnicodeError):
        raise checkpoint.CheckpointError("invalid recovery JSON") from None


def _atomic_bytes(path, raw):
    checkpoint.regular(path, missing=True)
    if path.exists():
        if path.read_bytes() != raw:
            raise checkpoint.CheckpointError("refusing to replace different recovery history")
        return
    stage = path.with_name(".ai-recovery-"+uuid.uuid4().hex+".tmp")
    try:
        with stage.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(stage, path)
    finally:
        stage.unlink(missing_ok=True)


def _public_evidence(value):
    if (not isinstance(value, dict) or set(value) != {"E000", "tools"}
            or not isinstance(value["E000"], dict) or not isinstance(value["tools"], list)
            or not 1 <= len(value["tools"]) <= 32):
        raise checkpoint.CheckpointError("invalid public recovery evidence")
    def public(item, parent=""):
        if isinstance(item, dict):
            for key, child in item.items():
                if key == "messages" or key == "source" and parent not in {"sample", "baseline"}:
                    raise checkpoint.CheckpointError("private body is not a public recovery receipt")
                public(child, key)
        elif isinstance(item, list):
            for child in item:
                public(child, parent)
    public(value)
    for index, row in enumerate(value["tools"], 1):
        if (not isinstance(row, dict) or set(row) != {"id", "tool", "args", "result"}
                or row["id"] != "E"+str(index).zfill(3) or not isinstance(row["args"], dict)
                or not isinstance(row["result"], dict) or row["result"].get("evidence_id") != row["id"]):
            raise checkpoint.CheckpointError("invalid recovery tool receipt identity")
        schemas = {"page_evidence": {"page"}, "family_evidence": {"family", "side"},
                   "protocol_evidence": {"protocol", "side"}, "module_source": {"path"}}
        if (row["tool"] not in schemas or set(row["args"])-schemas[row["tool"]]
                or not all(isinstance(value, str) and 0 < len(value) <= 1024 for value in row["args"].values())
                or "side" in row["args"] and row["args"]["side"] not in {"target", "baseline"}
                or row["tool"] == "module_source" and {"source", "excerpt"} & set(row["result"])):
            raise checkpoint.CheckpointError("unapproved or private recovery tool receipt")
        required = schemas[row["tool"]]-{"side"}
        if not required <= set(row["args"]):
            raise checkpoint.CheckpointError("missing recovery tool arguments")
    return value


def restore_inputs(root, verifiedfiles, parent_run, policy=POLICY):
    """Accept only the two public files in the caller's verified artifact inventory."""
    if type(parent_run) is not int or parent_run <= 0 or not isinstance(policy, str) or policy not in RECOVERY_FILES:
        raise checkpoint.CheckpointError("invalid recovery parent run")
    root = Path(root); root.mkdir(parents=True, exist_ok=True)
    def selected(name):
        selected = [Path(path) for path in verifiedfiles if Path(path).name == name]
        if len(selected) != 1:
            raise checkpoint.CheckpointError("missing or ambiguous public recovery file: "+name)
        return _read(selected[0])
    active_raw, active = selected("ai-checkpoint.json")
    checkpoint.validate(active)
    active_policy = active["binding"].get("policy", {}).get("recovery_policy")
    if policy != POLICY:
        if active_policy not in (checkpoint.PARENT_POLICY[policy], policy):
            raise checkpoint.CheckpointError("completion recovery requires its immediate named parent policy")
        files = RECOVERY_FILES[policy]
        repeated = active_policy == policy
        raw, original = selected(files["ai-checkpoint.json"] if repeated else "ai-checkpoint.json")
        evidence_raw, document = selected(files["ai-evidence.json"] if repeated else "ai-evidence.json")
        checkpoint.validate(original); _public_evidence(document)
        _completion_parent(original, document, policy)
        metadata = {"parent_run": parent_run, "checkpoint_sha256": hashlib.sha256(raw).hexdigest(),
                    "evidence_sha256": hashlib.sha256(evidence_raw).hexdigest()}
        if repeated:
            _history(active, original, metadata, document)
            current_raw, current = selected("ai-evidence.json")
            _evidence_history(current, document)
            metadata["active_evidence_sha256"] = hashlib.sha256(current_raw).hexdigest()
        else:
            # Each origin is its complete immediate predecessor; verify that
            # predecessor's immutable origin before adopting the latest ledger.
            ancestor_files = RECOVERY_FILES[active_policy]
            ancestor_raw, ancestor = selected(ancestor_files["ai-checkpoint.json"])
            ancestor_evidence_raw, ancestor_document = selected(ancestor_files["ai-evidence.json"])
            checkpoint.validate(ancestor); _public_evidence(ancestor_document)
            _history(active, ancestor, {"checkpoint_sha256": hashlib.sha256(ancestor_raw).hexdigest(),
                "evidence_sha256": hashlib.sha256(ancestor_evidence_raw).hexdigest()}, ancestor_document)
            _evidence_history(document, ancestor_document)
        _atomic_bytes(root/files["ai-checkpoint.json"], raw)
        _atomic_bytes(root/files["ai-evidence.json"], evidence_raw)
        if repeated:
            _atomic_bytes(root/"ai-checkpoint.json", active_raw)
            _atomic_bytes(root/"ai-evidence.json", current_raw)
        return metadata
    if active_policy in (COMPLETION_POLICY, FINAL_POLICY):
        raise checkpoint.CheckpointError("completion parent requires the explicit completion policy")
    extended = active_policy == POLICY
    metadata = {"parent_run": parent_run}
    for name, target in FILES.items():
        raw, value = selected(target if extended else name)
        checkpoint.validate(value) if name == "ai-checkpoint.json" else _public_evidence(value)
        _atomic_bytes(root/target, raw)
        metadata["checkpoint_sha256" if name == "ai-checkpoint.json" else "evidence_sha256"] = hashlib.sha256(raw).hexdigest()
    if extended:
        _, original = _read(root/FILES["ai-checkpoint.json"])
        _history(active, original, metadata)
        _atomic_bytes(root/"ai-checkpoint.json", active_raw)
    return metadata


def _history(value, original, inputs, document=None):
    recovery = value.get("recovery", {})
    count = recovery.get("adopted_attempt_count")
    _binding(original["binding"], value["binding"])
    if (recovery.get("origin_checkpoint_sha256") != inputs["checkpoint_sha256"]
            or recovery.get("evidence_sha256") != inputs["evidence_sha256"]
            or recovery.get("original_binding") != original["binding"]
            or count != len(original["attempts"]) or recovery.get("adopted_units") != _draft_prefix(original)
            or value["attempts"][:count] != original["attempts"]
            or any(value["units"].get(name) != saved for name, saved in original["units"].items())
            or any(value["responses"].get(name) != saved for name, saved in original["responses"].items())
            or value["transport_retries"] < original["transport_retries"]
            or value["elapsed_seconds"] < original["elapsed_seconds"]):
        raise checkpoint.CheckpointError("extended recovery changed its immutable origin history")
    if recovery.get("policy") in (COMPLETION_POLICY, FINAL_POLICY):
        if (document is None or recovery.get("adopted_review_units") != _review_prefix(original)
                or recovery.get("original_review_start") != _completion_parent(original, document, recovery["policy"])
                or recovery.get("parent_recovery") != original.get("recovery")):
            raise checkpoint.CheckpointError("completion recovery changed its immutable parent history")
        touched = {row["profile"] for row in value["attempts"][count:]}
        if (not set(original["providers"]) <= set(value["providers"])
                or any(value["providers"][name] != saved for name, saved in original["providers"].items()
                       if name not in touched)):
            raise checkpoint.CheckpointError("completion recovery changed its inherited provider state")
    if recovery["resume_transport_retry_pending"]:
        if (len(value["attempts"]) != count or value["transport_retries"] != original["transport_retries"]
                or recovery["next_retry_unit"] != original["attempts"][-1]["unit"]):
            raise checkpoint.CheckpointError("recovery compensation reservation changed")
    elif (len(value["attempts"]) <= count or not value["attempts"][count].get("transport_retry")
            or value["attempts"][count]["unit"] != original["attempts"][-1]["unit"]):
        raise checkpoint.CheckpointError("recovery compensation receipt is missing")


def _binding(old, new):
    checkpoint.policy_limits(old); checkpoint.policy_limits(new)
    old_policy = old.get("policy", {}).get("recovery_policy")
    new_policy = new.get("policy", {}).get("recovery_policy")
    if old_policy in RECOVERY_FILES and old_policy == new_policy:
        if old != new:
            raise checkpoint.CheckpointError("extended recovery binding changed")
        return
    if new_policy not in RECOVERY_FILES or old_policy != checkpoint.PARENT_POLICY[new_policy]:
        raise checkpoint.CheckpointError("explicit extended recovery policy required")
    comparable = copy.deepcopy(old)
    names = {"priority-target.json"} | ({"priority-baseline.json"} if old.get("baseline") else set())
    if (old.get("no_apk_access") is False and new.get("no_apk_access") is True and
            old.get("static_manifest_sha256") is None and set(old.get("static_files", {})) == names and
            set(new.get("static_files", {})) == names | {"static-manifest.json"} and
            all(old["static_files"][name] == new["static_files"][name] for name in names) and
            checkpoint.HEX.fullmatch(str(new.get("static_manifest_sha256", ""))) and
            new["static_files"]["static-manifest.json"] == new["static_manifest_sha256"]):
        comparable.update(no_apk_access=True, static_files=new["static_files"],
                          static_manifest_sha256=new["static_manifest_sha256"])
    unchanged_code = BOUND_CODE - MUTABLE_CODE
    if (new.get("no_apk_access") is True and
            (old.get("code", {}).get("ai_review.py"), new.get("code", {}).get("ai_review.py")) == FROZEN_REVIEWER_MIGRATION):
        unchanged_code = unchanged_code - {"ai_review.py"}
    if (set(old) != set(new) or set(old.get("code", {})) != BOUND_CODE or set(new.get("code", {})) != BOUND_CODE
            or any(comparable[key] != new[key] for key in old if key not in {"code", "policy"})
            or any(old["code"][key] != new["code"][key] for key in unchanged_code)):
        raise checkpoint.CheckpointError("recovery source/static/prompt/acceptance/provider/plan binding changed")
    expected_policy = {**old["policy"], **checkpoint.RECOVERY_LIMITS[new_policy], "recovery_policy": new_policy}
    if "output_budget" in new["policy"]:
        expected_policy.update(output_budget=checkpoint.OUTPUT_BUDGET, max_output=checkpoint.OUTPUT_TOKENS)
    if new["policy"] != expected_policy:
        raise checkpoint.CheckpointError("recovery changed an unapproved policy field")
    for value in (*old["code"].values(), *new["code"].values()):
        if not isinstance(value, str) or not checkpoint.HEX.fullmatch(value):
            raise checkpoint.CheckpointError("invalid recovery code digest")


def _static(root, binding):
    names = {"priority-target.json", "static-manifest.json"}
    if binding.get("baseline"):
        names.add("priority-baseline.json")
    if set(binding.get("static_files", {})) != names:
        raise checkpoint.CheckpointError("invalid recovery static file paths")
    for name, digest in binding["static_files"].items():
        path = root/name
        info = path.lstat()
        if (not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)
                or getattr(info, "st_file_attributes", 0) & 0x400 or info.st_nlink != 1
                or hostlab.digest(path) != digest):
            raise checkpoint.CheckpointError("recovery frozen static bytes changed")
    if binding["static_files"]["static-manifest.json"] != binding.get("static_manifest_sha256"):
        raise checkpoint.CheckpointError("recovery static manifest identity changed")


def _draft_prefix(value):
    names = sorted((name for name in value["units"] if name.startswith("d")), key=lambda name: int(name[1:]))
    if names != ["d"+str(index) for index in range(len(names))] or len(names) > len(value["binding"].get("draft_units", [])):
        raise checkpoint.CheckpointError("recovery draft units are not a contiguous plan prefix")
    for index, name in enumerate(names):
        result = value["units"][name]["result"]
        if [row.get("page") for row in result.get("pages", [])] != value["binding"]["draft_units"][index]:
            raise checkpoint.CheckpointError("recovery accepted draft page assignment changed")
    return names


def _review_prefix(value):
    names = sorted((name for name in value["units"] if name.startswith("r")), key=lambda name: int(name[1:]))
    if names != ["r"+str(index) for index in range(len(names))] or len(names) > 12:
        raise checkpoint.CheckpointError("recovery review units are not a contiguous plan prefix")
    return names


def _completion_parent(value, document, policy=COMPLETION_POLICY):
    if (policy not in (COMPLETION_POLICY, FINAL_POLICY)
            or value["binding"].get("policy", {}).get("recovery_policy") != checkpoint.PARENT_POLICY[policy]
            or not _draft_prefix(value)
            or len(_draft_prefix(value)) != len(value["binding"].get("draft_units", []))
            or not _review_prefix(value)):
        raise checkpoint.CheckpointError("completion recovery requires every draft and an accepted review prefix")
    attempts = value["attempts"]
    if (not attempts or attempts[-1].get("status") != "failed" or not attempts[-1].get("retryable")
            or attempts[-1].get("stage") != "review"
            or attempts[-1].get("unit") != "r"+str(len(_review_prefix(value)))
            or value["transport_retries"] >= checkpoint.RECOVERY_LIMITS[policy]["transport_retries"]):
        raise checkpoint.CheckpointError("completion recovery requires its next retryable review and remaining compensation")
    pages = [page for unit in value["binding"]["draft_units"] for page in unit]
    rows = document["tools"]
    prefetched = rows[:len(pages)]
    prefetch_pages = [row["args"].get("page") for row in prefetched]
    refresh = [page for page in prefetch_pages if page in {"comment", "dynamic"}]
    if (not refresh or len(rows) < len(pages)+len(refresh)
            or len(set(pages)) != len(pages) or set(prefetch_pages) != set(pages)
            or any(row["tool"] != "page_evidence" or set(row["args"]) != {"page"} for row in prefetched)):
        raise checkpoint.CheckpointError("completion recovery lacks its original page prefetch")
    start = next((index for index in range(len(pages), len(rows)) if rows[index]["tool"] == "page_evidence"), None)
    if (start is None or [row["args"] for row in rows[start:start+len(refresh)]] != [{"page": page} for page in refresh]
            or any(row["tool"] != "page_evidence" for row in rows[start:start+len(refresh)])):
        raise checkpoint.CheckpointError("completion recovery lacks its original fresh review boundary")
    return start


def _evidence_history(current, original):
    _public_evidence(current)
    if current["E000"] != original["E000"] or current["tools"][:len(original["tools"])] != original["tools"]:
        raise checkpoint.CheckpointError("completion recovery evidence changed its immutable parent prefix")


def _rebuild(evidence, document):
    rows = document["tools"]
    current = evidence.public_journal()
    pages = list(evidence.summary["page_path_matrix"])
    if (not current or current != rows[:len(current)]
            or [row.get("args", {}).get("page") for row in current] != pages
            or any(row["tool"] != "page_evidence" for row in current)):
        raise checkpoint.CheckpointError("recovery prefetched page receipts differ")
    prior = copy.deepcopy((evidence.journal, evidence.ids, evidence.calls, evidence.limit))
    try:
        for row in rows[len(current):]:
            if row["tool"] == "page_evidence":
                evidence.server_read(row["tool"], row["args"])
            else:
                evidence.run_tool(row["tool"], row["args"])
        if evidence.public_journal() != rows:
            raise checkpoint.CheckpointError("recovery public tool replay differs from its verified receipts")
    except BaseException:
        evidence.journal, evidence.ids, evidence.calls, evidence.limit = prior
        raise


def _corrected_wire_stop(original, new_binding):
    """One explicit migration for the former default SSE envelope limit.

    Retain the original nonretryable/unknown-billing receipt verbatim. This is
    never normal automatic retry permission for malformed or oversized output.
    """
    if (original["binding"]["policy"].get("recovery_policy") is not None
            or new_binding["policy"].get("recovery_policy") != POLICY
            or original["binding"]["code"]["ai_transport.py"] == new_binding["code"]["ai_transport.py"]):
        return False
    last = original["attempts"][-1] if original["attempts"] else {}
    metrics = last.get("metrics") or {}
    size, events = metrics.get("response_bytes"), metrics.get("events")
    return (last.get("status") == "failed" and last.get("kind") == "protocol"
        and last.get("reason") == "API response exceeds bound" and last.get("retryable") is False
        and last.get("http_status") is None and type(size) is int and 2*1024*1024 < size <= 2*1024*1024+8192
        and type(events) is int and 1 <= events <= 65536)


def prepare_recovery(root, summary, new_binding, evidence):
    """Rebuild read-only evidence, then atomically adopt a bounded ledger migration."""
    policy = summary.get("ai_recovery_policy")
    if policy is None:
        return {"migrated": False, "imported_units": []}
    if not isinstance(policy, str) or policy not in RECOVERY_FILES:
        raise checkpoint.CheckpointError("unknown AI recovery policy")
    completion = policy != POLICY
    inputs = summary.get("ai_recovery_inputs")
    required = {"parent_run", "checkpoint_sha256", "evidence_sha256"}
    allowed = required | ({"active_evidence_sha256"} if completion else set())
    if (not isinstance(inputs, dict) or not required <= set(inputs) <= allowed
            or type(inputs["parent_run"]) is not int or inputs["parent_run"] <= 0
            or summary.get("checkpoint_from_run") != inputs["parent_run"]):
        raise checkpoint.CheckpointError("explicit recovery needs verified parent-run inputs")
    root = Path(root)
    files = RECOVERY_FILES[policy]
    raw, original = _read(root/files["ai-checkpoint.json"])
    evidence_raw, document = _read(root/files["ai-evidence.json"])
    if (hashlib.sha256(raw).hexdigest() != inputs["checkpoint_sha256"]
            or hashlib.sha256(evidence_raw).hexdigest() != inputs["evidence_sha256"]):
        raise checkpoint.CheckpointError("verified recovery input bytes changed")
    checkpoint.validate(original); _public_evidence(document)
    _binding(original["binding"], new_binding); _static(root, new_binding)
    imported = _draft_prefix(original)
    review_start = _completion_parent(original, document, policy) if completion else None
    if not completion and original["binding"].get("policy", {}).get("recovery_policy") != POLICY and any(name.startswith("r") for name in original["units"]):
        raise checkpoint.CheckpointError("initial extended recovery cannot import accepted review units")
    if (not original["attempts"] or original["attempts"][-1].get("status") != "failed"
            or not original["attempts"][-1].get("retryable") and not _corrected_wire_stop(original, new_binding)):
        raise checkpoint.CheckpointError("extended recovery needs an original retryable failed request")
    active_document = document
    if "active_evidence_sha256" in inputs:
        current_raw, active_document = _read(root/"ai-evidence.json")
        if hashlib.sha256(current_raw).hexdigest() != inputs["active_evidence_sha256"]:
            raise checkpoint.CheckpointError("verified active recovery evidence bytes changed")
        _evidence_history(active_document, document)
    _rebuild(evidence, active_document)
    path = root/"ai-checkpoint.json"
    checkpoint.regular(root/"ai-checkpoint.lock", missing=True)
    lock = remote_schedule.admission_lock(root/"ai-checkpoint.lock")
    if lock is None:
        raise checkpoint.CheckpointError("AI recovery checkpoint is already in use")
    try:
        if path.exists():
            _, existing = _read(path); checkpoint.validate(existing)
            if (existing["binding"] != new_binding or existing.get("recovery", {}).get("origin_checkpoint_sha256") !=
                    (inputs["checkpoint_sha256"] if completion else
                     original.get("recovery", {}).get("origin_checkpoint_sha256", inputs["checkpoint_sha256"]))):
                raise checkpoint.CheckpointError("refusing to overwrite a different active recovery ledger")
            value = existing
            _history(value, original, inputs, document)
            imported = value["recovery"]["adopted_units"]
        else:
            value = copy.deepcopy(original)
            value["binding"] = copy.deepcopy(new_binding)
            value["binding_sha256"] = checkpoint.digest(new_binding)
            value["recovery"] = {"schema": 1, "policy": policy, "parent_run": inputs["parent_run"],
                "origin_checkpoint_sha256": inputs["checkpoint_sha256"], "evidence_sha256": inputs["evidence_sha256"],
                "original_binding": copy.deepcopy(original["binding"]), "original_binding_sha256": original["binding_sha256"],
                "old_limits": checkpoint.policy_limits(original["binding"]), "new_limits": checkpoint.policy_limits(new_binding),
                "resume_transport_retry_pending": True, "next_retry_unit": original["attempts"][-1]["unit"],
                "adopted_units": imported, "adopted_attempt_count": len(original["attempts"]), "migrated_at": time.time(),
                "migration_tool_sha256": hostlab.digest(Path(__file__))}
            if completion:
                value["recovery"].update(parent_recovery=copy.deepcopy(original["recovery"]),
                    adopted_review_units=_review_prefix(original), original_review_start=review_start)
            checkpoint.validate(value)
            checkpoint.atomic(path, value)
    finally:
        lock.close()
    result = {"migrated": True, "imported_units": imported, "recovery": copy.deepcopy(value["recovery"]),
            "adopted_attempt_count": value["recovery"]["adopted_attempt_count"],
            "restored_tool_rows": len(evidence.journal), "restored_model_tool_calls": evidence.calls}
    if completion:
        result.update(imported_review_units=_review_prefix(value), original_review_start=review_start)
    return result
