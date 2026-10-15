"""Offline source identity checks across runner, model evidence, reports and regeneration."""
import base64
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import ai_review
import auto_intake
import hostlab
import priority_analysis
import publish_report
import regenerate_report
import remote_job
import snapshot_transport
import source_snapshot


def frozen_source(label="original"):
    raw=("package fake\n// private source " + label + "\nclass CommentFeature\n").encode()
    record={"path":source_snapshot.SOURCE_PREFIX+"fake/CommentFeature.kt", "sha256":hashlib.sha256(raw).hexdigest(),
            "bytes":len(raw), "pages":["comment"], "markers":[], "source":raw.decode()}
    ctx={"schema":2,"selection_version":1,"captured_at":"2026-10-13T10:00:00Z","repository_head":"1"*40,
         "working_tree_dirty":True,"source_records":[record]}
    ctx["source_tree_sha256"]=source_snapshot._tree_identity(ctx["repository_head"],ctx["source_records"])
    sha=hashlib.sha256(source_snapshot.serialize(ctx)).hexdigest()
    binding={"schema":1,"repo":snapshot_transport.SOURCE_REPO,"revision":"2"*40,
             "path":"source-snapshots/"+sha+"/context.json","snapshot_sha256":sha,
             "source_tree_sha256":ctx["source_tree_sha256"],"repository_head":ctx["repository_head"],
             "captured_at":ctx["captured_at"],"verified_at":"2026-10-13T10:01:00Z","origin":"worktree",
             "working_tree_dirty":True,"file_count":1,"selection_version":1}
    return ctx,binding


def sample():
    return {"version_code":2,"version_name":"test","sha256":"a"*64,"revision":"b"*40}


def summary(ctx,binding):
    return {"sample":sample(),"baseline":None,"changes":[],"analysis_status":"REVIEW_REQUIRED",
            "ai_status":"failed","ai_review":{"status":"failed"},"runtime_verified":False,
            "limitations":["runtime unknown"],"page_path_matrix":{},"source_snapshot":source_snapshot.public_context(ctx,binding)}


