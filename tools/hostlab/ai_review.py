"""Bounded API reviewer. Model tools are read-only and never receive credentials."""
import hashlib
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import hostlab
import process_control
import ai_prompts
import source_snapshot
import snapshot_transport

DRAFT_REQUESTS = 6
REVIEW_TOTAL = 8
HARD_REQUEST_CAP = 16
MAX_TRANSPORT_RETRIES = 2
MODEL_TOOLS = 6
MAX_OUTPUT = 65536
MAX_CONTEXT_CHARS = 640000
REVIEW_EXCERPT_CHARS = 2600
PREFETCH_VIEW_CHARS = 5000
AI_DEADLINE_SECONDS = 1800
DRAFT_SUBMIT_NUDGE_AT = 3
MIN_DRAFT_DEEP_DIVES = 2
REQUEST_TIMEOUT_SECONDS = 120


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def redact(text):
    for name in ("AI_API_KEY_PRIMARY", "AI_API_KEY_BACKUP", "HF_TOKEN", "GH_TOKEN"):
        value = os.environ.get(name)
        if value:
            text = text.replace(value, "[REDACTED]")
    return text


def call_api(profile, messages, tools, force_tool=None, session_id=None, **options):
    """Retain the mockable public call boundary while transport owns streaming/timeouts."""
    import ai_transport
    return ai_transport.call_api(profile, messages, tools, force_tool, session_id, **options)


