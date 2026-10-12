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
import ai_prompts

MAX_REQUESTS = 8
MAX_TRANSPORT_RETRIES = 2
MAX_TOOLS = 8
MAX_OUTPUT = 16384
MAX_CONTEXT_CHARS = 160000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def redact(text):
    for name in ("AI_API_KEY_PRIMARY", "AI_API_KEY_BACKUP", "HF_TOKEN", "GH_TOKEN"):
        value = os.environ.get(name)
        if value:
            text = text.replace(value, "[REDACTED]")
    return text


def call_api(profile, messages, tools, force_finish=False, session_id=None):
    name = profile.upper()
    key = os.environ.get("AI_API_KEY_" + name, "")
    base = os.environ.get("AI_" + name + "_BASE_URL", "").rstrip("/")
    model = os.environ.get("AI_" + name + "_MODEL", "")
    parsed = urllib.parse.urlsplit(base)
    if not key or not model or parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise RuntimeError("API configuration incomplete or invalid")
    payload = {"model": model, "messages": messages, "tools": tools,
               "tool_choice": {"type": "function", "function": {"name": "finish_report"}} if force_finish else "auto",
               "max_tokens": MAX_OUTPUT, "stream": False}
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json",
               "User-Agent": "HostLab-AIReview/1"}
    if session_id:
        # OpenCode-compatible gateways route and cache prompts per session ID.
        headers["x-opencode-session"] = session_id
    request = urllib.request.Request(base + "/chat/completions", data=json.dumps(payload).encode(),
        headers=headers)
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=180) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise RuntimeError("API response exceeds bound")
        data = json.loads(redact(raw.decode("utf-8")))
        message = data["choices"][0]["message"]
        # Do not persist hidden reasoning or vendor response metadata.
        clean = {"role": "assistant", "content": message.get("content")}
        if message.get("tool_calls"):
            clean["tool_calls"] = message["tool_calls"]
        return clean, data.get("usage", {}), model
    except urllib.error.HTTPError as exc:
        raise RuntimeError("API HTTP " + str(exc.code)) from None
    except Exception as exc:
        raise RuntimeError("API failure: " + type(exc).__name__) from None