class RunnerSourceTest(unittest.TestCase):
    def test_source_check_validates_private_payload_without_apk_scan_or_ai(self):
        ctx,binding=frozen_source()
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab,"STATE",Path(folder)), \
             patch.dict(os.environ,self.env("source_check"),clear=True), \
             patch.object(snapshot_transport,"load_for_analysis",return_value=(ctx,binding)), \
             patch.object(snapshot_transport,"cache_snapshot") as cache, \
             patch.object(hostlab,"api_private",side_effect=AssertionError("APK access")), \
             patch.object(remote_job.subprocess,"run",side_effect=AssertionError("scan")):
            self.assertEqual(remote_job.main(),0)
            job=json.loads((hostlab.STATE/"remote-output/job.json").read_text())
            self.assertEqual(job["scope"],"source_metadata_only")
            self.assertEqual(job["source_snapshot"]["binding"]["snapshot_sha256"],binding["snapshot_sha256"])
            self.assertNotIn("source",job["source_snapshot"]["source_records"][0])
            cache.assert_called_once_with(ctx,binding)

    def env(self,operation="multipath_audit"):
        return {"HOSTLAB_VERSION":"2","HOSTLAB_OPERATION":operation,"HOSTLAB_ARGUMENT":"",
                "HOSTLAB_REVISION":"b"*40,"HOSTLAB_SHA":"a"*64,"HOSTLAB_MAX_CELL_CHARS":"300"}

    def test_missing_source_stops_before_sample_access(self):
        with patch.dict(os.environ,self.env(),clear=True), \
             patch.object(snapshot_transport,"load_for_analysis",side_effect=RuntimeError("missing")), \
             patch.object(hostlab,"api_private") as sample_access, patch.object(remote_job.subprocess,"run") as run:
            with self.assertRaisesRegex(RuntimeError,"missing"):
                remote_job.main()
            sample_access.assert_not_called()
            run.assert_not_called()

    def test_damaged_source_stops_before_scan(self):
        ctx,binding=frozen_source();ctx["source_records"][0]["source"]="changed"
        with patch.dict(os.environ,self.env(),clear=True), \
             patch.object(snapshot_transport,"load_for_analysis",return_value=(ctx,binding)), \
             patch.object(hostlab,"api_private") as sample_access:
            with self.assertRaises(ValueError):remote_job.main()
            sample_access.assert_not_called()

    def test_query_does_not_load_module_source(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab,"STATE",Path(folder)), \
             patch.dict(os.environ,self.env("query"),clear=True), \
             patch.object(snapshot_transport,"load_for_analysis") as load, \
             patch.object(hostlab,"api_private",return_value=(None,"b"*40)), \
             patch.object(hostlab,"manifest",return_value={"samples":[sample()]}), \
             patch.object(hostlab,"select",return_value=sample()), \
             patch.object(hostlab,"write_json") as write, \
             patch.object(remote_job.subprocess,"run",return_value=SimpleNamespace(returncode=0)), \
             patch.object(remote_job.analyze,"tool_hashes",return_value={}):
            self.assertEqual(remote_job.main(),0)
            load.assert_not_called()
            job=write.call_args.args[1]
            self.assertNotIn("source_snapshot",job)

    def test_priority_direct_entry_requires_valid_source_before_resolve(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab,"STATE",Path(folder)), \
             patch.dict(os.environ,self.env(),clear=True), \
             patch.object(snapshot_transport,"load_for_analysis",side_effect=RuntimeError("missing")), \
             patch.object(priority_analysis,"resolve") as resolve:
            with self.assertRaises(RuntimeError):priority_analysis.main()
            resolve.assert_not_called()

    def test_priority_summary_has_public_source_identity(self):
        ctx,binding=frozen_source()
        target={"sample":sample(),"families":{},"unknown_families":[],"page_path_matrix":{},
                "protocol_paths":{},"protocol_twins":[],"unregistered_protocols":[],
                "unclassified_protocol_callers":[],"limitations":[]}
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab,"STATE",Path(folder)), \
             patch.dict(os.environ,self.env(),clear=True), \
             patch.object(snapshot_transport,"load_for_analysis",return_value=(ctx,binding)), \
             patch.object(priority_analysis,"resolve",return_value=(Path("fake.apk"),sample())), \
             patch.object(priority_analysis,"audit_sample",return_value={"features":[]}), \
             patch.object(priority_analysis,"scan_apk",return_value=target):
            priority_analysis.main()
            data=json.loads((Path(folder)/"remote-output/priority-summary.json").read_text())
            self.assertEqual(data["source_snapshot"]["binding"]["snapshot_sha256"],binding["snapshot_sha256"])
            self.assertEqual(data["source_snapshot"]["freshness"],"dispatch_worktree_snapshot")
            self.assertNotIn("private source",json.dumps(data))


