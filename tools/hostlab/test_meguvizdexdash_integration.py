"""Unit tests for the MeguvizDexDash 1.2.2 advanced HostLab integration."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import analyze
import hostlab
import install_meguvizdexdash
import mdd_gates
import mdd_session
import native_audit


ROOT = Path(__file__).resolve().parents[2]


class InstallerMeguvizDexDashTest(unittest.TestCase):
    def test_pinned_release_metadata(self):
        self.assertEqual(install_meguvizdexdash.PRODUCT, "MeguvizDexDash")
        self.assertEqual(install_meguvizdexdash.VERSION, "1.2.2")
        self.assertEqual(install_meguvizdexdash.SOURCE_COMMIT, "e0358934620aa82091178febb1a2ce6c7abad9db")
        self.assertEqual(install_meguvizdexdash.REQUIRED_DIALECT, "dexsql-0.1.0")
        self.assertEqual(install_meguvizdexdash.ENV_OVERRIDE, "HOSTLAB_MEGUVIZDEXDASH")
        self.assertEqual(
            set(install_meguvizdexdash.PLATFORMS),
            {("Windows", "AMD64"), ("Linux", "x86_64"), ("Darwin", "arm64")},
        )

    def test_override_is_never_overwritten_and_missing_binary_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "not-mdd.exe"
            bad.write_bytes(b"wrong binary")
            with patch.dict(os.environ, {"HOSTLAB_MEGUVIZDEXDASH": str(bad)}), patch.object(
                install_meguvizdexdash, "_build_from_pinned_source"
            ) as build:
                with self.assertRaises(RuntimeError):
                    install_meguvizdexdash.install()
                self.assertFalse(install_meguvizdexdash.status()["available"])
                build.assert_not_called()
            self.assertEqual(bad.read_bytes(), b"wrong binary")

    def test_inspect_validates_version_build_id_and_capabilities(self):
        _, build_id = install_meguvizdexdash.asset()
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "meguvizdexdash"
            binary.write_bytes(b"mdd-fixture")
            version_payload = {
                "product": "MeguvizDexDash",
                "engine_version": "1.2.2",
                "build_id": build_id,
            }
            caps_payload = {
                "schema_version": "mdd.capabilities.v1",
                "build_id": build_id,
                "sql_dialects": [{"name": "dexsql-0.1.0"}],
                "capabilities": [{"name": "cli-serve", "available": True}],
            }
            with patch.object(
                install_meguvizdexdash, "_run_json", side_effect=[version_payload, caps_payload]
            ):
                info = install_meguvizdexdash.inspect(binary)
            self.assertEqual(info["version"], "1.2.2")
            self.assertEqual(info["build_id"], build_id)

            bad_caps = {**caps_payload, "capabilities": [{"name": "cli-serve", "available": False}]}
            with patch.object(
                install_meguvizdexdash, "_run_json", side_effect=[version_payload, bad_caps]
            ), self.assertRaisesRegex(RuntimeError, "cli-serve"):
                install_meguvizdexdash.inspect(binary)


class MddSessionContractTest(unittest.TestCase):
    def test_serve_command_and_environment(self):
        cmd = mdd_session.serve_command("/bin/meguvizdexdash", Path("sample.apk"), timeout_seconds=120)
        self.assertEqual(cmd[:2], ["/bin/meguvizdexdash", "serve"])
        self.assertNotIn("--threads", cmd)
        self.assertEqual(cmd[cmd.index("--dialect") + 1], "dexsql-0.1.0")
        self.assertEqual(cmd[cmd.index("--non-scalar-text") + 1], "lossy-replacement")
        self.assertIn("--input", cmd)

        with patch.dict(
            os.environ,
            {
                "HF_TOKEN": "secret",
                "GH_TOKEN": "secret",
                "DEXQ_CACHE_DIR": "/tmp/dexq",
                "DEXQ_WORKERS": "8",
            },
        ):
            env = mdd_session.child_environment(Path("sample.apk"), 2)
        self.assertNotIn("HF_TOKEN", env)
        self.assertNotIn("GH_TOKEN", env)
        self.assertNotIn("DEXQ_CACHE_DIR", env)
        self.assertIn("MDD_FACTS_THREADS", env)
        self.assertEqual(env["PYTHONIOENCODING"], "utf-8")

    def test_dto_cell_decoding_and_completeness_checks(self):
        decode = mdd_session.B1Session._decode_dto_cell
        self.assertIsNone(decode({"t": "null"}))
        self.assertEqual(decode({"t": "text", "v": "hello"}), "hello")
        self.assertEqual(decode({"t": "text", "units": "0041d83dde00"}), "A\U0001f600")
        self.assertEqual(decode({"t": "u64", "v": "18446744073709551615"}), "18446744073709551615")
        self.assertEqual(decode({"t": "i64", "v": -7}), "-7")
        self.assertEqual(decode({"t": "dex_mutf8", "v": "6162", "utf16_units": 2}), "ab")
        for bad in (
            {"t": "text", "units": "d800"},
            {"t": "bool", "v": True},
            {"t": "f64", "bits": "00" * 8},
            {"t": "bytes", "v": "00"},
        ):
            with self.subTest(bad=bad), self.assertRaises(mdd_session.EngineProtocolError):
                decode(bad)
        self.assertTrue(mdd_session._completeness("ok", "complete", "complete", True)["complete"])
        self.assertFalse(mdd_session._completeness("ok", "complete", "partial", True)["complete"])


class MddGatesAndWorkflowTest(unittest.TestCase):
    def test_gate_descriptor_helpers(self):
        self.assertEqual(mdd_gates._desc_to_java("[Ljava/lang/String;"), "java.lang.String[]")
        self.assertEqual(
            mdd_gates._parse_method_descriptor("LFoo;->m(I[Ljava/lang/String;)V"),
            (["I", "[Ljava/lang/String;"], "V"),
        )
        self.assertEqual(
            mdd_gates._extract_field_type_descriptor("LFoo;->bar:Ljava/lang/String;"),
            "Ljava/lang/String;",
        )
        rendered = mdd_gates.render_home_frame_log(
            Path("sample.apk"), {"apk": "sample.apk", "data.owner": "Lx;"}
        )
        self.assertEqual(rendered, "======== sample.apk\n  data.owner: Lx;\n")

    def test_missing_shared_fact_gates_fail_closed(self):
        from analysis.run_intake import EXPECTED_FEATURES

        bad_native = {
            "features": {name: {"status": "FOUND", "detail": "fixture"} for name in EXPECTED_FEATURES},
            "discoveries": {},
            "complete": True,
            "source_sha_reverified": True,
            "class_count": 1,
            "surface": {"fixture": True},
            "gates": None,
        }
        with tempfile.TemporaryDirectory() as folder, patch.object(hostlab, "STATE", Path(folder)), patch(
            "install_meguvizdexdash.status", return_value={"available": True}
        ), patch.object(
            analyze, "inputs", return_value=(Path(folder) / "sample.apk", {"version_code": 1, "sha256": "a" * 64})
        ), patch.object(analyze, "tool_hashes", return_value={}), patch.object(
            hostlab, "sdk_tool", side_effect=RuntimeError()
        ), patch.object(native_audit, "run", return_value=bad_native):
            with self.assertRaisesRegex(RuntimeError, "shared-fact gates"):
                analyze.main(["audit", "--apk", folder, "--backend", "meguvizdexdash"])

    def test_host_analysis_workflow_copies_are_byte_identical(self):
        root_wf = (ROOT / ".github/workflows/host-analysis.yml").read_bytes()
        tool_wf = (ROOT / "tools/hostlab/host-analysis.yml").read_bytes()
        self.assertEqual(root_wf, tool_wf)
        self.assertIn(b"options: [meguvizdexdash, sqlite, dexsql]", root_wf)
        self.assertIn(b"default: meguvizdexdash", root_wf)


if __name__ == "__main__":
    unittest.main()
