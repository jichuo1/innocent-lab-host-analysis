"""Audit failures stay closed; subprocess resource limits also clean grandchildren."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from unittest.mock import patch

import analyze
import ai_review
from analysis.run_intake import EXPECTED_FEATURES
import hostlab
import priority_analysis
import process_control
import runner_resources


class HeapBudgetTest(unittest.TestCase):
    def budget(self, available):
        with patch.object(runner_resources.platform, "system", return_value="Linux"), \
             patch.object(runner_resources, "linux_raw", return_value={"memory_available_bytes": available}):
            return runner_resources.audit_heap_mib()

    def test_large_runner_is_capped(self):
        self.assertEqual(self.budget(64 * runner_resources.GIB), 8192)

    def test_small_runner_keeps_native_headroom(self):
        self.assertEqual(self.budget(4 * runner_resources.GIB), 2048)

    def test_unknown_telemetry_keeps_bounded_fallback(self):
        self.assertEqual(self.budget(None), 4096)

    def test_exhausted_or_too_small_runner_fails_before_jvm(self):
        for available in (0, runner_resources.GIB, 3 * runner_resources.GIB - 1):
            with self.subTest(available=available), self.assertRaisesRegex(RuntimeError, "Insufficient"):
                self.budget(available)


class ProcessTest(unittest.TestCase):
    def test_nonzero_exit_is_preserved_and_output_goes_to_file(self):
        with tempfile.TemporaryFile() as output:
            rc = process_control.run([sys.executable, "-c", "print('evidence');raise SystemExit(7)"],
                                     stdout=output, timeout=10)
            output.seek(0)
            self.assertEqual(rc, 7)
            self.assertIn(b"evidence", output.read())

    def test_missing_executable_fails(self):
        with tempfile.TemporaryFile() as output, self.assertRaises(FileNotFoundError):
            process_control.run(["hostlab-no-such-executable"], stdout=output, timeout=1)

    def test_deadline_kills_grandchild_before_it_can_write(self):
        with tempfile.TemporaryDirectory() as folder:
            sentinel = Path(folder) / "orphan.txt"
            child = "import time;from pathlib import Path;time.sleep(3);Path(" + repr(str(sentinel)) + ").write_text('orphan')"
            # Include a separate session on Linux, as nested managed audits use one.
            parent = ("import subprocess,sys,time;subprocess.Popen([sys.executable,'-c'," + repr(child) +
                      "],start_new_session=" + repr(os.name != "nt") + ");print('started',flush=True);time.sleep(60)")
            with tempfile.TemporaryFile() as output:
                self.assertEqual(process_control.run([sys.executable, "-c", parent], stdout=output, timeout=1), 124)
                output.seek(0)
                self.assertIn(b"started", output.read())
            time.sleep(3)
            self.assertFalse(sentinel.exists(), "grandchild survived audit timeout")

    def test_high_output_does_not_fill_a_pipe(self):
        with tempfile.TemporaryFile() as output:
            self.assertEqual(process_control.run([sys.executable, "-c", "import sys;sys.stdout.write('x'*2000000)"],
                                                 stdout=output, timeout=10), 0)
            self.assertEqual(output.tell(), 2000000)


class AuditEvidenceTest(unittest.TestCase):
    def invoke(self, report=None, rc=0, *, stale=False):
        sample = {"version_code": 1, "sha256": "a"*64}
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab, "STATE", Path(folder)):
            root = Path(folder) / "reports/1" / ("a"*16)
            if stale:
                old = root / "old/summary.json"
                old.parent.mkdir(parents=True)
                old.write_text(json.dumps(self.report()))
            def audit(_):
                if report is not None:
                    path = root / "new/summary.json"
                    path.parent.mkdir(parents=True)
                    path.write_text(json.dumps(report))
                return rc
            with patch.object(analyze, "main", side_effect=audit):
                return priority_analysis.audit_sample(sample, "b"*40)

    def report(self):
        return {"audit_complete": True, "sample": {"sha256": "a"*64, "revision": "b"*40},
                "features": {key: {"status": "FOUND"} for key in EXPECTED_FEATURES}}

    def test_complete_negative_findings_still_reach_review(self):
        report = self.report()
        report["features"][EXPECTED_FEATURES[0]]["status"] = "MISSING"
        self.assertEqual(self.invoke(report, rc=1)["exit_code"], 1)

    def test_empty_partial_timed_out_or_mismatched_evidence_never_passes(self):
        reports = [self.report() for _ in range(5)]
        reports[0]["features"] = {}
        reports[1]["features"].pop(EXPECTED_FEATURES[-1])
        reports[2]["audit_complete"] = False
        reports[3]["sample"]["sha256"] = "f"*64
        reports[4]["sample"]["revision"] = "c"*40
        for report, rc in [*( (r, 0) for r in reports), (self.report(), 124), (self.report(), -9)]:
            with self.subTest(report=report, rc=rc), self.assertRaisesRegex(RuntimeError, "FEATURE evidence"):
                self.invoke(report, rc=rc)

    def test_stale_report_is_not_reused_after_failure(self):
        with self.assertRaisesRegex(RuntimeError, "FEATURE evidence"):
            self.invoke(stale=True, rc=1)


class ScanAdmissionTest(unittest.TestCase):
    def test_missing_duplicate_or_broken_dex_inventory_fails_before_workers(self):
        with tempfile.TemporaryDirectory() as folder:
            apk = Path(folder) / "sample.apk"
            with zipfile.ZipFile(apk, "w"):
                pass
            with patch.object(priority_analysis, "ProcessPoolExecutor") as pool:
                with self.assertRaisesRegex(RuntimeError, "DEX inventory"):
                    priority_analysis.scan_apk(apk, {})
                with zipfile.ZipFile(apk, "w") as archive:
                    archive.writestr("classes.dex", b"fixture")
                    with self.assertWarns(UserWarning):
                        archive.writestr("classes.dex", b"duplicate")
                with self.assertRaisesRegex(RuntimeError, "DEX inventory"):
                    priority_analysis.scan_apk(apk, {})
                apk.write_bytes(b"broken archive")
                with self.assertRaises(zipfile.BadZipFile):
                    priority_analysis.scan_apk(apk, {})
                pool.assert_not_called()

    def test_low_or_unknown_memory_reduces_parallelism_without_skipping_dex(self):
        with tempfile.TemporaryDirectory() as folder:
            apk = Path(folder) / "sample.apk"
            with zipfile.ZipFile(apk, "w") as archive:
                archive.writestr("classes.dex", b"fixture1")
                archive.writestr("classes2.dex", b"fixture2")
            for memory, cpus, expected in ((None, 8, 1), (2*runner_resources.GIB, 8, 1),
                                           (8*runner_resources.GIB, 8, 2), (8*runner_resources.GIB, 1, 1)):
                with self.subTest(memory=memory, cpus=cpus), \
                     patch.object(runner_resources.Probe, "collect", return_value={
                         "memory_available_bytes": memory, "effective_cpus": cpus}), \
                     patch.object(priority_analysis, "ProcessPoolExecutor") as factory:
                    pool = factory.return_value.__enter__.return_value
                    pool.map.return_value = []
                    result = priority_analysis.scan_apk(apk, {})
                    self.assertEqual(factory.call_args.kwargs["max_workers"], expected)
                    self.assertEqual(len(pool.map.call_args.args[1]), 2)
                    self.assertEqual(result["scan_execution"]["dex_files"], 2)


class AiDecompileTest(unittest.TestCase):
    def invoke(self, rc, write_new):
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab, "STATE", Path(folder)):
            evidence = ai_review.Evidence(Path(folder), {})
            evidence.data["target"] = {"sample": {"version_code": 1, "sha256": "a"*64, "revision": "b"*40},
                                       "class_records": [{"class": "Lexample/Actual;"}], "invoke_edges": []}
            reports = Path(folder) / "reports/1" / ("a"*16)
            old = reports / "old/class.java"
            old.parent.mkdir(parents=True)
            old.write_text("stale source")
            def run(command, *, stdout, timeout):
                self.assertEqual(timeout, 150)
                self.assertEqual(stdout, subprocess.DEVNULL)
                self.assertEqual(command[command.index("--revision")+1], "b"*40)
                if write_new:
                    new = reports / "new/class.java"
                    new.parent.mkdir(parents=True)
                    new.write_text("current source")
                return rc
            with patch.object(process_control, "run", side_effect=run):
                return evidence.run_tool("decompile_class", {"class_name": "example.Actual"})

    def test_decompile_reads_only_current_successful_output(self):
        self.assertEqual(self.invoke(0, True)["source"], "current source")

    def test_timeout_nonzero_and_missing_output_cannot_reuse_old_source(self):
        for rc, write_new in ((124, False), (1, True), (0, False)):
            with self.subTest(rc=rc, write_new=write_new), self.assertRaisesRegex(RuntimeError, "decompile failed"):
                self.invoke(rc, write_new)


if __name__ == "__main__":
    unittest.main()