class EvidenceSourceTest(unittest.TestCase):
    def test_module_source_identity_and_public_journal(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        evidence=ai_review.Evidence(Path("."),data)
        with patch.object(snapshot_transport,"load_pinned",return_value=ctx):
            result=evidence.run_tool("module_source",{"path":ctx["source_records"][0]["path"]})
        self.assertIn("private source",result["source"])
        self.assertEqual(result["source_snapshot"]["binding"],binding)
        self.assertEqual(result["source_snapshot"]["captured_at"],ctx["captured_at"])
        self.assertNotIn("private source",json.dumps(evidence.public_journal()))

    def test_escaped_source_trims_body_without_losing_identity_or_leaking_excerpt(self):
        ctx,binding=frozen_source()
        record=ctx["source_records"][0]
        record["source"]="private source sentry " + "\\\n" * 5000
        raw=record["source"].encode()
        record.update({"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
        ctx["source_tree_sha256"]=source_snapshot._tree_identity(ctx["repository_head"],ctx["source_records"])
        binding.update({"source_tree_sha256":ctx["source_tree_sha256"],
                        "snapshot_sha256":hashlib.sha256(source_snapshot.serialize(ctx)).hexdigest()})
        binding["path"]="source-snapshots/"+binding["snapshot_sha256"]+"/context.json"
        evidence=ai_review.Evidence(Path("."),summary(ctx,binding))
        with patch.object(snapshot_transport,"load_pinned",return_value=ctx):
            result=evidence.run_tool("module_source",{"path":record["path"]})
        self.assertTrue(result["truncated"])
        self.assertEqual(result["source_snapshot"]["binding"],binding)
        self.assertLessEqual(len(json.dumps(result,ensure_ascii=False)),14000)
        self.assertNotIn("private source sentry",json.dumps(evidence.public_journal()))

    def test_corrupt_pinned_context_stops_ai_before_api(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"priority-summary.json").write_text(json.dumps(data))
            (root/"priority-report.md").write_text("static")
            with patch.object(snapshot_transport,"load_pinned",side_effect=ValueError("corrupt cache")), \
                 patch.object(ai_review,"call_api") as api:
                with self.assertRaises(RuntimeError):ai_review.run(root)
                api.assert_not_called()
            outcome=json.loads((root/"ai-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(outcome["status"],"failed")
            self.assertIn("ValueError",outcome["error"])

    def test_mismatched_public_metadata_is_rejected(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        data["source_snapshot"]["working_tree_dirty"]=False
        with patch.object(snapshot_transport,"load_pinned",return_value=ctx):
            with self.assertRaisesRegex(RuntimeError,"metadata differs"):
                ai_review.Evidence(Path("."),data).module_context()

    def test_changed_public_file_manifest_is_rejected(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        data["source_snapshot"]["source_records"][0]["sha256"]="f"*64
        with patch.object(snapshot_transport,"load_pinned",return_value=ctx):
            with self.assertRaisesRegex(RuntimeError,"metadata differs"):
                ai_review.Evidence(Path("."),data).module_context()

    def test_e000_and_saved_ai_outcome_keep_source_identity_without_body(self):
        import ai_pipeline
        ctx,binding=frozen_source();data=summary(ctx,binding)
        data["page_path_matrix"]={}
        completed={"overview":"静态建议","pages":[],"findings":[],"next_steps":[],
                   "review":{"status":"completed","pages":[],"findings":[],"remaining_gaps":[]}}
        seed_seen=[]
        def collect(coordinator,stage,unit,messages,tools,evidence,validate,**kwargs):
            if stage=="draft":
                seed_seen.append(json.loads(messages[1]["content"])["seed"])
                evidence.run_tool("module_source",{"path":ctx["source_records"][0]["path"]})
                return {key:completed[key] for key in ("overview","pages","findings","next_steps")}
            return {"pages":[],"findings":[],"remaining_gaps":[]}
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"priority-summary.json").write_text(json.dumps(data))
            (root/"priority-report.md").write_text("static")
            with patch.object(snapshot_transport,"load_pinned",return_value=ctx), \
                 patch.object(ai_pipeline,"draft_units",return_value=[[]]), \
                 patch.object(ai_pipeline,"collect",side_effect=collect), \
                 patch.object(ai_review,"assemble_report",return_value=completed):
                ai_review.run(root)
            outcome=json.loads((root/"ai-analysis.json").read_text())
            evidence=json.loads((root/"ai-evidence.json").read_text())
            self.assertEqual(seed_seen[0]["source_snapshot"]["binding"],binding)
            self.assertEqual(evidence["E000"]["source_snapshot"]["binding"],binding)
            self.assertEqual(outcome["source_snapshot"]["binding"],binding)
            self.assertNotIn("private source",json.dumps(evidence))


class ReportSourceTest(unittest.TestCase):
    def test_report_index_and_bundle_preserve_identity_without_source(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);out=root/"remote-output";out.mkdir()
            (out/"priority-summary.json").write_text(json.dumps(data))
            (out/"priority-report.md").write_text("static")
            (out/"ai-evidence.json").write_text(json.dumps({"tools":[{"tool":"module_source","result":{"source":"private source body"}}]}))
            entry,files,_,assets=publish_report.prepare(root,"321","1")
            self.assertEqual(entry["source_snapshot"]["binding"],binding)
            report=next(text for path,text in files.items() if path.endswith("report.md"))
            self.assertIn(binding["snapshot_sha256"],report)
            self.assertIn(ctx["captured_at"],report)
            with zipfile.ZipFile(assets[0]) as archive:
                self.assertNotIn("private source", "".join(archive.read(n).decode() for n in archive.namelist()))

    def test_legacy_metadata_remains_readable_and_labeled(self):
        data={"changes":[],"source_snapshot":{"repository_head":"old","source_records":[{"path":"old.kt","sha256":"oldhash","source":"private source"}]}}
        compact=publish_report.compact(data)
        self.assertTrue(compact["source_snapshot"]["legacy"])
        self.assertIn("legacy",publish_report.source_note(data))
        self.assertNotIn("private source",json.dumps(compact))


class RegenerateSourceTest(unittest.TestCase):
    def test_verified_history_without_binding_cannot_downgrade_to_legacy(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        data["source_snapshot"].pop("binding")
        with patch.object(snapshot_transport,"load_for_analysis") as load:
            with self.assertRaisesRegex(RuntimeError,"binding is missing"):
                regenerate_report.review_source(data,"")
            load.assert_not_called()

    def run_regenerate(self,folder,data,explicit=None):
        state=Path(folder)
        source=state/"regenerate-input/987/remote-output";source.mkdir(parents=True)
        target={"sample":data["sample"], "rule_sha256":"c"*64, "page_path_matrix":data["page_path_matrix"],
                "unknown_families":[], "unregistered_protocols":[]}
        for name,value in (("priority-summary.json",data),("priority-target.json",target),
                           ("job.json",{"version_code":2,"operation":"multipath_audit","exit_code":0,
                                        "sample_revision":"b"*40,"apk_sha256":"a"*64})):
            (source/name).write_text(json.dumps(value))
        (source/"priority-report.md").write_text("static\n# AI 适配分析\nold review")
        env={"HOSTLAB_ARGUMENT":"987","HOSTLAB_VERSION":"2","HOSTLAB_MODULE_SOURCE":explicit or ""}
        run={"id":987,"run_attempt":1,"head_sha":"d"*40,"conclusion":"failure"}
        downloaded={"root":str(source.parent), "files":[str(p) for p in source.iterdir()],
                    "artifact":{"id":1,"digest":"sha256:"+"f"*64}, "cache_hit":True}
        with patch.object(hostlab,"STATE",state), patch.object(hostlab,"CONFIG",state/"config.json"), \
             patch.dict(os.environ,env,clear=True), patch.object(regenerate_report,"verified_artifact",return_value=(run,downloaded)):
            regenerate_report.main()
        return json.loads((state/"remote-output/priority-summary.json").read_text())

    def test_default_retains_original_binding_and_historical_static_run(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(snapshot_transport,"load_for_analysis",return_value=(ctx,binding)) as load, \
             patch.object(snapshot_transport,"cache_snapshot"):
            actual=self.run_regenerate(folder,data)
            self.assertEqual(json.loads(load.call_args.args[0]),binding)
            self.assertEqual(actual["source_snapshot"]["binding"],binding)
            self.assertEqual(actual["source_snapshot"]["freshness"],"historical")
            self.assertEqual(actual["regenerated_from_run"],987)
            self.assertEqual(actual["static_evidence_run"],987)
            self.assertFalse(actual["source_rebound_for_review"])

    def test_explicit_new_source_keeps_original_static_evidence_run(self):
        ctx,binding=frozen_source();new_ctx,new_binding=frozen_source("new")
        data=summary(ctx,binding);data["static_evidence_run"]=456
        with tempfile.TemporaryDirectory() as folder, \
             patch.object(snapshot_transport,"load_for_analysis",return_value=(new_ctx,new_binding)), \
             patch.object(snapshot_transport,"cache_snapshot"):
            actual=self.run_regenerate(folder,data,json.dumps(new_binding))
            self.assertEqual(actual["source_snapshot"]["binding"],new_binding)
            self.assertEqual(actual["static_evidence_run"],456)
            self.assertEqual(actual["regenerated_from_run"],987)
            self.assertTrue(actual["source_rebound_for_review"])
            self.assertIn("只重新执行 AI",publish_report.source_note(actual))

    def test_legacy_source_moves_to_private_cache_and_is_labeled(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        data["source_snapshot"]={k:v for k,v in ctx.items() if k not in {"schema","selection_version","source_tree_sha256","captured_at"}}
        with tempfile.TemporaryDirectory() as folder, patch.object(snapshot_transport,"load_for_analysis") as load:
            actual=self.run_regenerate(folder,data)
            load.assert_not_called()
            self.assertNotIn("private source",json.dumps(actual))
            with patch.object(hostlab,"STATE",Path(folder)):
                result=ai_review.Evidence(Path(folder)/"remote-output",actual).run_tool("module_source",{"path":ctx["source_records"][0]["path"]})
            self.assertEqual(result["source_status"],"legacy_not_current")
            self.assertIn("private source",result["source"])

    def test_second_legacy_review_without_private_cache_keeps_historical_gap(self):
        ctx,binding=frozen_source();data=summary(ctx,binding)
        data["source_snapshot"]={"schema":0,"legacy":True,"freshness":"historical",
                                 "legacy_cache_sha256":"f"*64,"source_records":[],"repository_head":"1"*40}
        with tempfile.TemporaryDirectory() as folder, patch.object(snapshot_transport,"load_for_analysis") as load:
            actual=self.run_regenerate(folder,data)
            self.assertEqual(actual["source_snapshot"]["source_availability"],"legacy_source_unavailable")
            self.assertIn("私有源码全文缓存缺失",publish_report.source_note(actual))
            with patch.object(hostlab,"STATE",Path(folder)), self.assertRaisesRegex(RuntimeError,"cache is unavailable"):
                ai_review.Evidence(Path(folder)/"remote-output",actual).module_context()
            load.assert_not_called()


class IntakeSourceTest(unittest.TestCase):
    def api(self,calls):
        state={"schema":1,"seen":[],"watermark":0,"jobs":{}}
        def answer(path,data=None,method=None):
            calls.append((path,data,method))
            if path.startswith("contents/") and method is None:
                return {"sha":"c"*40,"content":base64.b64encode(json.dumps(state).encode()).decode()}
            if path.startswith("actions/") and data is None:return {"workflow_runs":[]}
            return None
        return answer

    def test_source_unavailable_never_dispatches_or_marks_seen(self):
        calls=[]
        with patch.object(hostlab,"api_private",return_value=(None,"b"*40)), \
             patch.object(hostlab,"manifest",return_value={"samples":[sample()]}), \
             patch.object(auto_intake,"api",side_effect=self.api(calls)), \
             patch.object(snapshot_transport,"resolve_published",side_effect=RuntimeError("missing source")):
            with self.assertRaises(RuntimeError):auto_intake.main()
        self.assertFalse(any(data is not None for _,data,_ in calls))

    def test_dispatch_pins_only_published_source(self):
        _,binding=frozen_source();binding["origin"]="published";calls=[]
        with patch.object(hostlab,"api_private",return_value=(None,"b"*40)), \
             patch.object(hostlab,"manifest",return_value={"samples":[sample()]}), \
             patch.object(auto_intake,"api",side_effect=self.api(calls)), \
             patch.object(snapshot_transport,"resolve_published",return_value=binding):
            auto_intake.main()
        dispatched=next(data for path,data,_ in calls if path.endswith("dispatches"))
        self.assertEqual(json.loads(dispatched["inputs"]["module_source"]),binding)
        self.assertEqual(dispatched["inputs"]["source_revision"],"b"*40)
        written=next(data for _,data,method in calls if method=="PUT")
        state=json.loads(base64.b64decode(written["content"]))
        self.assertEqual(state["source_freshness"],"published_unverified_worktree")
        self.assertEqual(state["seen"],["a"*64])


if __name__=="__main__":
    unittest.main()
