"""Native audits retain exact evidence, bounded transport and fail-closed gates."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import subprocess
import unittest
from unittest.mock import MagicMock, patch

import analyze
from analysis.run_intake import EXPECTED_FEATURES
import hostlab
import native_audit
from native_graph import Graph, Method, Type, UnsupportedAudit, field_type, method_types, parse_type
from native_rules import CATALOG, HERE, Rules
from native_session import literal
from native_surface import code_locations, legacy_body_order, prefix
import plan_ci
import verify_audits
import remote_job


def complete():
    return {"features": {name: {"status": "FOUND", "detail": "fixture"} for name in EXPECTED_FEATURES},
            "discoveries": {}, "complete": True, "source_sha_reverified": True, "class_count": 1,
            "surface": {"fixture": True},
            "gates": {"gate_mode": "mdd_fact_reuse", "drift": ([], [], []), "home": {}, "home_log": "======== sample.apk\n"}}


class RuleContractTest(unittest.TestCase):
    def test_catalog_is_bound_to_exact_canonical_reference(self):
        source = (HERE/"analysis/HostCompatibilityAudit.java").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha256(source.encode()).hexdigest(), CATALOG["reference_sha256"])
        for values in CATALOG["lists"].values():
            self.assertTrue(values)
            self.assertTrue(all('"'+v+'"' in source for v in values))
        methods = list(re.finditer(r'^    (?:private|public)[^\n]+? (\w+)\(', source, re.M))
        actual = {}
        for i, match in enumerate(methods):
            section = source[match.start():methods[i+1].start() if i+1 < len(methods) else len(source)]
            for array in re.finditer(r'(?:List|Set)<String> (\w+) = (?:List|Set)\.of\((.*?)\);', section, re.S):
                if not re.sub(r'"(?:[^"\\]|\\.)*"|[\s,]', '', array[2]):
                    actual[match[1]+"."+array[1]] = re.findall(r'"([^"\\]*)"', array[2])
        self.assertEqual(actual, CATALOG["lists"])

    def test_reference_drift_stops_native_before_opening_graph(self):
        with patch.dict(CATALOG, reference_sha256="0"*64), patch("native_rules.Graph") as graph:
            with self.assertRaisesRegex(UnsupportedAudit, "reference changed"):
                Rules(None)
            graph.assert_not_called()

    def test_generics_arrays_type_variables_wildcards_and_inner_classes(self):
        value, end = parse_type("Ljava/util/List<+Lexample/Outer.Inner<TT;>;>;")
        self.assertEqual(str(value), "java.util.List<? extends example.Outer$Inner<T>>")
        self.assertEqual(end, 45)
        args, result = method_types("<T:Ljava/lang/Object;>([ITT;Ljava/util/List<*>;)TT;^Ljava/lang/Exception;")
        self.assertEqual(list(map(str, args)), ["int[]", "T", "java.util.List<?>"])
        self.assertEqual(str(result), "T")

    def test_malformed_signatures_fail_instead_of_approximating(self):
        for value in ("", "T", "T;", "Ljava/util/List<", "Lexample/Type", "Q"):
            with self.subTest(value=value), self.assertRaises(UnsupportedAudit): parse_type(value)
        for value in ("(I", "(I)", "()Vjunk", "<T:Ljava/lang/Object;(I)V"):
            with self.subTest(value=value), self.assertRaises(UnsupportedAudit): method_types(value)
        for value in ("Ljava/util/List<Ljava/lang/String;>;junk", "Lexample/Outer<TT;>.Inner;"):
            with self.subTest(value=value), self.assertRaises(UnsupportedAudit): field_type(value)

    def test_shared_signature_sets_keep_every_owner_and_use_string_pool(self):
        class Session:
            def all(self, sql): return list(self.rows(sql))
            def rows(self, sql):
                if "annotation_directory_entries" in sql:
                    return iter([{"file_id":"7", "entry_kind":"field", "entry_idx":str(i), "annotation_set_off":"30"} for i in (1, 2)])
                if "annotation_set_entries" in sql:
                    return iter([{"file_id":"7", "annotation_set_off":"30", "annotation_off":"40"}])
                if "FROM annotations" in sql:
                    return iter([{"file_id":"7", "annotation_off":"40", "type_idx":"8"}])
                if "annotation_elements" in sql:
                    return iter([{"file_id":"7", "annotation_off":"40", "ordinal":"0", "value_index":"90"}])
                if "FROM strings" in sql:
                    assert "string_pool_id=3" in sql
                    return iter([{"string_pool_id":"3", "string_idx":"90", "value":"Ljava/util/List<Lexample/Item;>;"}])
                raise AssertionError(sql)
        graph = Graph.__new__(Graph)
        graph.session, graph.pools, graph.signature_ids = Session(), {7: 3}, {7: 8}
        values = graph.signatures([{"file_id": 7, "class_idx": 1}])
        self.assertEqual(values[(7, "field", 1)], values[(7, "field", 2)])

    def test_inheritance_cycles_are_bounded_and_methods_are_not_reloaded(self):
        graph = Graph.__new__(Graph)
        method = Method("Base", "get", "()I", [], Type("int"), 1, 0, 1)
        graph.classes = {"Child": {"super":"Base", "interfaces":[], "members":True, "methods":[]},
                         "Base": {"super":"Child", "interfaces":[], "members":True, "methods":[method]}}
        self.assertEqual(graph.methods(["Child"], inherited=True), [method])
        self.assertFalse(graph.subclass("Child", "Absent"))

    def test_fingerprint_order_uses_legacy_spaced_argument_descriptors(self):
        a, b = "(ILx;)V", "(I[Ljava/lang/String;)V"
        self.assertLess(a, b)
        self.assertEqual(legacy_body_order(a), "(I Lx;)V")
        self.assertEqual(legacy_body_order(b), "(I [Ljava/lang/String;)V")
        with self.assertRaises(UnsupportedAudit): legacy_body_order("(Q)V")

    def test_sql_literals_and_like_wildcards_are_escaped(self):
        self.assertEqual(literal("O'Brien"), "'O''Brien'")
        self.assertIn(r"a\_b\%", prefix("name", "a_b%"))
        for value in ("x\ny", "x\ry", "x\0y"):
            with self.assertRaises(ValueError): literal(value)

    def test_code_locations_filter_is_bounded_file_local_and_preserves_units(self):
        statements = []
        class Session:
            def rows(self, sql, **bounds):
                statements.append(sql)
                lower, upper = map(int, re.search(r"BETWEEN (\d+) AND (\d+)", sql).groups())
                indices = range(lower, upper+1)
                self_test.assertLess(len(sql.encode()), 256)
                return iter({"method_idx":str(i), "insns_off":str(i*4), "insns_size":"3"} for i in indices if i%2)
        self_test = self
        methods = {2: dict.fromkeys(range(17000)), 9: {1: None}}
        result = code_locations(Session(), methods)
        self.assertEqual(len(statements), 2)
        self.assertEqual(set(result), {(2,i) for i in range(17000) if i%2}|{(9,1)})
        self.assertEqual(result[(9,1)], (4,6))
        self.assertEqual(code_locations(Session(), {}), {})
        self.assertEqual(code_locations(Session(), {2:{}}), {})
        self.assertEqual(code_locations(Session(), {2:{1:None,5:None}}), {(2,1):(4,6), (2,5):(20,6)})

    def test_unrequested_code_item_cannot_enter_fingerprint_input(self):
        session = MagicMock()
        session.rows.return_value = [{"method_idx":"99", "insns_off":"4", "insns_size":"3"}]
        with self.assertRaisesRegex(RuntimeError, "requested method range"):
            code_locations(session, {1: {1: None}})


class CompletenessTest(unittest.TestCase):
    def test_reference_materializes_exact_source_only_without_checkout_changes(self):
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=hostlab.ROOT, text=True).strip()
        with tempfile.TemporaryDirectory() as folder:
            root, hashes = verify_audits.reference_tree(revision, Path(folder)/"reference")
            raw = subprocess.check_output(["git", "show", revision+":tools/hostlab/mdd_session.py"], cwd=hostlab.ROOT)
            self.assertEqual(hashes["tools/hostlab/mdd_session.py"], hashlib.sha256(raw).hexdigest())
            self.assertEqual((root/"tools/hostlab/mdd_session.py").read_bytes(), raw)
            self.assertTrue((root/"tools/hostlab/analysis/audit_catalog.json").is_file())
            self.assertTrue(all(Path(name).suffix in {".py", ".java", ".json"} for name in hashes))

    def test_reference_rejects_mutable_or_shell_like_input_before_git(self):
        for revision in ("main", "../other", "a"*39, "a"*40+"; command", None):
            with self.subTest(revision=revision), patch.object(verify_audits.subprocess, "run") as git:
                with self.assertRaises(ValueError): verify_audits.reference_tree(revision, Path("unused"))
                git.assert_not_called()

    def test_remote_reference_requires_explicit_audit_and_full_sha(self):
        for options in ({"native_reference":"main", "audit":True}, {"native_reference":"a"*40}, {"native_reference":None, "audit":True}):
            with self.subTest(options=options), patch.object(analyze, "fetch_sample") as fetch:
                with self.assertRaises(ValueError): remote_job.run_validation(json.dumps(options), {}, "unused", "b"*40)
                fetch.assert_not_called()

    def test_partial_or_tampered_results_never_publish_completion(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"features.tsv"
            for change in ({"complete":False}, {"source_sha_reverified":False}, {"features":{}}):
                result = {**complete(), **change}
                with self.assertRaisesRegex(RuntimeError, "incomplete"): native_audit.write_tsv(path, result, "sample.apk")
                self.assertFalse(path.exists())

    def test_negative_findings_are_complete_evidence_and_remain_negative(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"features.tsv"
            result = complete()
            for index, state in enumerate(("MISSING", "PARTIAL", "AMBIGUOUS")):
                result["features"][EXPECTED_FEATURES[index]]["status"] = state
            native_audit.write_tsv(path, result, "sample.apk")
            self.assertIn("META\taudit_complete\ttrue", path.read_text())
            self.assertEqual(analyze.features(path), result["features"])

    def invoke(self, backend="meguvizdexdash", *, failure=None, basic_rc=0):
        import mdd_gates
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab, "STATE", Path(folder)), \
             patch.object(analyze, "jar_path", return_value=None), patch.object(analyze.shutil, "which", return_value=None), \
             patch("install_meguvizdexdash.status", return_value={"available":True}), \
             patch.object(analyze, "inputs", return_value=(Path(folder)/"sample.apk", {"version_code":1, "sha256":"a"*64})), \
             patch.object(analyze, "tool_hashes", return_value={}), \
             patch.object(hostlab, "sdk_tool", side_effect=RuntimeError()), \
             patch.object(native_audit, "run", side_effect=failure, return_value=complete()), \
             patch.object(mdd_gates, "render_intake_log", return_value=(basic_rc, "intake log\n")) as render_gate, \
             patch.object(analyze, "execute", side_effect=[basic_rc, 0]) as execute, \
             patch.object(analyze.process_control, "run") as process:
            carrier = {}
            argv = ["audit", "--apk", folder]
            if backend is not None: argv += ["--backend", backend]
            rc = analyze.main(argv, surface_output=carrier)
            report = json.loads(next(Path(folder).glob("reports/*/*/*/summary.json")).read_text())
            self.assertTrue(all("java" not in str(c.args[0]) and "--audit" not in c.args[0] for c in execute.call_args_list))
            if failure is None:
                execute.assert_not_called()
                render_gate.assert_called_once()
            process.assert_not_called()
            return rc, report, carrier

    def test_native_full_audit_runs_retained_gates_without_java(self):
        rc, report, carrier = self.invoke()
        self.assertEqual(rc, 0)
        self.assertTrue(report["audit_complete"])
        self.assertEqual(report["audit_backend"], "meguvizdexdash")
        self.assertIn("report", carrier)

    def test_default_prefers_available_native_after_cloud_equivalence_acceptance(self):
        with patch.dict(os.environ):
            os.environ.pop("HOSTLAB_AUDIT_BACKEND", None)
            _, report, _ = self.invoke(None)
        self.assertEqual(report["audit_backend"], "meguvizdexdash")

    def test_invalid_environment_policy_fails_before_input_fetch(self):
        with patch.dict(os.environ, HOSTLAB_AUDIT_BACKEND="invalid"), patch.object(analyze, "inputs") as inputs:
            with self.assertRaises(ValueError): analyze.main(["audit", "--apk", "."])
            inputs.assert_not_called()

    def test_basic_gate_timeout_cannot_become_complete_native_audit(self):
        rc, report, _ = self.invoke(basic_rc=124)
        self.assertEqual(rc, 124)
        self.assertFalse(report["audit_complete"])

    def test_native_runtime_failure_is_not_silently_retried_with_legacy(self):
        with self.assertRaisesRegex(RuntimeError, "fatal query"):
            self.invoke("auto", failure=RuntimeError("fatal query"))
        with self.assertRaises(UnsupportedAudit): self.invoke(failure=UnsupportedAudit("unsupported"))

    def test_missing_pinned_explicit_backend_fails_without_java_or_input_fetch(self):
        with patch("install_meguvizdexdash.status", return_value={"available":False}), patch.object(analyze, "inputs") as inputs:
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                analyze.main(["audit", "--apk", ".", "--backend", "meguvizdexdash"])
            with self.assertRaisesRegex(RuntimeError, "replaced by meguvizdexdash"):
                analyze.main(["audit", "--apk", ".", "--backend", "dexsql"])
            inputs.assert_not_called()

    def test_apk_sha_change_is_detected_before_dataset_open(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(native_audit, "NativeSession") as session:
            apk = Path(folder)/"sample.apk"
            apk.write_bytes(b"fixture")
            with self.assertRaisesRegex(RuntimeError, "immutable"):
                native_audit.run(apk, sha256="0"*64)
            session.assert_not_called()

    def test_comparison_preserves_duplicates_and_normalizes_tuple_transport(self):
        self.assertEqual(verify_audits.normalized([("a", 1)], multiset=True), verify_audits.normalized([["a", 1]], multiset=True))
        checks = verify_audits.compare({"invoke_edges":[[1], [1]]}, {"invoke_edges":[[1]]})
        self.assertFalse(checks["invoke_edges"]["equal"])
        with self.assertRaises(RuntimeError): verify_audits.compare({"features":{}}, {})

    def test_cloud_audits_prepare_optional_native_and_keep_java_for_semantics(self):
        for operation in ("audit", "multipath_audit"):
            plan = plan_ci.requirements(operation, "")
            self.assertEqual((plan["needs_mdd"], plan["mdd_optional"], plan["needs_dexsql"], plan["needs_java"]),
                             ("true", "true", "false", "false"))


if __name__ == "__main__":
    unittest.main()
