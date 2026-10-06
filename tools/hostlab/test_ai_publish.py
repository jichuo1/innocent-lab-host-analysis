import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import ai_review
import publish_report


class AiBoundaryTest(unittest.TestCase):
    def report(self):
        return {"overview":"建议复核","pages":[{"page":"comment","assessment":"待核验","evidence_ids":["E000"]}],
                "findings":[],"next_steps":["真机验证"]}

    def test_invented_evidence_is_rejected(self):
        value=self.report()
        value["pages"][0]["evidence_ids"]=["E999"]
        with self.assertRaises(RuntimeError):
            ai_review.validate_report(value,{"E000"},["comment"])

    def test_missing_page_is_rejected(self):
        with self.assertRaises(RuntimeError):
            ai_review.validate_report(self.report(),{"E000"},["comment","dynamic"])

    def test_secret_is_redacted(self):
        with patch.dict("os.environ",{"AI_API_KEY_PRIMARY":"private-test-value"}):
            self.assertNotIn("private-test-value",ai_review.redact("echo private-test-value"))

    def test_model_cannot_read_arbitrary_file(self):
        evidence=ai_review.Evidence(Path("."),{"source_snapshot":{"source_records":[]}})
        with self.assertRaises(RuntimeError):
            evidence.execute("module_source",{"path":"../../.env"})

    def test_partial_ai_never_replaces_latest(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            out=root/"remote-output"
            out.mkdir()
            data={"sample":{"version_code":1,"version_name":"test","sha256":"a"*64},
                  "changes":[],"analysis_status":"REVIEW_REQUIRED","ai_status":"failed", "ai_review":{"status":"failed"}}
            (out/"priority-summary.json").write_text(json.dumps(data),encoding="utf-8")
            (out/"priority-report.md").write_text("未完成",encoding="utf-8")
            entry,files,_,_=publish_report.prepare(root,"123","1")
            self.assertFalse(entry["complete"])
            self.assertFalse(any(path.endswith("latest.json") for path in files))

    def test_compact_summary_omits_raw_source(self):
        value={"changes":[],"source_snapshot":{"source_records":[{"path":"a.kt","sha256":"hash","source":"raw private source"}]}}
        self.assertNotIn("raw private source",json.dumps(publish_report.compact(value)))


if __name__=="__main__":
    unittest.main()
