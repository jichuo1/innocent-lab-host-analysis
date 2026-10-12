import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import ai_review
import publish_report


def summary():
    sample={"version_code":2,"version_name":"test","sha256":"a"*64}
    pages={p:{"paths":{p+"_native":{"evidence":"static_invoke_observed"}},"protocols":{}} for p in ("comment","dynamic")}
    return {"sample":sample,"baseline":dict(sample,version_code=1),"changes":[],"resource_changes":{},
        "analysis_status":"REVIEW_REQUIRED","limitations":["runtime unknown"],"page_path_matrix":pages,
        "unregistered_protocols":[],"source_snapshot":{"working_tree_dirty":False,"source_records":[]}}


def page_evidence_ids(root):
    """Evidence ids assigned to prefetched pages, in matrix order."""
    data=json.loads((Path(root)/"priority-summary.json").read_text(encoding="utf-8"))
    return {page:"E"+str(i+1).zfill(3) for i,page in enumerate(data["page_path_matrix"])}


def report(ids,pages,finding=True,overview="静态建议，运行未知",deep=None,level="needs_runtime"):
    value={"overview":overview,"pages":[],"findings":[],"next_steps":["补运行证据"]}
    for page in pages:
        value["pages"].append({"page":page,"assessment":"目标与基线需要按路径核对","evidence_ids":[ids[page]],
            "path_reviews":[{"path":page+"_native","status":"static_invoke_observed","change":"无确定变化",
                "impact":"未知","verification":"打开对应入口并核对调用","evidence_ids":[ids[page]]}]})
    if finding:
        value["findings"].append({"title":"评论待验证","page":"comment","level":level,
            "analysis":"调用存在不证明启用","alternatives":"可能是未启用的并存路径",
            "recommendation":"按入口验证","evidence_ids":[deep or ids["comment"]]})
    return value


def review_record(fresh,pages,disposition="retained",revision=None):
    record={"pages":[{"page":p,"assessment":"两侧证据已重新读取，仍需运行验证","evidence_ids":[fresh[p]]} for p in pages],
        "findings":[{"finding_id":"F001","disposition":disposition,"reason":"缺少实际启用证据","evidence_ids":[fresh["comment"]]}],
        "remaining_gaps":["运行条件未知"]}
    if revision is not None:
        record["findings"][0]["revision"]=revision
    return record


def response(name,args):
    return ({"role":"assistant","content":None,"tool_calls":[{
        "id":"call-1","type":"function","function":{"name":name,"arguments":json.dumps(args)}}]},{},"test-model")