def tool(name, description, properties, required):
    return {"type": "function", "function": {"name": name, "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required, "additionalProperties": False}}}


def _diff_names(expected, got):
    missing=sorted(set(expected)-set(got))
    extra=sorted(set(got)-set(expected))
    parts=[]
    if missing: parts.append("missing="+",".join(missing))
    if extra: parts.append("unexpected="+",".join(extra))
    return "; ".join(parts) if parts else "duplicates present"


def validate_report(value, ids, pages, matrix=None):
    if not isinstance(value, dict) or not isinstance(value.get("overview"), str):
        raise RuntimeError("Report requires overview")
    assessments = value.get("pages", [])
    got_pages=[p.get("page") for p in assessments if isinstance(p,dict)]
    if len(assessments) != len(pages) or set(got_pages) != set(pages):
        raise RuntimeError("Assess every registered page exactly once ("+_diff_names(pages,got_pages)+
            "); submit exactly these page names: "+",".join(pages))
    findings = value.get("findings", [])
    if not isinstance(findings, list) or len(findings) > 12:
        raise RuntimeError("Findings exceed bound")
    if not isinstance(value.get("next_steps"),list) or len(value["next_steps"])>12 or not all(isinstance(s,str) for s in value["next_steps"]):
        raise RuntimeError("Bound next_steps to at most twelve strings")
    for item in assessments + findings:
        refs = item.get("evidence_ids", [])
        bad=[ref for ref in refs if ref not in ids]
        if not refs or bad:
            raise RuntimeError("Only cite actual E000/E001 evidence IDs (invalid refs: "+
                (",".join(str(r) for r in bad) if bad else "none provided")+")")
    for item in assessments:
        if not isinstance(item.get("assessment"),str):
            raise RuntimeError("Page assessment must be text")
        if matrix is not None:
            checks=item.get("path_reviews",[])
            expected=set(matrix[item["page"]].get("paths",{}))
            got_paths=[c.get("path") for c in checks if isinstance(c,dict)]
            if len(checks)!=len(expected) or set(got_paths)!=expected:
                raise RuntimeError("Assess each registered path of page "+item["page"]+" exactly once ("+
                    _diff_names(expected,got_paths)+"); expected paths: "+",".join(sorted(expected)))
            for check in checks:
                if not all(isinstance(check.get(k),str) and check[k].strip() for k in ("status","change","impact","verification")):
                    raise RuntimeError("Path "+str(check.get("path"))+" needs status, change, impact and verification")
                if check["status"]!=matrix[item["page"]]["paths"][check["path"]]["evidence"]:
                    raise RuntimeError("Path "+check["path"]+" status must be exactly '"+
                        matrix[item["page"]]["paths"][check["path"]]["evidence"]+"' (copy it from prefetch)")
                if not check.get("evidence_ids") or any(ref not in ids for ref in check["evidence_ids"]):
                    raise RuntimeError("Path "+str(check.get("path"))+" references unknown evidence")
    for item in findings:
        if item.get("level") not in {"candidate", "static_evidence", "needs_runtime"}:
            raise RuntimeError("Unsupported claim level (use candidate/static_evidence/needs_runtime)")
        if item.get("page") not in pages or not all(isinstance(item.get(k),str) for k in ("title","analysis","recommendation")):
            raise RuntimeError("Finding requires a registered page and text fields (page='"+str(item.get("page"))+
                "' not in "+",".join(pages)+")")
        if matrix is not None and (not isinstance(item.get("alternatives"),str) or not item["alternatives"].strip()):
            raise RuntimeError("Finding must discuss alternative explanations")
    size=len(json.dumps(value, ensure_ascii=False))
    if size > 100000:
        raise RuntimeError("Report exceeds output bound ("+str(size)+" chars); shorten assessments, not coverage")
    return value


def priority_pages(summary):
    changed={c.get("family") for c in summary.get("changes",[])}
    return [name for name,page in summary["page_path_matrix"].items()
            if name in {"comment","dynamic"} or len(page.get("paths",{}))>1 or changed.intersection(page.get("paths",{}))]


def validate_review_record(review,draft,evidence,priorities,review_start):
    if not isinstance(review,dict):
        raise RuntimeError("Independent review record is required")
    rows=review.get("pages",[])
    got_pages=[r.get("page") for r in rows if isinstance(r,dict)]
    if len(rows)!=len(priorities) or set(got_pages)!=set(priorities):
        raise RuntimeError("Review every priority page exactly once ("+_diff_names(priorities,got_pages)+
            "); submit exactly these pages: "+",".join(priorities))
    findings=review.get("findings",[])
    expected={r["finding_id"] for r in draft["findings"]}
    got_ids=[r.get("finding_id") for r in findings if isinstance(r,dict)]
    if len(findings)!=len(expected) or set(got_ids)!=expected:
        raise RuntimeError("Review every draft finding exactly once ("+_diff_names(expected,got_ids)+
            "); submit exactly these finding_ids: "+",".join(sorted(expected)))
    for row in rows+findings:
        field="assessment" if "page" in row else "reason"
        if not isinstance(row.get(field),str) or not row[field].strip():
            raise RuntimeError("Review requires an explanation ("+field+")")
        bad=[ref for ref in row.get("evidence_ids",[]) if ref not in evidence.ids]
        if not row.get("evidence_ids") or bad:
            raise RuntimeError("Review references unknown evidence (invalid refs: "+
                (",".join(str(r) for r in bad) if bad else "none provided")+
                "); use ids from prefetch/fresh_refresh or your own tool results")
    for row in findings:
        if row.get("disposition") not in {"retained","revised","rejected","needs_more_evidence"}:
            raise RuntimeError("Invalid review disposition for "+str(row.get("finding_id"))+
                " (use retained/revised/rejected/needs_more_evidence)")
        revision=row.get("revision")
        if row.get("disposition")=="revised":
            message=invalid_revision(revision)
            if message:
                raise RuntimeError(message)
        elif revision is not None:
            raise RuntimeError("Revision patch is only allowed with disposition=revised (finding "+
                str(row.get("finding_id"))+" has revision but disposition="+str(row.get("disposition"))+")")
    gaps=review.get("remaining_gaps")
    if not isinstance(gaps,list) or len(gaps)>20 or not all(isinstance(g,str) for g in gaps):
        raise RuntimeError("Review must record bounded remaining gaps")
    fresh=evidence.journal[review_start:]
    for page in set(priorities)&{"comment","dynamic"}:
        reads=[r for r in fresh if r["tool"]=="page_evidence" and r["args"].get("page")==page]
        page_row=next(r for r in rows if r["page"]==page)
        if not reads or not any(r["id"] in page_row["evidence_ids"] for r in reads):
            raise RuntimeError("Reviewer must reread and cite priority page evidence: "+page)
    review["status"]="completed"
    return review


class Evidence:
    def __init__(self, root, summary):
        self.root, self.summary = root, summary
        self.data = {}
        self.calls = 0
        self.journal = []
        self.ids = {"E000"}
        self.limit = MODEL_TOOLS
        self.source_context = None

    def module_context(self):
        if self.source_context is not None:
            return self.source_context
        metadata = self.summary.get("source_snapshot") or {}
        binding = metadata.get("binding")
        if binding:
            context = snapshot_transport.load_pinned(binding)
            source_snapshot.validate(context, expected_sha256=binding["snapshot_sha256"])
            verified_metadata = source_snapshot.public_context(context)
            for key in ("schema", "selection_version", "repository_head", "source_tree_sha256", "captured_at",
                        "working_tree_dirty", "source_records"):
                if metadata.get(key) != verified_metadata.get(key):
                    raise RuntimeError("Source snapshot metadata differs from its pinned payload")
        else:
            if metadata.get("schema", 0) >= 2:
                raise RuntimeError("Verified source snapshot binding is missing")
            digest = metadata.get("legacy_cache_sha256", "")
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise RuntimeError("Legacy source is unavailable; historical metadata is not current source")
            cache = hostlab.STATE / "source-snapshots" / ("legacy-" + digest) / "context.json"
            if not cache.is_file():
                raise RuntimeError("Legacy source cache is unavailable; no latest source fallback")
            raw = cache.read_bytes()
            if hashlib.sha256(raw).hexdigest() != digest:
                raise RuntimeError("Legacy source cache digest differs")
            context = json.loads(raw)
        self.source_context = context
        return context

    def dataset(self, side):
        if side not in {"target", "baseline"}:
            raise RuntimeError("Invalid side")
        if side not in self.data:
            self.data[side] = json.loads((self.root / ("priority-" + side + ".json")).read_text(encoding="utf-8"))
        return self.data[side]

    def server_read(self, name, args):
        """Server-side read that never consumes the model tool budget."""
        saved_calls = self.calls
        saved_limit = self.limit
        self.limit = saved_calls + 1
        try:
            return self.run_tool(name, args)
        finally:
            self.calls = saved_calls
            self.limit = saved_limit

    def run_tool(self, name, args):
        if self.calls >= self.limit:
            raise RuntimeError("Read-only tool budget exhausted")
        self.calls += 1
        side = args.get("side", "target")
        if name == "page_evidence":
            page=args["page"]
            matrix=self.summary["page_path_matrix"]
            if page not in matrix:
                raise RuntimeError("Select a registered page")
            families=list(matrix[page]["paths"])
            protocols=list(matrix[page].get("protocols",{}))
            result={"page":page,"sides":{},"limits":"Two class samples per family; four caller samples per protocol; runtime unknown"}
            for which in ("target","baseline"):
                if which=="baseline" and not self.summary.get("baseline"):
                    result["sides"][which]={"missing":True}
                    continue
                data=self.dataset(which)
                selected={}
                for family in families:
                    rows=[r for r in data["class_records"] if r["family"]==family]
                    selected[family]={"summary":data["families"].get(family),"samples":[
                        {"class":r["class"],"fields":r.get("fields",[])[:4],"methods":r.get("methods",[])[:6]} for r in rows[:2]]}
                calls={p:{"summary":{k:v for k,v in (data["protocol_paths"].get(p) or {}).items() if k!="signatures"},
                    "caller_samples":[e for e in data["invoke_edges"] if e[5]==p and e[2]!=e[6]][:4]} for p in protocols}
                result["sides"][which]={"sample":data["sample"],"families":selected,"protocols":calls}
        elif name == "family_evidence":
            data = self.dataset(side)
            family = args["family"]
            rows = [r for r in data["class_records"] if r["family"] == family]
            samples=[]
            for row in rows[:5]:
                samples.append({**{k:v for k,v in row.items() if k not in {"fields","methods"}},
                    "fields":row.get("fields",[])[:8],"methods":row.get("methods",[])[:10],
                    "total_fields":len(row.get("fields",[])),"total_methods":len(row.get("methods",[]))})
            result = {"family": family, "side": side, "total_classes": len(rows),
                "summary": data["families"].get(family), "class_samples": samples,
                "sample_limit": 5, "full_evidence_file": "priority-" + side + ".json"}
        elif name == "protocol_evidence":
            data = self.dataset(side)
            protocol = args["protocol"]
            calls = [e for e in data["invoke_edges"] if e[5] == protocol and e[2] != e[6]]
            protocol_summary=dict(data["protocol_paths"].get(protocol) or {})
            if "signatures" in protocol_summary:
                protocol_summary["signatures"]=protocol_summary["signatures"][:12]
            result = {"protocol": protocol, "side": side, "summary": protocol_summary,
                      "total_callers": len(calls), "caller_samples": calls[:12], "sample_limit": 12}
        elif name == "module_source":
            context = self.module_context()
            metadata = self.summary.get("source_snapshot") or {}
            records = context.get("source_records", [])
            matches = [r for r in records if r["path"] == args["path"]]
            if len(matches) != 1:
                raise RuntimeError("Select an exact source path from E000")
            r = matches[0]
            result = {"path": r["path"], "sha256": r["sha256"], "source": r["source"][:9000],
                      "truncated": len(r["source"]) > 9000, "working_tree_dirty": context.get("working_tree_dirty"),
                      "source_snapshot": {k:v for k,v in metadata.items() if k != "source_records"},
                      "source_status": "verified_pinned" if metadata.get("binding") else "legacy_not_current"}
        elif name == "decompile_class":
            if self.summary.get("ai_no_apk_access") is True:
                raise RuntimeError("APK access is disabled for this frozen-evidence review")
            data = self.dataset(side)
            class_name = args["class_name"]
            descriptor = "L" + class_name.replace(".", "/") + ";"
            allowed = {r["class"] for r in data["class_records"]}
            allowed.update(e[2] for e in data["invoke_edges"])
            allowed.update(e[6] for e in data["invoke_edges"])
            if descriptor not in allowed or not re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+", class_name):
                raise RuntimeError("Class must be a real member in the frozen evidence")
            sample = data["sample"]
            folder = hostlab.STATE / "reports" / str(sample["version_code"]) / sample["sha256"][:16]
            previous = set(folder.glob("*/class.java"))
            command = [sys.executable, str(Path(__file__).with_name("hostlab.py")), "decompile",
                       "--version-code", str(sample["version_code"]), "--sha256", sample["sha256"],
                       "--revision", sample["revision"], "--class", class_name, "--timeout", "120"]
            rc = process_control.run(command, stdout=subprocess.DEVNULL, timeout=150)
            sources = set(folder.glob("*/class.java")) - previous
            if rc or len(sources) != 1:
                raise RuntimeError("Class decompile failed or timed out")
            source = next(iter(sources))
            text = source.read_text(encoding="utf-8", errors="replace")
            result = {"class": class_name, "side": side, "source_sha256": hostlab.digest(source),
                      "source": text[:10000], "truncated": len(text) > 10000}
        else:
            raise RuntimeError("Tool is not allowed")
        if name=="page_evidence" and len(json.dumps(result,ensure_ascii=False))>13000:
            for data in result["sides"].values():
                for family in data.get("families",{}).values():
                    family.pop("samples",None)
            result["limits"]+="; class samples omitted to retain both sides within size bound"
        eid = "E" + str(len(self.journal) + 1).zfill(3)
        result["evidence_id"] = eid
        text = redact(json.dumps(result, ensure_ascii=False))
        if name == "module_source":
            # Escaped source can exceed the JSON bound even below the character limit.
            # Trim only the source field so the immutable identity always survives.
            while len(text) > 14000 and result["source"]:
                result["source"] = result["source"][:len(result["source"]) // 2]
                result["truncated"] = True
                text = redact(json.dumps(result, ensure_ascii=False))
            if len(text) > 14000:
                raise RuntimeError("Source metadata exceeds the evidence bound")
        if len(text) > 14000:
            result = {"evidence_id": eid, "truncated": True, "total_characters": len(text), "excerpt": text[:13000]}
        self.ids.add(eid)
        self.journal.append({"id": eid, "tool": name, "args": args, "result": result})
        return result

    def public_journal(self):
        rows = copy.deepcopy(self.journal)
        for row in rows:
            if row["tool"] == "module_source":
                row["result"].pop("source", None)
                row["result"].pop("excerpt", None)
        return rows


def transport_retry_credit(attempts):
    """Extra request slots for dropped connections, bounded by MAX_TRANSPORT_RETRIES."""
    failures=sum(1 for a in attempts if a.get("status")=="failed" and str(a.get("reason","")).startswith("API failure:"))
    return min(failures,MAX_TRANSPORT_RETRIES)


def prefetch_view(result, limit=PREFETCH_VIEW_CHARS):
    """Bounded per-page view for prompts; the full result stays in the journal."""
    def build(with_callers):
        view={"page":result.get("page"),"evidence_id":result.get("evidence_id"),
              "limits":result.get("limits"),"sides":{}}
        for which,data in (result.get("sides") or {}).items():
            if data.get("missing"):
                view["sides"][which]={"missing":True}
                continue
            view["sides"][which]={
                "sample":data.get("sample"),
                "families":{k:{"summary":v.get("summary")} for k,v in (data.get("families") or {}).items()},
                "protocols":{k:{"summary":v.get("summary"),
                    **({"callers":(v.get("caller_samples") or [])[:2]} if with_callers else {})}
                    for k,v in (data.get("protocols") or {}).items()}}
        return view
    view=build(True)
    if len(json.dumps(view,ensure_ascii=False))>limit:
        view=build(False)
    text=json.dumps(view,ensure_ascii=False)
    if len(text)>limit:
        view={"page":result.get("page"),"evidence_id":result.get("evidence_id"),
              "truncated":True,"excerpt":text[:limit]}
    return view


def prefetch_evidence(evidence,summary):
    """Deterministic server-side page reads; zero API cost and no model tool budget."""
    views=[]
    for page in summary["page_path_matrix"]:
        views.append(prefetch_view(evidence.server_read("page_evidence",{"page":page})))
    return views


REVISION_FIELDS=("title","analysis","recommendation","alternatives","level")
CLAIM_LEVELS={"candidate","static_evidence","needs_runtime"}


def invalid_revision(revision):
    """Return a rejection message when a revision patch fails value checks, else None."""
    if not isinstance(revision,dict) or not revision:
        return "revised disposition requires a non-empty revision patch"
    for key in revision:
        if key not in REVISION_FIELDS:
            return "Revision patch has unsupported fields: "+str(key)
    for key,value in revision.items():
        if key=="level":
            if not isinstance(value,str) or value not in CLAIM_LEVELS:
                return "Revision level must be one of candidate/static_evidence/needs_runtime"
        elif not isinstance(value,str) or not value.strip():
            return "Revision field must be non-empty text: "+key
    return None


def assemble_report(draft,review):
    """Deterministic assembly: draft pages plus review dispositions become the final report."""
    if not isinstance(review,dict):
        raise RuntimeError("Review record must be an object")
    rows=review.get("findings")
    if not isinstance(rows,list):
        raise RuntimeError("Review record requires a findings list")
    by_id={}
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get("finding_id"),str):
            raise RuntimeError("Each review finding requires a finding_id")
        if row["finding_id"] in by_id:
            raise RuntimeError("Duplicate review finding_id: "+row["finding_id"])
        by_id[row["finding_id"]]=row
    draft_ids={f.get("finding_id") for f in draft["findings"]}
    extra=[key for key in by_id if key not in draft_ids]
    if extra:
        raise RuntimeError("Review references findings absent from the draft: "+",".join(sorted(extra)))
    findings=[]
    for item in draft["findings"]:
        row=by_id.get(item["finding_id"])
        if row is None:
            raise RuntimeError("Review is missing draft finding "+item["finding_id"])
        disposition=row.get("disposition")
        if disposition=="rejected":
            continue
        if disposition not in {"retained","revised","needs_more_evidence"}:
            raise RuntimeError("Invalid review disposition for "+item["finding_id"])
        merged=copy.deepcopy(item)
        revision=row.get("revision")
        if disposition=="revised":
            message=invalid_revision(revision)
            if message:
                raise RuntimeError(message)
            merged.update({k:revision[k] for k in REVISION_FIELDS if k in revision})
            refs=row.get("evidence_ids")
            if not isinstance(refs,list) or not refs or not all(isinstance(ref,str) and ref for ref in refs):
                raise RuntimeError("Revised finding requires non-empty validated evidence_ids")
            # The validated review justifies the revised text; stale draft
            # references may be exactly the cross-page error it corrected.
            merged["evidence_ids"]=copy.deepcopy(refs)
        elif revision is not None:
            raise RuntimeError("Revision patch is only allowed with disposition=revised")
        if disposition=="needs_more_evidence" and merged.get("level")=="static_evidence":
            merged["level"]="needs_runtime"
        findings.append(merged)
    assembled=copy.deepcopy(draft)
    assembled["findings"]=findings
    assembled["review"]=copy.deepcopy(review)
    return assembled


def bounded_journal(journal):
    """Bound the review payload; full results stay reachable by re-reading with the same tools."""
    rows=[]
    for row in journal:
        result=row.get("result")
        text=json.dumps(result,ensure_ascii=False)
        if len(text)>REVIEW_EXCERPT_CHARS:
            result={"excerpt":text[:REVIEW_EXCERPT_CHARS],"truncated":True,
                    "note":"full result omitted to bound context; re-read with the same tool arguments"}
        rows.append({"id":row.get("id"),"tool":row.get("tool"),"args":row.get("args"),"result":result})
    return rows


def collect_report(messages,tools,evidence,summary,attempts,profile,request_limit,draft=None,review_start=None,deadline=None):
    if review_start is None:
        review_start=len(evidence.journal)
    # One stable session ID per conversation; OpenCode-compatible gateways use it for routing
    # and prompt caching, and reject session-less requests with MissingSessionID.
    session_id="hostlab-"+os.urandom(12).hex()
    nudged=False
    offered={t["function"]["name"] for t in tools}
    attempts_before=len(attempts)
    def credit():
        failures=transport_retry_credit(attempts[attempts_before:])
        return min(failures,max(0,HARD_REQUEST_CAP-1-len(attempts)))
    while len(attempts)<HARD_REQUEST_CAP and len(attempts)-attempts_before<request_limit+credit():
        size=len(json.dumps(messages,ensure_ascii=False))
        if deadline is not None and time.monotonic()>deadline:
            print(json.dumps({"event":"deadline_reached","attempts":len(attempts),"deadline_seconds":AI_DEADLINE_SECONDS}))
            break
        if size>MAX_CONTEXT_CHARS:
            print(json.dumps({"event":"context_limit_reached","chars":size,"limit":MAX_CONTEXT_CHARS,"attempts":len(attempts)}))
            break
        try:
            remaining=request_limit+credit()-(len(attempts)-attempts_before)
            # Force the last two slots of each phase so a rejected submission can be corrected.
            force=remaining<=2
            if draft is None and remaining<=DRAFT_SUBMIT_NUDGE_AT and not nudged:
                messages.append({"role":"user","content":
                    "预算提醒：剩余请求有限。请立即调用 finish_report 提交完整报告"
                    "（覆盖全部登记页面与每条登记路径）；继续取证而不提交会导致本次分析失败。"
                    "可用一次回复并行调用多个深挖工具，但优先保证提交。"})
                nudged=True
            force_tool=("finish_review" if draft is not None else "finish_report") if force else None
            message,usage,model=call_api(profile,messages,tools,force_tool,session_id=session_id)
            attempts.append({"stage":"review" if draft else "draft","profile":profile,"model":model,"usage":usage,"status":"response_received"})
        except RuntimeError as exc:
            reason=str(exc)
            attempts.append({"stage":"review" if draft else "draft","profile":profile,"status":"failed","reason":reason,"billing_unknown":True})
            if profile=="primary" and os.environ.get("AI_ALLOW_FALLBACK","true").lower()=="true":
                profile="backup"
                continue
            retryable=reason.startswith("API failure:") or any(code in reason for code in ("HTTP 429","HTTP 500","HTTP 502","HTTP 503","HTTP 504"))
            if retryable and len(attempts)<HARD_REQUEST_CAP and len(attempts)-attempts_before<request_limit+credit():
                time.sleep(2)
                continue
            break
        messages.append(message)
        calls=message.get("tool_calls",[])
        if not calls:
            usage=attempts[-1].get("usage") or {}
            completion=usage.get("completion_tokens")
            # Reasoning-heavy models can burn the entire output budget on hidden reasoning
            # (completion == cap) and return no content and no tool call. Flag it so the
            # loop issues a short resubmission instruction instead of the generic nudge.
            if isinstance(completion,int) and completion>=MAX_OUTPUT:
                attempts[-1]["empty_completion"]=True
                messages.append({"role":"user","content":
                    "上一次回复没有产生任何工具调用（输出预算被推理耗尽）。"
                    "请立即直接调用 finish_report（复核阶段为 finish_review），不要继续推理或取证。"})
            else:
                messages.append({"role":"user","content":"先用证据工具调查，再调用 finish_report 提交结构化报告。"})
            continue
        completed=None
        for call in calls:
            tool_name=None
            try:
                tool_name=call["function"]["name"]
                args=json.loads(call["function"]["arguments"])
                if tool_name=="finish_report":
                    if draft is not None:
                        raise RuntimeError("Submit the review via finish_review in this session")
                    if evidence.calls<MIN_DRAFT_DEEP_DIVES:
                        raise RuntimeError("Verify at least "+str(MIN_DRAFT_DEEP_DIVES)+
                            " hypotheses with deep-dive tools (family_evidence/protocol_evidence/module_source/decompile_class) before submitting the draft")
                    candidate=validate_report(args,evidence.ids,list(summary["page_path_matrix"]),summary["page_path_matrix"])
                    deep_ids={r["id"] for r in evidence.journal if r["tool"]!="page_evidence"}
                    if candidate.get("findings") and not any(set(f.get("evidence_ids",[]))&deep_ids for f in candidate["findings"]):
                        raise RuntimeError("At least one finding must cite deep-dive evidence (not only prefetched page evidence)")
                    completed=candidate
                    result={"accepted":True}
                elif tool_name=="finish_review":
                    if draft is None:
                        raise RuntimeError("finish_review is only available in the review session")
                    candidate=validate_review_record(args,draft,evidence,priority_pages(summary),review_start)
                    completed=candidate
                    result={"accepted":True}
                elif tool_name in offered:
                    result=evidence.run_tool(tool_name,args)
                else:
                    raise RuntimeError("Tool is not allowed: "+str(tool_name))
            except Exception as exc:
                if isinstance(exc,json.JSONDecodeError):
                    result={"error":"tool arguments were not valid JSON (most likely truncated by the output limit); resubmit this call with more concise arguments"}
                else:
                    result={"error":str(exc)[:300] if type(exc) is RuntimeError else type(exc).__name__}
                errors=attempts[-1].setdefault("call_errors",[])
                if len(errors)<8:
                    errors.append({"tool":tool_name or "invalid_call","error":result["error"]})
            messages.append({"role":"tool","tool_call_id":call["id"],"content":redact(json.dumps(result,ensure_ascii=False))})
        if completed:
            return completed,profile
    return None,profile


def _run(root):
    summary_path = root / "priority-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    evidence = Evidence(root, summary)
    source_metadata = summary.get("source_snapshot") or {}
    if source_metadata.get("binding") or source_metadata.get("schema", 0) >= 2:
        # Source corruption must stop the review before the first model request.
        evidence.module_context()
    attempts=[]
    seed = {"evidence_id": "E000", "sample": summary["sample"], "baseline": summary.get("baseline"),
        "pages": copy.deepcopy(summary["page_path_matrix"]), "changes": summary["changes"],
        "resource_change_counts": {k:len(v) for k,v in (summary.get("resource_changes") or {}).items() if isinstance(v,list)},
        "limitations": summary["limitations"], "source_files": [r["path"] for r in (summary.get("source_snapshot") or {}).get("source_records", [])],
        "source_dirty": (summary.get("source_snapshot") or {}).get("working_tree_dirty"),
        "source_snapshot": {k:v for k,v in source_metadata.items() if k != "source_records"},
        "unregistered_protocols": summary.get("unregistered_protocols", [])}
    # Keep detailed signatures in tools; initial evidence covers all registered pages.
    for page in seed["pages"].values():
        page["protocols"] = {k:{a:b for a,b in v.items() if a != "signatures"} for k,v in page.get("protocols", {}).items()}
    seed["changes"] = [{k:v for k,v in c.items() if k not in {"before","after"}} for c in seed["changes"]]
    prefetch_entries=0
    try:
        views=prefetch_evidence(evidence,summary)
        prefetch_entries=len(evidence.journal)
    except Exception as exc:
        attempts.append({"stage":"prefetch","status":"failed","reason":type(exc).__name__+": "+str(exc)[:200]})
        raise RuntimeError("Evidence prefetch failed; analysis aborted before any API request") from None
    messages = [{"role":"system", "content":ai_prompts.DRAFT},
                {"role":"user", "content":json.dumps({"seed":seed,"prefetch":views},ensure_ascii=False)}]
    side = {"type":"string","enum":["target","baseline"]}
    string = {"type":"string"}
    deep_tools=[tool("family_evidence","Read family structures, counts and bounded class samples",{"family":string,"side":side},["family","side"]),
             tool("protocol_evidence","Read exact signatures and actual static invoke callers",{"protocol":string,"side":side},["protocol","side"]),
             tool("module_source","Read a frozen production source file, never filesystem paths",{"path":string},["path"]),
             tool("decompile_class","Read pseudo-Java of a real frozen APK class",{"class_name":string,"side":side},["class_name","side"])]
    tools = deep_tools + [tool("finish_report","Submit Chinese review with evidence citations; no adaptation acceptance",{
                 "overview":string,"pages":{"type":"array","items":{"type":"object","properties":{"page":string,"assessment":string,"evidence_ids":{"type":"array","items":string}},"required":["page","assessment","evidence_ids"]}},
                 "findings":{"type":"array","items":{"type":"object","properties":{"title":string,"page":string,"level":{"type":"string","enum":["candidate","static_evidence","needs_runtime"]},"analysis":string,"recommendation":string,"evidence_ids":{"type":"array","items":string}},"required":["title","page","level","analysis","recommendation","evidence_ids"]}},
                 "next_steps":{"type":"array","items":string}},["overview","pages","findings","next_steps"])]
    finish=tools[-1]["function"]["parameters"]
    path_schema={"type":"object","properties":{k:string for k in ("path","status","change","impact","verification")},
        "required":["path","status","change","impact","verification","evidence_ids"]}
    path_schema["properties"]["evidence_ids"]={"type":"array","items":string}
    page_schema=finish["properties"]["pages"]["items"]
    page_schema["properties"]["path_reviews"]={"type":"array","items":path_schema}
    page_schema["required"].append("path_reviews")
    finding_schema=finish["properties"]["findings"]["items"]
    finding_schema["properties"]["alternatives"]=string
    finding_schema["required"].append("alternatives")
    profile="backup" if os.environ.get("AI_DEFAULT_PROFILE","primary").lower()=="backup" else "primary"
    deadline=time.monotonic()+AI_DEADLINE_SECONDS
    # Reserve two model tool calls for the review session.
    evidence.limit=MODEL_TOOLS-2
    draft,profile=collect_report(messages,tools,evidence,summary,attempts,profile,DRAFT_REQUESTS,deadline=deadline)
    completed=None
    if draft:
        for index,finding in enumerate(draft["findings"],1):
            finding["finding_id"]=f"F{index:03d}"
        (root/"ai-draft.json").write_text(redact(json.dumps(draft,ensure_ascii=False,indent=2)),encoding="utf-8")
        evidence.limit=MODEL_TOOLS
        priorities=priority_pages(summary)
        refresh_pages=[p for p in priorities if p in {"comment","dynamic"}]
        # The fresh reread is part of the review window, so its ids satisfy the
        # reviewer-must-reread check in validate_review_record.
        review_start=len(evidence.journal)
        review=None
        try:
            fresh={}
            for page in refresh_pages:
                fresh[page]=evidence.server_read("page_evidence",{"page":page})["evidence_id"]
            refs={"type":"array","items":string}
            revision={"type":"object","properties":{
                "title":string,"analysis":string,"recommendation":string,"alternatives":string,
                "level":{"type":"string","enum":["candidate","static_evidence","needs_runtime"]}}}
            review_tools=deep_tools+[tool("finish_review","Submit the review record only; the final report is assembled server-side",{
                "pages":{"type":"array","items":{"type":"object","properties":{"page":string,"assessment":string,"evidence_ids":refs},"required":["page","assessment","evidence_ids"]}},
                "findings":{"type":"array","items":{"type":"object","properties":{"finding_id":string,"disposition":{"type":"string","enum":["retained","revised","rejected","needs_more_evidence"]},"reason":string,"evidence_ids":refs,"revision":revision},"required":["finding_id","disposition","reason","evidence_ids"]}},
                "remaining_gaps":{"type":"array","items":string}},["pages","findings","remaining_gaps"])]
            review_messages=[{"role":"system","content":ai_prompts.REVIEW},
                {"role":"user","content":json.dumps({"seed":seed,"draft":draft,"priority_pages":priorities,"prefetch":views,
                    "fresh_refresh":fresh,"evidence":bounded_journal(evidence.journal[prefetch_entries:])},ensure_ascii=False)}]
            review,profile=collect_report(review_messages,review_tools,evidence,summary,attempts,profile,REVIEW_TOTAL,
                draft=draft,review_start=review_start,deadline=deadline)
        except Exception as exc:
            attempts.append({"stage":"review","profile":profile,"status":"failed",
                             "reason":type(exc).__name__+": "+str(exc)[:200]})
            review=None
        if review:
            try:
                completed=assemble_report(draft,review)
                validate_report(completed,evidence.ids,list(summary["page_path_matrix"]),summary["page_path_matrix"])
            except Exception as exc:
                attempts.append({"stage":"assembly","profile":profile,"status":"failed",
                                 "reason":type(exc).__name__+": "+str(exc)[:200]})
                completed=None
    (root/"ai-review.json").write_text(redact(json.dumps((completed or {}).get("review",{"status":"not_completed"}),ensure_ascii=False,indent=2)),encoding="utf-8")
    outcome = {"schema":2,"prompt_version":ai_prompts.PROMPT_VERSION,
               "prompt_sha256":hashlib.sha256((ai_prompts.DRAFT+ai_prompts.REVIEW).encode()).hexdigest(),
               "status":"completed" if completed else "failed", "profile":profile,
               "source_snapshot": {k:v for k,v in source_metadata.items() if k != "source_records"},
               "static_evidence_run": summary.get("static_evidence_run"),
               "runtime_verified":False,"claim_scope":"ai_suggestions_over_static_evidence", "attempts":attempts,
               "limits":{"draft_requests":DRAFT_REQUESTS,"review_requests":REVIEW_TOTAL,"hard_cap":HARD_REQUEST_CAP,
                   "transport_retry_allowance":MAX_TRANSPORT_RETRIES,"model_read_tools":MODEL_TOOLS,
                   "prefetched_pages":len(views),"deadline_seconds":AI_DEADLINE_SECONDS,
                   "server_read_tool_calls":max(0,len(evidence.journal)-evidence.calls),
                   "output_tokens_per_request":MAX_OUTPUT,"usd_cap_enforced":False},
               "report":completed,"review_status":"completed" if completed else "not_completed","review":completed.get("review") if completed else None,"read_tool_calls":evidence.calls}
    return save_outcome(root, summary, evidence, seed, outcome)


def save_outcome(root, summary, evidence, seed, outcome):
    summary_path = root / "priority-summary.json"
    completed = outcome.get("report")
    profile, attempts = outcome.get("profile"), outcome.get("attempts", [])
    report_path = root / "priority-report.md"
    if report_path.is_file():
        static = report_path.read_text(encoding="utf-8")
        for marker in ("\n# AI 适配分析", "\n# AI 分析未完成"):
            static = static.split(marker, 1)[0]
        report_path.write_text(static, encoding="utf-8")
    (root/"ai-review.json").write_text(redact(json.dumps((completed or {}).get("review", {"status":"not_completed"}), ensure_ascii=False, indent=2)), encoding="utf-8")
    (root/"ai-analysis.json").write_text(redact(json.dumps(outcome,ensure_ascii=False,indent=2)),encoding="utf-8")
    (root/"ai-evidence.json").write_text(redact(json.dumps({"E000":seed,"tools":evidence.public_journal()},ensure_ascii=False,indent=2)),encoding="utf-8")
    summary["ai_status"] = outcome["status"]
    summary["ai_review"] = outcome
    hostlab.write_json(summary_path, summary)
    if not completed:
        with (root/"priority-report.md").open("a",encoding="utf-8") as stream:
            stream.write("\n\n# AI 分析未完成\n\n请求失败或达到调用限制；详情见 ai-analysis.json。不能将本次结果视为完整 AI 分析。\n")
        raise RuntimeError("AI review did not complete within limits; failure evidence saved")
    lines = ["", "# AI 适配分析", "", "AI 建议；证据引用已检查，仍须人工及真机验证。", "", completed["overview"], "", "## 各页面评估", ""]
    for page in completed["pages"]:
        lines += [f"### {page['page']}", "", page["assessment"], "", "证据：" + ", ".join(page["evidence_ids"]), ""]
        for path in page["path_reviews"]:
            lines += ["#### 路径："+path["path"],"","- 状态："+path["status"],"- 变化："+path["change"],
                "- 可能影响："+path["impact"],"- 验证："+path["verification"],"- 证据："+", ".join(path["evidence_ids"]),""]
    for item in completed["findings"]:
        lines += ["### " + item["finding_id"]+"："+item["title"], item["analysis"], "反例与替代解释："+item["alternatives"], "建议：" + item["recommendation"], "证据：" + ", ".join(item["evidence_ids"]), ""]
    lines += ["## 重点项独立复核", "", "同一模型以独立上下文复核；不代表人工审查或真机验收。", ""]
    for row in completed["review"]["pages"]:
        lines += ["### 复核页面："+row["page"],row["assessment"],"证据："+", ".join(row["evidence_ids"]),""]
    for row in completed["review"]["findings"]:
        lines += ["- "+row["finding_id"]+" / "+row["disposition"]+"："+row["reason"]+"（"+", ".join(row["evidence_ids"])+"）"]
    lines += ["", "### 尚未解决的证据缺口", "", *["- "+g for g in completed["review"]["remaining_gaps"]], ""]
    lines += ["## 下一步", "", *["- " + s for s in completed["next_steps"]]]
    md=root/"priority-report.md"
    md.write_text(md.read_text(encoding="utf-8").replace("AI 未接入","AI 已完成独立分析（见后文）"),encoding="utf-8")
    with md.open("a",encoding="utf-8") as stream:
        stream.write(redact("\n".join(lines)))
    print(json.dumps({"ai_status":"completed","profile":profile,"requests":len(attempts),"read_tools":evidence.calls}))


def run(root):
    """Failure perimeter: any unexpected crash still leaves a failed record on disk."""
    try:
        import ai_pipeline
        ai_pipeline.run(root, api=call_api)
    except Exception as exc:
        _record_crash(root, exc)
        raise


def _record_crash(root, exc):
    analysis=root/"ai-analysis.json"
    if analysis.exists():
        return  # The normal failure path already wrote full evidence.
    message=redact(type(exc).__name__+": "+str(exc)[:300])
    outcome={"schema":2,"prompt_version":ai_prompts.PROMPT_VERSION,"status":"failed",
             "runtime_verified":False,"claim_scope":"ai_suggestions_over_static_evidence",
             "error":message,"attempts":[]}
    try:
        analysis.write_text(redact(json.dumps(outcome,ensure_ascii=False,indent=2)),encoding="utf-8")
        summary_path=root/"priority-summary.json"
        if summary_path.exists():
            summary=json.loads(summary_path.read_text(encoding="utf-8"))
            summary["ai_status"]="failed"
            summary["ai_review"]=outcome
            hostlab.write_json(summary_path,summary)
        report=root/"priority-report.md"
        if report.exists():
            with report.open("a",encoding="utf-8") as stream:
                stream.write("\n\n# AI 分析未完成\n\n分析流程异常中止；详情见 ai-analysis.json。\n")
    except OSError:
        pass


if __name__ == "__main__":
    run(hostlab.STATE/"remote-output")
