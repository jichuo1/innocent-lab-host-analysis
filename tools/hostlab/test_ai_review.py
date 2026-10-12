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
    return {"sample":sample,"baseline":dict(sample,version_code=1),"changes":[],
        "analysis_status":"REVIEW_REQUIRED","limitations":["runtime unknown"],
        "page_path_matrix":{p:{"paths":{p+"_native":{"evidence":"static_invoke_observed"}},"protocols":{}}
                            for p in ("comment","dynamic")}}


def report(review=False):
    value={"overview":"静态建议，运行未知","pages":[],"findings":[{
        "title":"评论待验证","page":"comment","level":"needs_runtime","analysis":"调用存在不证明启用",
        "alternatives":"可能是未启用的并存路径","recommendation":"按入口验证","evidence_ids":["E001"]}],
        "next_steps":["补运行证据"]}
    for page in ("comment","dynamic"):
        value["pages"].append({"page":page,"assessment":"目标与基线需要按路径核对","evidence_ids":["E000"],
            "path_reviews":[{"path":page+"_native","status":"static_invoke_observed","change":"无确定变化",
                "impact":"未知","verification":"打开对应入口并核对调用","evidence_ids":["E000"]}]})
    if review:
        value["findings"][0]["finding_id"]="F001"
        value["review"]={"pages":[{"page":p,"assessment":"两侧证据已重新读取，仍需运行验证","evidence_ids":[eid]}
            for p,eid in (("comment","E002"),("dynamic","E003"))],
            "findings":[{"finding_id":"F001","disposition":"needs_more_evidence","reason":"缺少实际启用证据","evidence_ids":["E002"]}],
            "remaining_gaps":["运行条件未知"]}
    return value


def response(*calls):
    return ({"role":"assistant","content":None,"tool_calls":[{
        "id":str(i),"type":"function","function":{"name":name,"arguments":json.dumps(args)}}
        for i,(name,args) in enumerate(calls)]},{},"test-model")


