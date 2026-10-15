"""Multi-version queue bounds, immutable bindings, crash recovery and comparisons."""
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import Mock,patch

import analysis_plan
import hostlab
import version_matrix as matrix


def samples(count=5):
    return [{"version_code":9000000+i,"apk_sha256":format(i+1,"064x"),"sample_revision":"c"*40} for i in range(count)]


def request():
    return {"backend":"dexsql","tasks":[{"id":"feature","operation":"locate","name":"getUrlsMap"}]}


class MatrixTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        p=patch.object(hostlab,"STATE",self.root);p.start();self.addCleanup(p.stop)
        self.head="a"*40
        self.jobs={};self.calls=[];self.keys={}
        p=patch.object(matrix.remote_schedule,"submit",side_effect=self.submit);p.start();self.addCleanup(p.stop)

    def gh(self,*args,**kwargs):
        return json.dumps({"object":{"sha":self.head}})

    def create(self,count=5,**kwargs):
        return matrix.create(samples(count),request(),self.gh,repository="owner/repo",**kwargs)

    def submit(self,code,spec,gh,lookup,runs,**kwargs):
        self.calls.append(kwargs)
        key=kwargs["idempotency_key"]
        if key in self.keys:
            rid=self.keys[key]
            run=self.jobs[rid]
            return {"request_id":rid,"status":run["status"],"conclusion":run.get("conclusion"),"reused":True}
        rid=format(len(self.keys)+1,"032x");self.keys[key]=rid
        self.jobs[rid]={"id":len(self.keys),"status":"queued","conclusion":None,"html_url":"https://example.invalid/"+rid}
        return {"request_id":rid,"status":"submitted","reused":False}

    def advance(self,identifier,**kwargs):
        return matrix.advance(identifier,self.gh,self.jobs.get,lambda:[],repository="owner/repo",workflow="host-analysis.yml",**kwargs)

    def complete(self):
        for job in self.jobs.values(): job.update(status="completed",conclusion="success")

    def test_plan_deduplicates_exact_samples_and_rejects_unbounded_or_unpinned_work(self):
        result=matrix.plan(samples(2)+samples(1),request())
        self.assertEqual(result["sample_count"],2)
        self.assertEqual(result["duplicate_samples_removed"],1)
        for rows,parallel in [(samples(41),4),([{"version_code":1}],4),(samples(1),5),(samples(1),True)]:
            with self.subTest(parallel=parallel),self.assertRaises(ValueError): matrix.plan(rows,request(),parallel)

    def test_real_feature_scenario_has_explicit_dialects_and_bounded_tasks(self):
        scenario=json.loads((Path(__file__).parent/"examples/comment-search-links.json").read_text(encoding="utf-8"))
        normalized=analysis_plan.validate(scenario)
        self.assertEqual(normalized["backend"],"dexsql")
        self.assertEqual(len(normalized["tasks"]),15)
        self.assertTrue(all(t["dialect"]=="dexsql" for t in normalized["tasks"] if t["operation"]=="query"))

    def test_github_pending_is_inflight_and_cannot_overfill_the_pool(self):
        created=self.create(max_parallel=2)
        first=self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),2)
        for job in self.jobs.values(): job["status"]="pending"
        second=self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),2)
        self.assertEqual(second["counts"]["queued_local"],3)
        self.assertEqual(second["peak_inflight"],2)

    def test_one_queue_snapshot_refreshes_all_active_versions_without_per_job_polling(self):
        created=self.create(max_parallel=2)
        self.advance(created["matrix_id"])
        rows=[{**job,"display_title":"hostlab-"+rid} for rid,job in self.jobs.items()]
        runs=Mock(return_value=rows);lookup=Mock(side_effect=AssertionError("unnecessary individual poll"))
        matrix.advance(created["matrix_id"],self.gh,lookup,runs,repository="owner/repo",workflow="host-analysis.yml")
        runs.assert_called_once();lookup.assert_not_called()

    def test_completed_slots_are_replenished_and_all_versions_are_retained(self):
        created=self.create(max_parallel=4)
        self.advance(created["matrix_id"]);state=self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),4)
        self.assertEqual(state["peak_inflight"],4)
        self.complete();self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),5)
        self.complete();state=self.advance(created["matrix_id"])
        self.assertTrue(state["finished"] and state["complete"])

    def test_capacity_backpressure_keeps_local_queue_intact(self):
        created=self.create(count=2)
        with patch.object(matrix.remote_schedule,"submit",return_value={"status":"capacity_full"}):
            state=self.advance(created["matrix_id"])
        self.assertEqual(state["counts"],{"queued_local":2})
        self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),2)

    def test_unknown_dispatch_is_not_replayed_and_occupies_its_slot(self):
        created=self.create(count=2,max_parallel=1)
        with patch.object(matrix.remote_schedule,"submit",return_value={"request_id":"d"*32,"status":"dispatch_unknown"}) as submit:
            self.advance(created["matrix_id"]);state=self.advance(created["matrix_id"])
        self.assertEqual(submit.call_count,1)
        self.assertEqual(state["counts"]["queued_local"],1)
        self.assertFalse(state["finished"])

    def test_crash_after_fast_completion_cannot_create_a_second_paid_job(self):
        created=self.create(count=1,reuse_completed=False)
        def crashed(*args,**kwargs):
            self.submit(*args,**kwargs)
            self.complete()
            raise SystemExit("caller crashed before persisting matrix entry")
        with patch.object(matrix.remote_schedule,"submit",side_effect=crashed),self.assertRaises(SystemExit):
            self.advance(created["matrix_id"])
        state=self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),1)
        self.assertTrue(state["complete"])
        self.assertEqual(self.calls[0]["idempotency_key"],self.calls[1]["idempotency_key"])

    def test_all_versions_keep_the_original_tool_commit_after_main_moves(self):
        created=self.create(max_parallel=2)
        self.head="b"*40
        self.advance(created["matrix_id"]);self.complete();self.advance(created["matrix_id"])
        self.assertTrue(all(c["runner_revision"]=="a"*40 for c in self.calls))

    def test_explicit_key_resumes_same_matrix_without_rebinding_source(self):
        first=self.create(count=2,idempotency_key="feature1")
        self.head="b"*40
        second=self.create(count=2,idempotency_key="feature1")
        self.assertEqual(first["matrix_id"],second["matrix_id"])
        self.assertEqual(second["runner_revision"],"a"*40)
        with self.assertRaises(ValueError): self.create(count=3,idempotency_key="feature1")

    def test_fresh_loads_have_distinct_keys_and_do_not_hit_completed_caches(self):
        first=self.create(count=1,reuse_completed=False)
        second=self.create(count=1,reuse_completed=False)
        a=matrix.load(first["matrix_id"])["entries"][0]["dispatch_key"]
        b=matrix.load(second["matrix_id"])["entries"][0]["dispatch_key"]
        self.assertNotEqual(a,b)
        cached1=self.create(count=1);cached2=self.create(count=1)
        self.assertEqual(matrix.load(cached1["matrix_id"])["entries"][0]["dispatch_key"],matrix.load(cached2["matrix_id"])["entries"][0]["dispatch_key"])

    def test_deadline_stops_new_dispatch_without_cancelling_accepted_work(self):
        created=self.create(count=2,max_parallel=1)
        self.advance(created["matrix_id"])
        with patch.object(matrix.time,"time",return_value=created["deadline_at"]+1):
            state=self.advance(created["matrix_id"])
        self.assertEqual(len(self.keys),1)
        self.assertEqual(state["counts"]["skipped"],1)
        self.assertFalse(state["finished"])

    def test_definition_tampering_fails_before_new_dispatch(self):
        created=self.create(count=1)
        value=matrix.load(created["matrix_id"]);value["definition"]["max_parallel"]=1
        hostlab.write_json(matrix.path(created["matrix_id"]),value)
        with self.assertRaises(ValueError): self.advance(created["matrix_id"])
        self.assertEqual(self.calls,[])

    def test_tool_and_sample_bindings_cannot_drift_in_a_saved_queue(self):
        for kind in ("tool","sample","retry"):
            created=self.create(count=1)
            value=matrix.load(created["matrix_id"])
            if kind=="tool": value["runner_revision"]="f"*40
            elif kind=="sample": value["entries"][0]["sample"]["apk_sha256"]="f"*64
            else: value["entries"][0]["dispatch_key"]="different"
            hostlab.write_json(matrix.path(created["matrix_id"]),value)
            with self.subTest(kind=kind),self.assertRaises(ValueError): self.advance(created["matrix_id"])
        self.assertEqual(self.calls,[])

    def test_structure_layout_hash_excludes_dex_repacking_but_detects_field_changes(self):
        original={"columns":["file_id","descriptor","field_layout"],"rows":[[1,"LReply;","a:I\nb:Ljava/lang/String;"]]}
        repacked={"columns":original["columns"],"rows":[[30,"LReply;","a:I\nb:Ljava/lang/String;"]]}
        changed={"columns":original["columns"],"rows":[[30,"LReply;","a:J\nb:Ljava/lang/String;"]]}
        self.assertEqual(matrix.attributes(original)[0],matrix.attributes(repacked)[0])
        self.assertNotEqual(matrix.attributes(original)[0],matrix.attributes(changed)[0])

    def test_comparison_uses_descriptors_not_dex_layout_and_checks_source_identity(self):
        created=self.create(count=2)
        self.advance(created["matrix_id"]);self.complete();self.advance(created["matrix_id"])
        state=matrix.load(created["matrix_id"])
        mapping={}
        for i,entry in enumerate(state["entries"]):
            out=self.root/str(i);out.mkdir()
            output={"complete":True,"tasks":[{"id":"feature","status":"complete","backend":"dexsql","result":{
                "partial":False,"identities":[{"descriptor":"LReply;->getUrlsMap()Ljava/util/Map;","file_id":i,"entry_name":f'classes{i+1}.dex'}]}}]}
            metadata={"operation":"batch","version_code":entry["sample"]["version_code"],"apk_sha256":entry["sample"]["apk_sha256"],
                "sample_revision":entry["sample"]["sample_revision"],"runner_revision":state["runner_revision"],
                "request_sha256":analysis_plan.fingerprint(state["definition"]["request"])}
            hostlab.write_json(out/"result.txt",output);hostlab.write_json(out/"job.json",metadata)
            mapping[entry["request_id"]]=json.dumps({"files":[str(out/"result.txt"),str(out/"job.json")]})
        report=matrix.compare(created["matrix_id"],mapping.__getitem__)
        difference=report["versions"][1]["tasks"]["feature"]["vs_first_version"]
        self.assertEqual(difference["added"],{})
        self.assertEqual(difference["removed"],{})
        metadata["apk_sha256"]="f"*64;hostlab.write_json(out/"job.json",metadata)
        with self.assertRaises(ValueError): matrix.compare(created["matrix_id"],mapping.__getitem__)


if __name__=="__main__": unittest.main()