def tool(name, description, properties, required):
    return {"type": "function", "function": {"name": name, "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required, "additionalProperties": False}}}


def validate_report(value, ids, pages, matrix=None):
    if not isinstance(value, dict) or not isinstance(value.get("overview"), str):
        raise RuntimeError("Report requires overview")
    assessments = value.get("pages", [])
    if len(assessments) != len(pages) or {p.get("page") for p in assessments} != set(pages):
        raise RuntimeError("Assess every registered page exactly once")
    findings = value.get("findings", [])
    if not isinstance(findings, list) or len(findings) > 12:
        raise RuntimeError("Findings exceed bound")
    if not isinstance(value.get("next_steps"),list) or len(value["next_steps"])>12 or not all(isinstance(s,str) for s in value["next_steps"]):
        raise RuntimeError("Bound next_steps to at most twelve strings")
    for item in assessments + findings:
        refs = item.get("evidence_ids", [])
        if not refs or any(ref not in ids for ref in refs):
            raise RuntimeError("Only cite actual E000/E001 evidence IDs")
    for item in assessments:
        if not isinstance(item.get("assessment"),str):
            raise RuntimeError("Page assessment must be text")
        if matrix is not None:
            checks=item.get("path_reviews",[])
            expected=set(matrix[item["page"]].get("paths",{}))
            if len(checks)!=len(expected) or {c.get("path") for c in checks}!=expected:
                raise RuntimeError("Assess each registered path exactly once")
            for check in checks:
                if not all(isinstance(check.get(k),str) and check[k].strip() for k in ("status","change","impact","verification")):
                    raise RuntimeError("Path needs status, change, impact and verification")
                if check["status"]!=matrix[item["page"]]["paths"][check["path"]]["evidence"]:
                    raise RuntimeError("Path status must match static evidence")
                if not check.get("evidence_ids") or any(ref not in ids for ref in check["evidence_ids"]):
                    raise RuntimeError("Path references unknown evidence")
    for item in findings:
        if item.get("level") not in {"candidate", "static_evidence", "needs_runtime"}:
            raise RuntimeError("Unsupported claim level")
        if item.get("page") not in pages or not all(isinstance(item.get(k),str) for k in ("title","analysis","recommendation")):
            raise RuntimeError("Finding requires a registered page and text fields")
        if matrix is not None and (not isinstance(item.get("alternatives"),str) or not item["alternatives"].strip()):
            raise RuntimeError("Finding must discuss alternative explanations")
    if len(json.dumps(value, ensure_ascii=False)) > 50000:
        raise RuntimeError("Report exceeds output bound")
    return value


def priority_pages(summary):
    changed={c.get("family") for c in summary.get("changes",[])}
    return [name for name,page in summary["page_path_matrix"].items()
            if name in {"comment","dynamic"} or len(page.get("paths",{}))>1 or changed.intersection(page.get("paths",{}))]


def validate_review(report,draft,evidence,priorities,review_start):
    review=report.get("review")
    if not isinstance(review,dict):
        raise RuntimeError("Independent review is required")
    rows=review.get("pages",[])
    if len(rows)!=len(priorities) or {r.get("page") for r in rows}!=set(priorities):
        raise RuntimeError("Review every priority page exactly once")
    findings=review.get("findings",[])
    expected={r["finding_id"] for r in draft["findings"]}
    if len(findings)!=len(expected) or {r.get("finding_id") for r in findings}!=expected:
        raise RuntimeError("Review every draft finding exactly once")
    for row in rows+findings:
        field="assessment" if "page" in row else "reason"
        if not isinstance(row.get(field),str) or not row[field].strip():
            raise RuntimeError("Review requires an explanation")
        if not row.get("evidence_ids") or any(ref not in evidence.ids for ref in row["evidence_ids"]):
            raise RuntimeError("Review references unknown evidence")
    for row in findings:
        if row.get("disposition") not in {"retained","revised","rejected","needs_more_evidence"}:
            raise RuntimeError("Invalid review disposition")
    final=report.get("findings",[])
    retained={r["finding_id"] for r in findings if r["disposition"]!="rejected"}
    if len(final)!=len(retained) or {r.get("finding_id") for r in final}!=retained:
        raise RuntimeError("Final findings must implement review dispositions")
    uncertain={r["finding_id"] for r in findings if r["disposition"]=="needs_more_evidence"}
    if any(r["finding_id"] in uncertain and r["level"]=="static_evidence" for r in final):
        raise RuntimeError("Insufficient evidence findings must remain uncertain")
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
        self.limit = MAX_TOOLS

    def dataset(self, side):
        if side not in {"target", "baseline"}:
            raise RuntimeError("Invalid side")
        if side not in self.data:
            self.data[side] = json.loads((self.root / ("priority-" + side + ".json")).read_text(encoding="utf-8"))
        return self.data[side]

    def execute(self, name, args):
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
            records = (self.summary.get("source_snapshot") or {}).get("source_records", [])
            matches = [r for r in records if r["path"] == args["path"]]
            if len(matches) != 1:
                raise RuntimeError("Select an exact source path from E000")
            r = matches[0]
            result = {"path": r["path"], "sha256": r["sha256"], "source": r["source"][:9000],
                      "truncated": len(r["source"]) > 9000, "working_tree_dirty": self.summary["source_snapshot"].get("working_tree_dirty")}
        elif name == "decompile_class":
            data = self.dataset(side)
            class_name = args["class_name"]
            descriptor = "L" + class_name.replace(".", "/") + ";"
            allowed = {r["class"] for r in data["class_records"]}
            allowed.update(e[2] for e in data["invoke_edges"])
            allowed.update(e[6] for e in data["invoke_edges"])
            if descriptor not in allowed or not re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+", class_name):
                raise RuntimeError("Class must be a real member in the frozen evidence")
            sample = data["sample"]
            command = [sys.executable, str(Path(__file__).with_name("hostlab.py")), "decompile",
                       "--version-code", str(sample["version_code"]), "--sha256", sample["sha256"],
                       "--revision", sample["revision"], "--class", class_name, "--timeout", "120"]
            rc = subprocess.run(command, capture_output=True, timeout=150, check=False).returncode
            folder = hostlab.STATE / "reports" / str(sample["version_code"]) / sample["sha256"][:16]
            sources = sorted(folder.glob("*/class.java"))
            if rc or not sources:
                raise RuntimeError("Class decompile failed or timed out")
            source = sources[-1]
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
        if len(text) > 14000:
            result = {"evidence_id": eid, "truncated": True, "total_characters": len(text), "excerpt": text[:13000]}
        self.ids.add(eid)
        self.journal.append({"id": eid, "tool": name, "args": args, "result": result})
        return result


def transport_retry_credit(attempts):
    """Extra request slots for dropped connections, bounded by MAX_TRANSPORT_RETRIES."""
    failures=sum(1 for a in attempts if a.get("status")=="failed" and str(a.get("reason","")).startswith("API failure:"))
    return min(failures,MAX_TRANSPORT_RETRIES)


def collect_report(messages,tools,evidence,summary,attempts,profile,request_limit,draft=None):
    review_start=len(evidence.journal)
    # One stable session ID per conversation; OpenCode-compatible gateways use it for routing
    # and prompt caching, and reject session-less requests with MissingSessionID.
    session_id="hostlab-"+os.urandom(12).hex()
    while len(attempts)<request_limit+transport_retry_credit(attempts):
        if len(json.dumps(messages,ensure_ascii=False))>MAX_CONTEXT_CHARS:
            break
        try:
            required=set(priority_pages(summary))&{"comment","dynamic"}
            reread={r["args"].get("page") for r in evidence.journal[review_start:] if r["tool"]=="page_evidence"}
            force=len(attempts)>=request_limit-1 or (draft is None and evidence.calls>=5)
            if draft is not None and not required.issubset(reread):
                force=False
            message,usage,model=call_api(profile,messages,tools,force,session_id=session_id)
            attempts.append({"stage":"review" if draft else "draft","profile":profile,"model":model,"usage":usage,"status":"response_received"})
        except RuntimeError as exc:
            reason=str(exc)
            attempts.append({"stage":"review" if draft else "draft","profile":profile,"status":"failed","reason":reason,"billing_unknown":True})
            if profile=="primary" and os.environ.get("AI_ALLOW_FALLBACK","true").lower()=="true":
                profile="backup"
                continue
            retryable=reason.startswith("API failure:") or any(code in reason for code in ("HTTP 429","HTTP 500","HTTP 502","HTTP 503","HTTP 504"))
            if retryable and len(attempts)<request_limit+transport_retry_credit(attempts):
                time.sleep(2)
                continue
            break
        messages.append(message)
        calls=message.get("tool_calls",[])
        if not calls:
            messages.append({"role":"user","content":"先用证据工具调查，再调用 finish_report 提交结构化报告。"})
            continue
        completed=None
        for call in calls:
            try:
                name=call["function"]["name"]
                args=json.loads(call["function"]["arguments"])
                if name=="finish_report":
                    if evidence.calls==0:
                        raise RuntimeError("Investigate actual evidence before finishing")
                    candidate=validate_report(args,evidence.ids,list(summary["page_path_matrix"]),summary["page_path_matrix"])
                    if draft is not None:
                        validate_review(candidate,draft,evidence,priority_pages(summary),review_start)
                    completed=candidate
                    result={"accepted":True}
                else:
                    result=evidence.execute(name,args)
            except Exception as exc:
                result={"error":str(exc)[:300] if type(exc) is RuntimeError else type(exc).__name__}
            messages.append({"role":"tool","tool_call_id":call["id"],"content":redact(json.dumps(result,ensure_ascii=False))})
        if completed:
            return completed,profile
    return None,profile


def run(root):
    summary_path = root / "priority-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    evidence = Evidence(root, summary)
    seed = {"evidence_id": "E000", "sample": summary["sample"], "baseline": summary.get("baseline"),
        "pages": copy.deepcopy(summary["page_path_matrix"]), "changes": summary["changes"],
        "resource_change_counts": {k:len(v) for k,v in (summary.get("resource_changes") or {}).items() if isinstance(v,list)},
        "limitations": summary["limitations"], "source_files": [r["path"] for r in (summary.get("source_snapshot") or {}).get("source_records", [])],
        "source_dirty": (summary.get("source_snapshot") or {}).get("working_tree_dirty"),
        "unregistered_protocols": summary.get("unregistered_protocols", [])}
    # Keep detailed signatures in tools; initial evidence covers all registered pages.
    for page in seed["pages"].values():
        page["protocols"] = {k:{a:b for a,b in v.items() if a != "signatures"} for k,v in page.get("protocols", {}).items()}
    seed["changes"] = [{k:v for k,v in c.items() if k not in {"before","after"}} for c in seed["changes"]]
    messages = [{"role":"system", "content":ai_prompts.DRAFT},
                {"role":"user", "content":json.dumps(seed,ensure_ascii=False)}]
    side = {"type":"string","enum":["target","baseline"]}
    string = {"type":"string"}
    tools = [tool("page_evidence","Compare every registered family and protocol of a page in target and baseline",{"page":string},["page"]),
             tool("family_evidence","Read family structures, counts and bounded class samples",{"family":string,"side":side},["family","side"]),
             tool("protocol_evidence","Read exact signatures and actual static invoke callers",{"protocol":string,"side":side},["protocol","side"]),
             tool("module_source","Read a frozen production source file, never filesystem paths",{"path":string},["path"]),
             tool("decompile_class","Read pseudo-Java of a real frozen APK class",{"class_name":string,"side":side},["class_name","side"]),
             tool("finish_report","Submit Chinese review with evidence citations; no adaptation acceptance",{
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
    attempts=[]
    # Reserve two tool calls and two API requests for the independent review session.
    evidence.limit=MAX_TOOLS-2
    draft,profile=collect_report(messages,tools,evidence,summary,attempts,profile,MAX_REQUESTS-2)
    completed=None
    if draft:
        for index,finding in enumerate(draft["findings"],1):
            finding["finding_id"]=f"F{index:03d}"
        (root/"ai-draft.json").write_text(redact(json.dumps(draft,ensure_ascii=False,indent=2)),encoding="utf-8")
        evidence.limit=MAX_TOOLS
        review_tools=copy.deepcopy(tools)
        review_schema=review_tools[-1]["function"]["parameters"]
        refs={"type":"array","items":string}
        review_schema["properties"]["review"]={"type":"object","properties":{
            "pages":{"type":"array","items":{"type":"object","properties":{"page":string,"assessment":string,"evidence_ids":refs},"required":["page","assessment","evidence_ids"]}},
            "findings":{"type":"array","items":{"type":"object","properties":{"finding_id":string,"disposition":{"type":"string","enum":["retained","revised","rejected","needs_more_evidence"]},"reason":string,"evidence_ids":refs},"required":["finding_id","disposition","reason","evidence_ids"]}},
            "remaining_gaps":{"type":"array","items":string}},"required":["pages","findings","remaining_gaps"]}
        review_schema["required"].append("review")
        review_schema["properties"]["findings"]["items"]["properties"]["finding_id"]=string
        review_schema["properties"]["findings"]["items"]["required"].append("finding_id")
        review_messages=[{"role":"system","content":ai_prompts.REVIEW},
            {"role":"user","content":json.dumps({"seed":seed,"draft":draft,"priority_pages":priority_pages(summary),"evidence":evidence.journal},ensure_ascii=False)}]
        completed,profile=collect_report(review_messages,review_tools,evidence,summary,attempts,profile,MAX_REQUESTS,draft)
    (root/"ai-review.json").write_text(redact(json.dumps(completed.get("review") if completed else {"status":"not_completed"},ensure_ascii=False,indent=2)),encoding="utf-8")
    outcome = {"schema":2,"prompt_version":ai_prompts.PROMPT_VERSION,
               "prompt_sha256":hashlib.sha256((ai_prompts.DRAFT+ai_prompts.REVIEW).encode()).hexdigest(),
               "status":"completed" if completed else "failed", "profile":profile,
               "runtime_verified":False,"claim_scope":"ai_suggestions_over_static_evidence", "attempts":attempts,
               "limits":{"api_requests":MAX_REQUESTS,"transport_retry_allowance":MAX_TRANSPORT_RETRIES,"read_tools":MAX_TOOLS,"output_tokens_per_request":MAX_OUTPUT,"usd_cap_enforced":False},
               "report":completed,"review_status":"completed" if completed else "not_completed","review":completed.get("review") if completed else None,"read_tool_calls":evidence.calls}
    (root/"ai-analysis.json").write_text(redact(json.dumps(outcome,ensure_ascii=False,indent=2)),encoding="utf-8")
    (root/"ai-evidence.json").write_text(redact(json.dumps({"E000":seed,"tools":evidence.journal},ensure_ascii=False,indent=2)),encoding="utf-8")
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


if __name__ == "__main__":
    run(hostlab.STATE/"remote-output")