class DetailedReviewTest(unittest.TestCase):
    def root(self,folder):
        root=Path(folder)
        (root/"priority-summary.json").write_text(json.dumps(summary()),encoding="utf-8")
        (root/"priority-report.md").write_text("AI 未接入",encoding="utf-8")
        for side in ("target","baseline"):
            frozen={"sample":{"version_code":2,"version_name":"test","sha256":"a"*64,"revision":"r"*40},
                    "families":{},"class_records":[],"protocol_paths":{},"invoke_edges":[]}
            (root/("priority-"+side+".json")).write_text(json.dumps(frozen),encoding="utf-8")
        return root

    def test_prefetch_covers_every_page_without_model_budget(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.root(folder)
            data=json.loads((root/"priority-summary.json").read_text(encoding="utf-8"))
            evidence=ai_review.Evidence(root,data)
            evidence.limit=0
            views=ai_review.prefetch_evidence(evidence,data)
            self.assertEqual([v["page"] for v in views],list(data["page_path_matrix"]))
            self.assertEqual(evidence.calls,0)
            self.assertEqual(len(evidence.journal),2)
    def test_end_to_end_review_uses_fresh_session_and_rereads_both_pages(self):
        seen=[]
        with tempfile.TemporaryDirectory() as folder:
            root=self.root(folder)
            ids=page_evidence_ids(root)
            fresh={"comment":"E005","dynamic":"E006"}
            replies=iter([response("family_evidence",{"family":"comment_native","side":"target"}),
                response("protocol_evidence",{"protocol":"comment_java_moss","side":"target"}),
                response("finish_report",report(ids,("comment","dynamic"),deep="E003")),
                response("finish_review",review_record(fresh,("comment","dynamic")))])
            def api(profile,messages,tools,force_tool=None,session_id=None):
                seen.append(copy.deepcopy(messages))
                return next(replies)
            with patch.object(ai_review,"call_api",side_effect=api):
                ai_review.run(root)
                outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
                self.assertEqual(outcome["review_status"],"completed")
                self.assertFalse(outcome["runtime_verified"])
                self.assertEqual([x["stage"] for x in outcome["attempts"]],["draft","draft","draft","review"])
                self.assertEqual([x["profile"] for x in outcome["attempts"]],["primary","primary","primary","primary"])
                self.assertEqual(outcome["limits"]["prefetched_pages"],2)
                # The review session starts from a fresh context: no draft assistant/tool messages.
                self.assertEqual(len(seen[3]),2)
                self.assertIn("draft",json.loads(seen[3][1]["content"]))
                self.assertIn("fresh_refresh",json.loads(seen[3][1]["content"]))
                draft=json.loads((root/"ai-draft.json").read_text(encoding="utf-8"))
                self.assertEqual(draft["findings"][0]["finding_id"],"F001")
                self.assertTrue((root/"ai-review.json").exists())
                self.assertIn("重点项独立复核",(root/"priority-report.md").read_text(encoding="utf-8"))

    def test_assembled_report_applies_review_dispositions(self):
        ids={"comment":"E001","dynamic":"E002"}
        draft=report(ids,("comment","dynamic"))
        draft["findings"][0]["finding_id"]="F001"
        revised=review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic"),
            disposition="revised",revision={"recommendation":"先验证评论入口"})
        final=ai_review.assemble_report(draft,revised)
        self.assertEqual(final["findings"][0]["recommendation"],"先验证评论入口")
        rejected=review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic"),disposition="rejected")
        dropped=ai_review.assemble_report(draft,rejected)
        self.assertEqual(dropped["findings"],[])
        illegal=review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic"))
        illegal["findings"][0]["revision"]={}
        with self.assertRaisesRegex(RuntimeError,"(?i)revision patch"):
            ai_review.assemble_report(draft,illegal)

    def test_review_failure_preserves_draft_but_does_not_complete(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            ids=page_evidence_ids(root)
            replies=[response("family_evidence",{"family":"comment_native","side":"target"}),
                response("protocol_evidence",{"protocol":"comment_java_moss","side":"target"}),
                response("finish_report",report(ids,("comment","dynamic"),deep="E003")),
                RuntimeError("API HTTP 403")]
            with patch.object(ai_review,"call_api",side_effect=replies), patch.object(ai_review.time,"sleep"):
                with self.assertRaises(RuntimeError):ai_review.run(root)
            result=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"failed")
            self.assertEqual(result["review_status"],"not_completed")
            self.assertTrue((root/"ai-draft.json").exists())

    def test_review_budget_survives_rejected_record_and_502(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            ids=page_evidence_ids(root)
            fresh={"comment":"E005","dynamic":"E006"}
            bad=review_record(fresh,("comment","dynamic"))
            bad.pop("remaining_gaps")
            replies=[response("family_evidence",{"family":"comment_native","side":"target"}),
                response("protocol_evidence",{"protocol":"comment_java_moss","side":"target"}),
                response("finish_report",report(ids,("comment","dynamic"),deep="E003")),
                RuntimeError("API HTTP 502"),
                response("finish_review",bad),
                response("finish_review",review_record(fresh,("comment","dynamic")))]
            def api(profile,messages,tools,force_tool=None,session_id=None):
                if replies:
                    item=replies.pop(0)
                    if isinstance(item,Exception):raise item
                    return item
                raise RuntimeError("unexpected extra request")
            with patch.object(ai_review,"call_api",side_effect=api) as mock_api, patch.object(ai_review.time,"sleep"):
                ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["review_status"],"completed")
            self.assertEqual([x["stage"] for x in outcome["attempts"]],["draft","draft","draft","review","review","review"])
            self.assertEqual(mock_api.call_count,6)

    def test_transport_retry_allowance_is_bounded(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            with patch.object(ai_review,"call_api",side_effect=RuntimeError("API failure: TimeoutError")) as api, patch.object(ai_review.time,"sleep"):
                with self.assertRaises(RuntimeError):ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["status"],"failed")
            self.assertLessEqual(api.call_count,ai_review.HARD_REQUEST_CAP)
            self.assertEqual(outcome["limits"]["hard_cap"],ai_review.HARD_REQUEST_CAP)

    def test_session_header_is_sent_for_gateway_compatibility(self):
        captured={}
        class FakeResponse:
            def read(self,n):return json.dumps({"choices":[{"message":{"content":"ok"}}],"usage":{}}).encode()
            def __enter__(self):return self
            def __exit__(self,*args):return False
        class FakeOpener:
            def open(self,request,timeout=None):
                captured["headers"]=dict(request.headers)
                return FakeResponse()
        with patch.dict("os.environ",{"AI_API_KEY_PRIMARY":"k","AI_PRIMARY_BASE_URL":"https://example.com/v1","AI_PRIMARY_MODEL":"m"}), \
             patch.object(ai_review.urllib.request,"build_opener",return_value=FakeOpener()):
            ai_review.call_api("primary",[],[],session_id="sess-123")
        self.assertEqual(captured["headers"].get("X-opencode-session"),"sess-123")

    def test_review_journal_is_bounded_but_keeps_locator_fields(self):
        journal=[{"id":"E001","tool":"page_evidence","args":{"page":"comment"},"result":{"blob":"x"*9000}},
                 {"id":"E002","tool":"page_evidence","args":{"page":"dynamic"},"result":{"small":"ok"}}]
        rows=ai_review.bounded_journal(journal)
        self.assertEqual([r["id"] for r in rows],["E001","E002"])
        self.assertEqual(rows[0]["args"],{"page":"comment"})
        self.assertTrue(rows[0]["result"]["truncated"])
        self.assertLessEqual(len(rows[0]["result"]["excerpt"]),ai_review.REVIEW_EXCERPT_CHARS)
        self.assertEqual(rows[1]["result"],{"small":"ok"})

    def test_prefetch_view_is_bounded_and_keeps_page_identity(self):
        big={"page":"comment","evidence_id":"E001","limits":"x","sides":{
            "target":{"sample":{},"families":{"f":{"summary":{},"samples":[{"blob":"y"*4000}]*6}},
                      "protocols":{"p":{"summary":{},"caller_samples":[["a"],["b"],["c"]]}}},
            "baseline":{"missing":True}}}
        view=ai_review.prefetch_view(big)
        self.assertEqual(view["page"],"comment")
        self.assertEqual(view["evidence_id"],"E001")
        self.assertTrue(view.get("truncated") or len(json.dumps(view,ensure_ascii=False))<=ai_review.PREFETCH_VIEW_CHARS)

    def test_draft_requires_deep_dive_before_submit(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.root(folder)
            ids=page_evidence_ids(root)
            replies=[response("finish_report",report(ids,("comment","dynamic"))),
                response("family_evidence",{"family":"comment_native","side":"target"}),
                response("protocol_evidence",{"protocol":"comment_java_moss","side":"target"}),
                response("finish_report",report(ids,("comment","dynamic"),deep="E003")),
                response("finish_review",review_record({"comment":"E005","dynamic":"E006"},("comment","dynamic")))]
            with patch.object(ai_review,"call_api",side_effect=replies) as api:
                ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["review_status"],"completed")
            errors=outcome["attempts"][0].get("call_errors",[])
            self.assertTrue(any("deep-dive" in e["error"] for e in errors),errors)
            self.assertEqual(api.call_count,5)

    def test_draft_rejects_findings_without_deep_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.root(folder)
            ids=page_evidence_ids(root)
            replies=[response("family_evidence",{"family":"comment_native","side":"target"}),
                response("protocol_evidence",{"protocol":"comment_java_moss","side":"target"}),
                response("finish_report",report(ids,("comment","dynamic"))),
                response("finish_report",report(ids,("comment","dynamic"),deep="E003")),
                response("finish_review",review_record({"comment":"E005","dynamic":"E006"},("comment","dynamic")))]
            with patch.object(ai_review,"call_api",side_effect=replies):
                ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            errors=outcome["attempts"][2].get("call_errors",[])
            self.assertTrue(any("deep-dive evidence" in e["error"] for e in errors),errors)

    def test_revision_value_errors_are_rejected_without_crash(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.root(folder)
            ids=page_evidence_ids(root)
            valid={"comment":"E005","dynamic":"E006"}
            bad={"comment":"E005","dynamic":"E006"}
            record=review_record(bad,("comment","dynamic"),disposition="revised",revision={"level":"totally_bogus"})
            replies=[response("family_evidence",{"family":"comment_native","side":"target"}),
                response("protocol_evidence",{"protocol":"comment_java_moss","side":"target"}),
                response("finish_report",report(ids,("comment","dynamic"),deep="E003")),
                response("finish_review",record),
                response("finish_review",review_record(valid,("comment","dynamic"),disposition="revised",
                    revision={"recommendation":"先验证评论入口"}))]
            with patch.object(ai_review,"call_api",side_effect=replies):
                ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["review_status"],"completed")
            errors=outcome["attempts"][3].get("call_errors",[])
            self.assertTrue(any("Revision level" in e["error"] for e in errors),errors)

    def test_crash_still_records_failed_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.root(folder)
            with patch.object(ai_review,"prefetch_evidence",side_effect=FileNotFoundError("priority-target.json")):
                with self.assertRaises(RuntimeError):
                    ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["status"],"failed")
            summary=json.loads((root/"priority-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["ai_status"],"failed")
            self.assertIn("AI 分析未完成",(root/"priority-report.md").read_text(encoding="utf-8"))

    def test_empty_completion_gets_targeted_instruction(self):
        seen=[]
        def api(profile,messages,tools,force_tool=None,session_id=None):
            seen.append(copy.deepcopy(messages))
            if len(seen)==1:
                return ({"role":"assistant","content":None},{"completion_tokens":ai_review.MAX_OUTPUT},"m")
            raise RuntimeError("stop")
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            with patch.object(ai_review,"call_api",side_effect=api), patch.object(ai_review.time,"sleep"):
                with self.assertRaises(RuntimeError):ai_review.run(root)
        content=seen[1][-1]["content"]
        self.assertIn("没有产生任何工具调用",content)
        self.assertIn("finish_report",content)

    def test_deadline_breaks_loop_and_records_failed(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            times=iter([10**9,10**9+ai_review.AI_DEADLINE_SECONDS+1])
            with patch.object(ai_review.time,"monotonic",side_effect=lambda:next(times)), \
                 patch.object(ai_review,"call_api") as api, patch.object(ai_review.time,"sleep"):
                with self.assertRaises(RuntimeError):ai_review.run(root)
            api.assert_not_called()
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["status"],"failed")

    def test_missing_or_changed_static_status_is_rejected(self):
        for change in ("missing","status"):
            value=report({"comment":"E001","dynamic":"E002"},("comment","dynamic"))
            path=value["pages"][0]["path_reviews"]
            if change=="missing":path.clear()
            else:path[0]["status"]="adapted"
            with self.assertRaises(RuntimeError):
                ai_review.validate_report(value,{"E000","E001","E002"},["comment","dynamic"],summary()["page_path_matrix"])

    def test_old_reads_cannot_satisfy_independent_review(self):
        data=summary()
        evidence=ai_review.Evidence(Path("."),data)
        evidence.ids.update({"E001","E002","E003","E004"})
        evidence.journal=[{"id":"E003","tool":"page_evidence","args":{"page":"comment"}},
                          {"id":"E004","tool":"page_evidence","args":{"page":"dynamic"}}]
        draft=report({"comment":"E001","dynamic":"E002"},("comment","dynamic"))
        draft["findings"][0]["finding_id"]="F001"
        with self.assertRaises(RuntimeError):
            ai_review.validate_review_record(review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic")),
                draft,evidence,["comment","dynamic"],2)

    def test_rejected_finding_cannot_remain_in_final_report(self):
        data=summary()
        evidence=ai_review.Evidence(Path("."),data)
        evidence.ids.update({"E001","E002","E003","E004"})
        evidence.journal=[{"id":"E003","tool":"page_evidence","args":{"page":"comment"}},
                          {"id":"E004","tool":"page_evidence","args":{"page":"dynamic"}}]
        draft=report({"comment":"E001","dynamic":"E002"},("comment","dynamic"))
        draft["findings"][0]["finding_id"]="F001"
        record=review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic"),disposition="rejected")
        validated=ai_review.validate_review_record(record,draft,evidence,["comment","dynamic"],0)
        assembled=ai_review.assemble_report(draft,validated)
        self.assertEqual(assembled["findings"],[])

    def test_schema_two_without_review_cannot_publish_success(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);out=root/"remote-output";out.mkdir()
            self.root(out)
            data=summary();data.update({"ai_status":"completed","ai_review":{"schema":2,"status":"completed"}})
            (out/"priority-summary.json").write_text(json.dumps(data),encoding="utf-8")
            entry,files,_,_=publish_report.prepare(root,"123","1")
            self.assertFalse(entry["complete"])
            self.assertIsNone(entry["release_url"])
            self.assertFalse(any(path.endswith("latest.json") for path in files))

    def test_unresolved_finding_cannot_be_upgraded_to_static_fact(self):
        data=summary()
        evidence=ai_review.Evidence(Path("."),data)
        evidence.ids.update({"E001","E002","E003","E004"})
        evidence.journal=[{"id":"E003","tool":"page_evidence","args":{"page":"comment"}},
                          {"id":"E004","tool":"page_evidence","args":{"page":"dynamic"}}]
        draft=report({"comment":"E001","dynamic":"E002"},("comment","dynamic"),level="static_evidence")
        draft["findings"][0]["finding_id"]="F001"
        record=ai_review.validate_review_record(review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic"),
            disposition="needs_more_evidence"),draft,evidence,["comment","dynamic"],0)
        assembled=ai_review.assemble_report(draft,record)
        self.assertEqual(assembled["findings"][0]["level"],"needs_runtime")

    def test_revised_finding_may_set_static_evidence_level(self):
        data=summary()
        evidence=ai_review.Evidence(Path("."),data)
        evidence.ids.update({"E001","E002","E003","E004"})
        evidence.journal=[{"id":"E003","tool":"page_evidence","args":{"page":"comment"}},
                          {"id":"E004","tool":"page_evidence","args":{"page":"dynamic"}}]
        draft=report({"comment":"E001","dynamic":"E002"},("comment","dynamic"))
        draft["findings"][0]["finding_id"]="F001"
        record=ai_review.validate_review_record(review_record({"comment":"E003","dynamic":"E004"},("comment","dynamic"),
            disposition="revised",revision={"level":"static_evidence"}),draft,evidence,["comment","dynamic"],0)
        assembled=ai_review.assemble_report(draft,record)
        self.assertEqual(assembled["findings"][0]["level"],"static_evidence")


if __name__=="__main__":
    unittest.main()
