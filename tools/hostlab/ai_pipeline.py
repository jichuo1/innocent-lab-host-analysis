"""Bounded page shards with durable request receipts and independent review."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time
from types import SimpleNamespace

import ai_checkpoint
import ai_prompts
import hostlab

MAX_OUTPUT = 8192
MAX_DRAFT_UNITS = 6
UNIT_PAGES = 2
UNIT_PATHS = 10


def merge_items(values, limit):
    """Keep every unique item verbatim while bounding the number of output strings."""
    unique = list(dict.fromkeys(values))
    if len(unique) <= limit:
        return unique, len(unique)
    width = math.ceil(len(unique)/limit)
    merged = ["\n".join("["+str(index+1)+"] "+unique[index] for index in range(start, min(start+width, len(unique))))
              for start in range(0, len(unique), width)]
    return merged, len(unique)


def draft_units(matrix):
    order = [page for page in ("comment", "dynamic") if page in matrix]
    order += [page for page in matrix if page not in order]
    units, current, paths = [], [], 0
    for page in order:
        count = len(matrix[page].get("paths", {}))
        if current and (len(current) >= UNIT_PAGES or paths+count > UNIT_PATHS):
            units.append(current); current, paths = [], 0
        current.append(page); paths += count
    if current:
        units.append(current)
    if len(units) > MAX_DRAFT_UNITS:
        raise RuntimeError("page/path plan exceeds six bounded draft units before model dispatch")
    return units


def review_units(priorities, draft):
    pages = list(priorities)
    for row in draft["findings"]:
        if row["page"] not in pages:
            pages.append(row["page"])
    result = []
    for start in range(0, len(pages), UNIT_PAGES):
        assigned = pages[start:start+UNIT_PAGES]
        result.append({"pages": [page for page in assigned if page in priorities],
                       "findings": [row["finding_id"] for row in draft["findings"] if row["page"] in assigned]})
    return result or [{"pages": [], "findings": []}]


def build_binding(root, summary, units):
    root = Path(root)
    files = {}
    for name in ("priority-target.json", "priority-baseline.json", "static-manifest.json"):
        path = root / name
        if path.is_file():
            files[name] = hostlab.digest(path)
    here = Path(__file__).resolve().parent
    code = {name: hostlab.digest(here/name) for name in
            ("ai_pipeline.py", "ai_checkpoint.py", "ai_review.py", "ai_prompts.py", "ai_transport.py")
            if (here/name).is_file()}
    source = summary.get("source_snapshot") or {}
    config = {profile: ai_checkpoint.digest({"base": os.environ.get("AI_"+profile.upper()+"_BASE_URL", "").rstrip("/"),
        "model": os.environ.get("AI_"+profile.upper()+"_MODEL", "")}) for profile in ("primary", "backup")}
    return {"schema": 1, "static_files": files, "static_manifest_sha256": summary.get("static_manifest_sha256"),
        "sample": summary["sample"], "baseline": summary.get("baseline"),
        "matrix_sha256": ai_checkpoint.digest(summary["page_path_matrix"]),
        "source_snapshot": {key: source.get(key) for key in
            ("binding", "source_tree_sha256", "repository_head", "captured_at", "selection_version")},
        "prompt_version": ai_prompts.PROMPT_VERSION, "code": code, "provider_config_sha256": config,
        "draft_units": units, "no_apk_access": summary.get("ai_no_apk_access") is True,
        "policy": {"max_requests": 16, "transport_retries": 2, "deadline_seconds": 1800,
            "max_output": MAX_OUTPUT, "total_timeout": 240, "idle_timeout": 45, "stream": True}}


def seed_for(summary):
    source = summary.get("source_snapshot") or {}
    seed = {"evidence_id": "E000", "sample": summary["sample"], "baseline": summary.get("baseline"),
        "pages": copy.deepcopy(summary["page_path_matrix"]), "changes": summary.get("changes", []),
        "limitations": summary.get("limitations", []), "source_files": [row["path"] for row in source.get("source_records", [])],
        "source_dirty": source.get("working_tree_dirty"),
        "source_snapshot": {key: value for key, value in source.items() if key != "source_records"},
        "unregistered_protocols": summary.get("unregistered_protocols", []),
        "resource_change_counts": {key: len(value) for key, value in (summary.get("resource_changes") or {}).items()
                                   if isinstance(value, list)}}
    for page in seed["pages"].values():
        page["protocols"] = {key: {field: value for field, value in row.items() if field != "signatures"}
                             for key, row in page.get("protocols", {}).items()}
    seed["changes"] = [{key: value for key, value in row.items() if key not in {"before", "after"}}
                       for row in seed["changes"]]
    return seed


def unit_seed(seed, summary, pages):
    records = (summary.get("source_snapshot") or {}).get("source_records", [])
    relevant, common = [], []
    for row in records:
        tags = set(row.get("pages", []))
        markers = row.get("markers", [])
        if tags.intersection(pages) or any(marker == page or marker.startswith(page+"_")
                for marker in markers if isinstance(marker, str) for page in pages):
            relevant.append(row["path"])
        elif not tags:
            common.append(row["path"])
    candidates = list(dict.fromkeys(relevant+common[:8]))
    families = {name for page in pages for name in summary["page_path_matrix"][page].get("paths", {})}
    return {**seed, "pages": {page: seed["pages"][page] for page in pages},
        "changes": [row for row in seed["changes"] if row.get("family") in families],
        "source_files": candidates[:72], "source_files_total": len(records),
        "source_candidates_truncated": len(candidates) > 72,
        "source_catalog_scope": "candidate index only; module_source accepts any exact pinned source path"}


def public_reply(message):
    """Only structured output/tool arguments survive; never persist free text or tool bodies."""
    clean = {"role": "assistant", "content": None}
    calls = []
    allowed = {"family_evidence": {"family", "side"}, "protocol_evidence": {"protocol", "side"},
        "module_source": {"path"}, "decompile_class": {"class_name", "side"},
        "finish_report": {"overview", "pages", "findings", "next_steps"},
        "finish_review": {"pages", "findings", "remaining_gaps"}}
    for index, call in enumerate(message.get("tool_calls", [])[:8]):
        function = call.get("function", {})
        name = function.get("name", "invalid_tool")
        name = name if isinstance(name, str) and re.fullmatch(r"[a-z_]{1,48}", name) else "invalid_tool"
        try:
            args = json.loads(function.get("arguments", "{}"))
            args = public_arguments(name, args) if isinstance(args, dict) else {}
        except (ValueError, TypeError):
            args = {}
        identifier = call.get("id", "")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", identifier):
            identifier = "call-"+str(index)
        calls.append({"id": identifier, "type": "function", "function": {"name": name,
                      "arguments": json.dumps(args, ensure_ascii=False)}})
    if calls:
        clean["tool_calls"] = calls
    return clean


def public_arguments(name, value):
    """Schema fields only: never retain provider-added nested source/messages metadata."""
    string = "string"
    refs = [string]
    path = {key: string for key in ("path", "status", "change", "impact", "verification")}
    path["evidence_ids"] = refs
    page = {"page": string, "assessment": string, "evidence_ids": refs, "path_reviews": [path]}
    finding = {key: string for key in ("title", "page", "level", "analysis", "recommendation", "alternatives")}
    finding["evidence_ids"] = refs
    revision = {key: string for key in ("title", "analysis", "recommendation", "alternatives", "level")}
    review_finding = {key: string for key in ("finding_id", "disposition", "reason")}
    review_finding.update(evidence_ids=refs, revision=revision)
    schemas = {"finish_report": {"overview": string, "pages": [page], "findings": [finding], "next_steps": refs},
        "finish_review": {"pages": [{key: value for key, value in page.items() if key != "path_reviews"}],
            "findings": [review_finding], "remaining_gaps": refs},
        "family_evidence": {"family": string, "side": string}, "protocol_evidence": {"protocol": string, "side": string},
        "module_source": {"path": string}, "decompile_class": {"class_name": string, "side": string}}

    def filtered(item, schema):
        if schema == string:
            return item if isinstance(item, str) else None
        if isinstance(schema, list):
            return [filtered(row, schema[0]) for row in item[:40]] if isinstance(item, list) else None
        if not isinstance(item, dict):
            return None
        return {key: filtered(entry, schema[key]) for key, entry in item.items() if key in schema}

    return filtered(value, schemas[name]) if name in schemas else {}


def public_usage(value):
    if not isinstance(value, dict):
        return {}
    result = {}
    for key, entry in value.items():
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_]{1,64}", key):
            continue
        if key == "_usage_unknown" and type(entry) is bool:
            result[key] = entry
        elif type(entry) in {int, float} and math.isfinite(entry):
            result[key] = entry
        elif isinstance(entry, dict):
            result[key] = {name: count for name, count in entry.items() if isinstance(name, str)
                           and re.fullmatch(r"[A-Za-z0-9_]{1,64}", name) and type(count) in {int, float} and math.isfinite(count)}
            if key == "_transport" and entry.get("finish_reason") in {"stop", "length", "tool_calls", "content_filter"}:
                result[key]["finish_reason"] = entry["finish_reason"]
    return result


def error_info(exc):
    if all(hasattr(exc, key) for key in ("reason", "kind", "retryable", "billing_unknown")):
        return exc
    # Existing mockable callers retain their RuntimeError shape.
    value = str(exc)
    status = re.search(r"API HTTP (\d{3})", value)
    status = int(status[1]) if status else None
    retryable = value.startswith("API failure:") or status in {429, 500, 502, 503, 504}
    return SimpleNamespace(reason=value[:160] if value.startswith("API ") else type(exc).__name__,
        kind="transport" if retryable else "rejected", retryable=retryable,
        billing_unknown=True, http_status=status, retry_after=None, metrics={})


class Coordinator:
    def __init__(self, checkpoint, api, *, profile, deadline):
        self.checkpoint, self.api, self.profile, self.deadline = checkpoint, api, profile, deadline
        self.reused = 0; self.position = 0

    def available_slots(self, reserve_after):
        used_retries = sum(bool(row.get("transport_retry")) for row in self.checkpoint.value["attempts"][:self.position])
        return 16-self.position-reserve_after-max(0, 2-used_retries)

    def request(self, stage, unit, messages, tools, force_tool):
        import ai_review as review
        session = "hostlab-"+ai_checkpoint.digest({"binding": self.checkpoint.value["binding_sha256"], "unit": unit})[:32]
        transport_retry = False
        handled = set()
        while True:
            if len(json.dumps(messages, ensure_ascii=False)) > review.MAX_CONTEXT_CHARS:
                raise RuntimeError("AI review context budget reached")
            request_hash = ai_checkpoint.digest({"profile": self.profile, "messages": messages,
                "tools": tools, "force_tool": force_tool, "session_id": session, "max_output": MAX_OUTPUT})
            cached = self.checkpoint.cached(request_hash)
            if cached is not None:
                self.reused += 1
                self.position = max(self.position, max((index+1 for index, row in enumerate(self.checkpoint.value["attempts"])
                    if row["request_sha256"] == request_hash and row["status"] == "response_received"), default=0))
                return copy.deepcopy(cached["clean"])
            remaining = self.deadline-time.monotonic()
            if remaining <= 0:
                raise RuntimeError("AI review deadline reached")
            previous = next((row for row in reversed(self.checkpoint.value["attempts"])
                if row["request_sha256"] == request_hash and row["status"] == "failed" and row["id"] not in handled), None)
            if previous is not None:
                handled.add(previous["id"])
                self.position = max(self.position, self.checkpoint.value["attempts"].index(previous)+1)
                info = SimpleNamespace(**{key: previous.get(key) for key in
                    ("reason", "kind", "retryable", "billing_unknown", "http_status", "retry_after")})
            else:
                token = self.checkpoint.claim(stage, unit, request_hash, self.profile, session,
                                             transport_retry=transport_retry)
                self.position = len(self.checkpoint.value["attempts"])
                try:
                    message, usage, model = self.api(self.profile, messages, tools, force_tool=force_tool, session_id=session,
                        max_output=MAX_OUTPUT, total_timeout=min(240, remaining), idle_timeout=min(45, remaining), stream=True)
                except Exception as exc:
                    info = error_info(exc)
                    self.checkpoint.failed(token, info)
                    handled.add(token)
                else:
                    clean = public_reply(message)
                    usage = public_usage(usage)
                    self.checkpoint.received(token, request_hash, clean, usage, model)
                    return clean
            if not info.retryable:
                raise RuntimeError("AI provider rejected the request")
            if self.checkpoint.value["transport_retries"] >= ai_checkpoint.MAX_TRANSPORT_RETRIES:
                raise RuntimeError("AI transport compensation budget exhausted")
            base = min(8, 2**self.checkpoint.value["transport_retries"])
            jitter = int(request_hash[:8], 16) % 250 / 1000
            retry_after = getattr(info, "retry_after", None)
            delay = min(30.0, max(base+jitter, retry_after if type(retry_after) in {int, float} else 0))
            if self.deadline-time.monotonic() <= delay:
                raise RuntimeError("AI deadline leaves no room for bounded retry backoff")
            self.checkpoint.value["attempts"][-1]["retry_delay_seconds"] = delay
            self.checkpoint.reserve_wait(delay)
            time.sleep(delay)
            if self.profile == "primary" and os.environ.get("AI_ALLOW_FALLBACK", "true").lower() == "true":
                self.profile = "backup"
            transport_retry = True


def draft_tool(remaining):
    import ai_review as review
    string = {"type": "string"}; refs = {"type": "array", "items": string}
    path = {"type": "object", "properties": {key: string for key in ("path", "status", "change", "impact", "verification")},
            "required": ["path", "status", "change", "impact", "verification", "evidence_ids"]}
    path["properties"]["evidence_ids"] = refs
    page = {"type": "object", "properties": {"page": string, "assessment": string, "evidence_ids": refs,
            "path_reviews": {"type": "array", "items": path}}, "required": ["page", "assessment", "evidence_ids", "path_reviews"]}
    finding = {"type": "object", "properties": {key: string for key in
        ("title", "page", "level", "analysis", "recommendation", "alternatives")},
        "required": ["title", "page", "level", "analysis", "recommendation", "alternatives", "evidence_ids"]}
    finding["properties"]["evidence_ids"] = refs
    return review.tool("finish_report", "Submit only this assigned page shard", {
        "overview": string, "pages": {"type": "array", "items": page},
        "findings": {"type": "array", "items": finding, "maxItems": remaining},
        "next_steps": {"type": "array", "items": string}}, ["overview", "pages", "findings", "next_steps"])


def deep_tools(no_apk):
    import ai_review as review
    string = {"type": "string"}; side = {"type": "string", "enum": ["target", "baseline"]}
    result = [review.tool("family_evidence", "Read a frozen family", {"family": string, "side": side}, ["family", "side"]),
        review.tool("protocol_evidence", "Read frozen protocol signatures/callers", {"protocol": string, "side": side}, ["protocol", "side"]),
        review.tool("module_source", "Read one exact pinned source file", {"path": string}, ["path"])]
    if not no_apk:
        result.append(review.tool("decompile_class", "Read a real APK class via JADX CLI", {"class_name": string, "side": side}, ["class_name", "side"]))
    return result


def review_tool():
    import ai_review as review
    string = {"type": "string"}; refs = {"type": "array", "items": string}
    revision = {"type": "object", "properties": {key: string for key in review.REVISION_FIELDS}}
    page = {"type": "object", "properties": {"page": string, "assessment": string, "evidence_ids": refs},
            "required": ["page", "assessment", "evidence_ids"]}
    finding = {"type": "object", "properties": {"finding_id": string, "disposition": string, "reason": string,
            "evidence_ids": refs, "revision": revision}, "required": ["finding_id", "disposition", "reason", "evidence_ids"]}
    return review.tool("finish_review", "Submit only assigned review pages/finding IDs", {
        "pages": {"type": "array", "items": page}, "findings": {"type": "array", "items": finding},
        "remaining_gaps": {"type": "array", "items": string}}, ["pages", "findings", "remaining_gaps"])


def collect(coordinator, stage, unit, messages, tools, evidence, validate, *, allow_deep=False, reserve_after=0):
    import ai_review as review
    offered = {row["function"]["name"] for row in tools}
    for _ in range(6 if allow_deep else 3):
        finish = "finish_report" if stage == "draft" else "finish_review"
        force = finish if (not allow_deep or evidence.calls >= evidence.limit
            or coordinator.available_slots(reserve_after) <= 1
            or unit == "d0" and evidence.calls >= review.MIN_DRAFT_DEEP_DIVES) else None
        message = coordinator.request(stage, unit, messages, tools, force)
        messages.append(message)
        accepted = None
        calls = message.get("tool_calls", [])
        if not calls:
            messages.append({"role": "user", "content": "上一次回复没有产生任何工具调用；请立即调用 "+finish+" 提交本单元结构化结果。"})
        for call in calls:
            name = call["function"]["name"]
            try:
                args = json.loads(call["function"]["arguments"])
                if name == finish:
                    if stage == "draft" and evidence.calls < review.MIN_DRAFT_DEEP_DIVES:
                        raise RuntimeError("Verify at least two hypotheses with the first-unit deep-dive tools")
                    accepted = validate(args)
                    result = {"accepted": True}
                elif name in offered and allow_deep:
                    result = evidence.run_tool(name, args)
                else:
                    raise RuntimeError("Tool is not allowed in this assigned unit")
            except Exception as exc:
                result = {"error": review.redact(str(exc)[:300]) if isinstance(exc, RuntimeError) else type(exc).__name__}
                # Errors are public protocol facts; never include source/result bodies.
                for attempt in reversed(coordinator.checkpoint.value["attempts"]):
                    if attempt.get("unit") == unit and attempt.get("status") == "response_received":
                        errors = attempt.setdefault("call_errors", [])
                        if len(errors) < 8:
                            errors.append({"tool": name, "error": result["error"]})
                        coordinator.checkpoint.save()
                        break
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "content": review.redact(json.dumps(result, ensure_ascii=False))})
        if accepted is not None:
            coordinator.checkpoint.save_unit(unit, accepted)
            return accepted
    raise RuntimeError("assigned AI unit did not complete within its logical request budget")


def run(root, *, api):
    import ai_review as review
    root = Path(root)
    summary = json.loads((root / "priority-summary.json").read_text(encoding="utf-8"))
    evidence = review.Evidence(root, summary)
    seed = seed_for(summary)
    source = summary.get("source_snapshot") or {}
    checkpoint = coordinator = None
    binding = fallback_ledger = None
    prior_requests = 0
    completed = draft = None
    started = time.monotonic()
    error = None; views = []; parts = []; review_plan = []; merged_counts = {}
    try:
        if source.get("binding") or source.get("schema", 0) >= 2:
            evidence.module_context()
        views = review.prefetch_evidence(evidence, summary)
        units = draft_units(summary["page_path_matrix"])
        binding = build_binding(root, summary, units)
        checkpoint = ai_checkpoint.Checkpoint(root, binding, resume_unknown=summary.get("ai_resume_unknown", False))
        prior_requests = len(checkpoint.value["attempts"])
        profile = "backup" if os.environ.get("AI_DEFAULT_PROFILE", "primary").lower() == "backup" else "primary"
        deadline = started+max(0, review.AI_DEADLINE_SECONDS-checkpoint.elapsed_base)
        coordinator = Coordinator(checkpoint, api, profile=profile, deadline=deadline)
        evidence.limit = review.MODEL_TOOLS-2
        findings = 0
        for index, pages in enumerate(units):
            matrix = {page: summary["page_path_matrix"][page] for page in pages}
            local_seed = unit_seed(seed, summary, pages)
            finding_budget = math.ceil((12-findings)/(len(units)-index))
            messages = [{"role": "system", "content": ai_prompts.SHARDED_DRAFT}, {"role": "user", "content": json.dumps({
                "seed": local_seed, "assigned_pages": pages, "finding_budget": finding_budget,
                "prefetch": [value for value in views if value["page"] in pages],
                "deep_evidence": review.bounded_journal([row for row in evidence.journal if row["tool"] != "page_evidence"]),
                "apk_access_disabled": summary.get("ai_no_apk_access") is True}, ensure_ascii=False)}]
            def validate(value, pages=pages, matrix=matrix, finding_budget=finding_budget, first=index == 0):
                value = review.validate_report(value, evidence.ids, pages, matrix)
                if len(value["findings"]) > finding_budget:
                    raise RuntimeError("assigned finding budget exceeded; reserve findings for the remaining pages")
                deep_ids = {row["id"] for row in evidence.journal if row["tool"] != "page_evidence"}
                if first and value["findings"] and not any(set(row["evidence_ids"]) & deep_ids for row in value["findings"]):
                    raise RuntimeError("At least one finding must cite deep-dive evidence")
                return value
            tools = deep_tools(summary.get("ai_no_apk_access") is True)+[draft_tool(finding_budget)]
            reserve = len(units)-index-1+max(1, math.ceil(len(summary["page_path_matrix"])/2))
            part = collect(coordinator, "draft", "d"+str(index), messages, tools, evidence, validate,
                           allow_deep=True, reserve_after=reserve)
            parts.append(part); findings += len(part["findings"])
        by_page = {row["page"]: row for part in parts for row in part["pages"]}
        next_steps, next_count = merge_items((step for part in parts for step in part["next_steps"]), 12)
        merged_counts.update(next_steps_unique=next_count, next_steps_merged=len(next_steps))
        draft = {"overview": "\n\n".join(part["overview"] for part in parts),
            "pages": [by_page[page] for page in summary["page_path_matrix"]],
            "findings": [row for part in parts for row in part["findings"]],
            "next_steps": next_steps}
        review.validate_report(draft, evidence.ids, list(summary["page_path_matrix"]), summary["page_path_matrix"])
        deep_ids = {row["id"] for row in evidence.journal if row["tool"] != "page_evidence"}
        if draft["findings"] and not any(set(row["evidence_ids"]) & deep_ids for row in draft["findings"]):
            raise RuntimeError("At least one finding in the full draft must cite deep-dive evidence")
        for index, finding in enumerate(draft["findings"], 1):
            finding["finding_id"] = f"F{index:03d}"
        (root / "ai-draft.json").write_text(review.redact(json.dumps(draft, ensure_ascii=False, indent=2)), encoding="utf-8")
        priorities = review.priority_pages(summary)
        review_start = len(evidence.journal)
        evidence.limit = review.MODEL_TOOLS
        fresh = {page: evidence.server_read("page_evidence", {"page": page})["evidence_id"]
                 for page in priorities if page in {"comment", "dynamic"}}
        review_plan = review_units(priorities, draft)
        records = []
        for index, assigned in enumerate(review_plan):
            assigned_findings = [row for row in draft["findings"] if row["finding_id"] in assigned["findings"]]
            included_pages = set(assigned["pages"]) | {row["page"] for row in assigned_findings}
            included_order = [page for page in summary["page_path_matrix"] if page in included_pages]
            local_draft = {**draft, "overview": draft["overview"][:1200],
                "pages": [row for row in draft["pages"] if row["page"] in included_pages], "findings": assigned_findings}
            messages = [{"role": "system", "content": ai_prompts.SHARDED_REVIEW}, {"role": "user", "content": json.dumps({
                "seed": unit_seed(seed, summary, included_order),
                "draft": local_draft, "priority_pages": assigned["pages"], "assigned_pages": assigned["pages"],
                "assigned_findings": assigned["findings"], "prefetch": [row for row in views if row["page"] in assigned["pages"]],
                "fresh_refresh": {page: identifier for page, identifier in fresh.items() if page in assigned["pages"]},
                "evidence": review.bounded_journal([row for row in evidence.journal if row["tool"] != "page_evidence"])}, ensure_ascii=False)}]
            validate = lambda value, local=local_draft, assigned=assigned: review.validate_review_record(
                value, local, evidence, assigned["pages"], review_start)
            record = collect(coordinator, "review", "r"+str(index), messages,
                deep_tools(summary.get("ai_no_apk_access") is True)+[review_tool()], evidence, validate,
                allow_deep=True, reserve_after=len(review_plan)-index-1)
            records.append(record)
        remaining_gaps, gap_count = merge_items((gap for record in records for gap in record["remaining_gaps"]), 20)
        merged_counts.update(remaining_gaps_unique=gap_count, remaining_gaps_merged=len(remaining_gaps))
        merged = {"pages": [row for record in records for row in record["pages"]],
            "findings": [row for record in records for row in record["findings"]],
            "remaining_gaps": remaining_gaps}
        review.validate_review_record(merged, draft, evidence, priorities, review_start)
        completed = review.assemble_report(draft, merged)
        review.validate_report(completed, evidence.ids, list(summary["page_path_matrix"]), summary["page_path_matrix"])
    except Exception as exc:
        error = type(exc).__name__+": "+review.redact(str(exc)[:200])
        if checkpoint is None and binding is not None:
            try:
                path = root / "ai-checkpoint.json"
                ai_checkpoint.regular(path)
                saved = ai_checkpoint.validate(json.loads(path.read_text(encoding="utf-8")))
                if saved["binding"] == binding:
                    fallback_ledger = saved
                    prior_requests = len(saved["attempts"])
            except (OSError, ValueError, RuntimeError):
                pass
    finally:
        if checkpoint is not None:
            try:
                checkpoint.record_elapsed(time.monotonic()-started)
            finally:
                checkpoint.close()
    ledger = checkpoint.value if checkpoint is not None else fallback_ledger
    attempts = ledger["attempts"] if ledger is not None else []
    outcome = {"schema": 2, "pipeline": "checkpoint-shards-v1", "prompt_version": ai_prompts.PROMPT_VERSION,
        "prompt_sha256": hashlib.sha256((ai_prompts.SHARDED_DRAFT+ai_prompts.SHARDED_REVIEW).encode()).hexdigest(),
        "status": "completed" if completed else "failed", "profile": coordinator.profile if coordinator else None,
        "source_snapshot": {key: value for key, value in source.items() if key != "source_records"},
        "static_evidence_run": summary.get("static_evidence_run"), "runtime_verified": False,
        "claim_scope": "ai_suggestions_over_static_evidence", "attempts": attempts,
        "limits": {"draft_logical_units": len(parts), "max_draft_logical_units": MAX_DRAFT_UNITS,
            "review_logical_units": len(review_plan), "hard_cap": 16, "transport_retry_allowance": 2,
            "model_read_tools": review.MODEL_TOOLS, "prefetched_pages": len(views),
            "deadline_seconds": review.AI_DEADLINE_SECONDS, "server_read_tool_calls": max(0, len(evidence.journal)-evidence.calls),
            "output_tokens_per_request": MAX_OUTPUT, "usd_cap_enforced": False},
        "report": completed, "review_status": "completed" if completed else "not_completed",
        "review": completed.get("review") if completed else None, "read_tool_calls": evidence.calls,
        "model_requests": len(attempts), "cached_responses_reused": coordinator.reused if coordinator else 0,
        "new_model_requests": max(0, len(attempts)-prior_requests),
        "merged_items": merged_counts,
        "usage_unknown": any(not row.get("usage") or row.get("billing_unknown") for row in attempts),
        **({"error": error} if error else {}),
        "checkpoint": {"binding_sha256": ledger["binding_sha256"], "completed_units": len(ledger["units"]),
                       "resume_blocked": fallback_ledger is not None} if ledger is not None else None}
    return review.save_outcome(root, summary, evidence, seed, outcome)