class DetailedReviewTest(unittest.TestCase):
    def root(self,folder):
        root=Path(folder)
        data=summary()
        (root/"priority-summary.json").write_text(json.dumps(data),encoding="utf-8")
        (root/"priority-report.md").write_text("AI 未接入",encoding="utf-8")
        for side in ("target","baseline"):
            frozen={"sample":data["sample" if side=="target" else "baseline"],"families":{},
                    "class_records":[],"protocol_paths":{},"invoke_edges":[]}
            (root/("priority-"+side+".json")).write_text(json.dumps(frozen),encoding="utf-8")
        return root

    def test_end_to_end_review_uses_fresh_session_and_rereads_both_pages(self):
        seen=[]
        replies=iter([response(("page_evidence",{"page":"comment"})),response(("finish_report",report())),
            response(("page_evidence",{"page":"comment"}),("page_evidence",{"page":"dynamic"})),
            response(("finish_report",report(True)))])
        def api(profile,messages,tools,force,session_id=None):
            seen.append(copy.deepcopy(messages))
            return next(replies)
        with tempfile.TemporaryDirectory() as folder, patch.object(ai_review,"call_api",side_effect=api):
            root=self.root(folder)
            ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["review_status"],"completed")
            self.assertFalse(outcome["runtime_verified"])
            self.assertEqual([x["stage"] for x in outcome["attempts"]],["draft","draft","review","review"])
            self.assertEqual(len(seen[2]),2)  # No assistant messages from the draft session.
            self.assertIn("draft",json.loads(seen[2][1]["content"]))
            self.assertTrue((root/"ai-draft.json").exists())
            self.assertIn("重点项独立复核",(root/"priority-report.md").read_text(encoding="utf-8"))

    def test_review_failure_preserves_draft_but_does_not_complete(self):
        replies=[response(("page_evidence",{"page":"comment"})),response(("finish_report",report())),RuntimeError("API HTTP 403")]
        with tempfile.TemporaryDirectory() as folder, patch.object(ai_review,"call_api",side_effect=replies), patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            with self.assertRaises(RuntimeError):ai_review.run(root)
            result=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"],"failed")
            self.assertEqual(result["review_status"],"not_completed")
            self.assertTrue((root/"ai-draft.json").exists())

    def test_retry_and_review_share_the_six_request_budget(self):
        invalid=report(True);invalid.pop("review")
        replies=[RuntimeError("API HTTP 502"),response(("page_evidence",{"page":"comment"})),
            response(("finish_report",report())),
            response(("page_evidence",{"page":"comment"}),("page_evidence",{"page":"dynamic"})),
            response(("finish_report",invalid)),response(("finish_report",report(True)))]
        with tempfile.TemporaryDirectory() as folder, patch.object(ai_review,"call_api",side_effect=replies) as api, patch.object(ai_review.time,"sleep"), patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder);ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(api.call_count,6)
            self.assertEqual(len(outcome["attempts"]),6)
            self.assertEqual(outcome["review_status"],"completed")

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

    def test_transport_failure_retries_within_allowance(self):
        replies=[RuntimeError("API failure: TimeoutError"),response(("page_evidence",{"page":"comment"})),
            response(("finish_report",report())),
            response(("page_evidence",{"page":"comment"}),("page_evidence",{"page":"dynamic"})),
            response(("finish_report",report(True)))]
        with tempfile.TemporaryDirectory() as folder, patch.object(ai_review,"call_api",side_effect=replies), patch.object(ai_review.time,"sleep"), patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder);ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["review_status"],"completed")
            self.assertEqual(len(outcome["attempts"]),5)
            self.assertEqual(outcome["limits"]["transport_retry_allowance"],2)

    def test_transport_retry_allowance_is_bounded(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(ai_review,"call_api",side_effect=RuntimeError("API failure: TimeoutError")) as api, patch.object(ai_review.time,"sleep"), patch.dict("os.environ",{"AI_DEFAULT_PROFILE":"backup"}):
            root=self.root(folder)
            with self.assertRaises(RuntimeError):ai_review.run(root)
            self.assertEqual(api.call_count,10)
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["status"],"failed")

    def test_review_journal_is_bounded_but_keeps_locator_fields(self):
        journal=[{"id":"E001","tool":"page_evidence","args":{"page":"comment"},"result":{"blob":"x"*9000}},
                 {"id":"E002","tool":"page_evidence","args":{"page":"dynamic"},"result":{"small":"ok"}}]
        rows=ai_review.bounded_journal(journal)
        self.assertEqual([r["id"] for r in rows],["E001","E002"])
        self.assertEqual(rows[0]["args"],{"page":"comment"})
        self.assertTrue(rows[0]["result"]["truncated"])
        self.assertLessEqual(len(rows[0]["result"]["excerpt"]),ai_review.REVIEW_EXCERPT_CHARS)
        self.assertEqual(rows[1]["result"],{"small":"ok"})

    def test_missing_path_or_changed_static_status_is_rejected(self):
        for change in ("missing","status"):
            value=report()
            path=value["pages"][0]["path_reviews"]
            if change=="missing":path.clear()
            else:path[0]["status"]="adapted"
            with self.assertRaises(RuntimeError):
                ai_review.validate_report(value,{"E000","E001"},["comment","dynamic"],summary()["page_path_matrix"])

    def test_old_reads_cannot_satisfy_independent_review(self):
        evidence=ai_review.Evidence(Path("."),summary())
        evidence.ids.update({"E001","E002","E003"})
        evidence.journal=[{"id":"E002","tool":"page_evidence","args":{"page":"comment"}},
                          {"id":"E003","tool":"page_evidence","args":{"page":"dynamic"}}]
        draft=report();draft["findings"][0]["finding_id"]="F001"
        with self.assertRaises(RuntimeError):
            ai_review.validate_review(report(True),draft,evidence,["comment","dynamic"],2)

    def test_rejected_finding_cannot_remain_in_final_report(self):
        evidence=ai_review.Evidence(Path("."),summary());evidence.ids.update({"E001","E002","E003"})
        evidence.journal=[{"id":"E002","tool":"page_evidence","args":{"page":"comment"}},
                          {"id":"E003","tool":"page_evidence","args":{"page":"dynamic"}}]
        draft=report();draft["findings"][0]["finding_id"]="F001"
        final=report(True);final["review"]["findings"][0]["disposition"]="rejected"
        with self.assertRaisesRegex(RuntimeError,"implement review dispositions"):
            ai_review.validate_review(final,draft,evidence,["comment","dynamic"],0)

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
        evidence=ai_review.Evidence(Path("."),summary());evidence.ids.update({"E001","E002","E003"})
        draft=report();draft["findings"][0]["finding_id"]="F001"
        final=report(True);final["findings"][0]["level"]="static_evidence"
        with self.assertRaisesRegex(RuntimeError,"remain uncertain"):
            ai_review.validate_review(final,draft,evidence,["comment","dynamic"],0)


if __name__=="__main__":
    unittest.main()
