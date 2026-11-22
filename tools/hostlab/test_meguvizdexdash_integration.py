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
        self.assertEqual(install_meguvizdexdash.RELEASE_TAG, "v1.2.2")
        self.assertEqual(install_meguvizdexdash.SOURCE_COMMIT, "6f0d5ce47680628ee9c51bfcc8a9157d9641c0ec")
        self.assertEqual(install_meguvizdexdash.REQUIRED_DIALECT, "dexsql-0.1.0")
        self.assertEqual(install_meguvizdexdash.ENV_OVERRIDE, "HOSTLAB_MEGUVIZDEXDASH")
        self.assertEqual(
            set(install_meguvizdexdash.PLATFORMS),
            {("Windows", "AMD64"), ("Linux", "x86_64"), ("Darwin", "arm64")},
        )
        self.assertEqual(
            set(install_meguvizdexdash.RELEASE_ASSETS),
            {("Windows", "AMD64"), ("Linux", "x86_64")},
        )
        self.assertEqual(
            install_meguvizdexdash.RELEASE_ASSETS[("Windows", "AMD64")][1],
            "7ecf44b0c707b0202a550d8d318e8d158e7a8ca2c286d8868034e40c63b50f68",
        )
        self.assertEqual(
            install_meguvizdexdash.RELEASE_ASSETS[("Linux", "x86_64")][1],
            "0d1a03bf130c47e06e342c01b8fb9ee0321e3c3a7b6807008ab1f4c2c3a76973",
        )

    def test_override_is_never_overwritten_and_missing_binary_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "not-mdd.exe"
            bad.write_bytes(b"wrong binary")
            with patch.dict(os.environ, {"HOSTLAB_MEGUVIZDEXDASH": str(bad)}), patch.object(
                install_meguvizdexdash, "_download_release_binary"
            ) as download, patch.object(
                install_meguvizdexdash, "_build_from_pinned_source"
            ) as build:
                with self.assertRaises(RuntimeError):
                    install_meguvizdexdash.install()
                self.assertFalse(install_meguvizdexdash.status()["available"])
                download.assert_not_called()
                build.assert_not_called()
            self.assertEqual(bad.read_bytes(), b"wrong binary")

    def test_release_download_verifies_sha_before_execution_and_writes_receipt(self):
        import hashlib
        import io

        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        payload = b"verified-release-binary"
        digest = hashlib.sha256(payload).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "vendor/meguvizdexdash/1.2.2/meguvizdexdash"
            target.parent.mkdir(parents=True)

            with patch.object(
                install_meguvizdexdash.urllib.request, "urlopen", return_value=FakeResponse(b"tampered")
            ), patch.object(install_meguvizdexdash, "inspect") as inspect_mock:
                with self.assertRaisesRegex(RuntimeError, "SHA-256 mismatch"):
                    install_meguvizdexdash._download_release_binary(target, "meguvizdexdash-linux-x86_64", digest)
                inspect_mock.assert_not_called()
            self.assertFalse(target.exists())
            self.assertEqual(list(target.parent.glob("*.staging")), [])

            fake_info = {
                "engine": "meguvizdexdash",
                "product": "MeguvizDexDash",
                "version": "1.2.2",
                "build_id": "source-sha256:d10a00fb9fa5ea1db35e15d3e4b6410cbd67cfb7fb2b99bb0f60855212e28164",
                "dialect": "dexsql-0.1.0",
                "sha256": digest,
                "path": str(target),
            }
            with patch.object(
                install_meguvizdexdash.urllib.request, "urlopen", return_value=FakeResponse(payload)
            ), patch.object(install_meguvizdexdash, "inspect", return_value=fake_info) as inspect_mock:
                install_meguvizdexdash._download_release_binary(target, "meguvizdexdash-linux-x86_64", digest)
            inspect_mock.assert_called_once()
            self.assertEqual(target.read_bytes(), payload)
            receipt = json.loads(target.with_name("BUILD_INFO.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["source"], "github_release")
            self.assertEqual(receipt["release_tag"], "v1.2.2")
            self.assertEqual(receipt["sha256"], digest)

    def test_install_routes_prebuilt_platforms_to_release_and_darwin_to_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for plat_system, plat_machine, expect_download in (
                ("Linux", "x86_64", True),
                ("Windows", "AMD64", True),
                ("Darwin", "arm64", False),
            ):
                target = root / plat_system / "meguvizdexdash"
                with self.subTest(system=plat_system), patch.dict(os.environ, {}, clear=True), patch.object(
                    install_meguvizdexdash.platform, "system", return_value=plat_system
                ), patch.object(
                    install_meguvizdexdash.platform, "machine", return_value=plat_machine
                ), patch.object(
                    install_meguvizdexdash, "executable", return_value=target
                ), patch.object(
                    install_meguvizdexdash, "_download_release_binary"
                ) as dl, patch.object(
                    install_meguvizdexdash, "_build_from_pinned_source"
                ) as build, patch.object(
                    install_meguvizdexdash, "verify", return_value=target
                ):
                    self.assertEqual(install_meguvizdexdash.install(), target)
                if expect_download:
                    dl.assert_called_once()
                    build.assert_not_called()
                else:
                    build.assert_called_once()
                    dl.assert_not_called()

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
        self.assertNotIn(b"install_dexsql.py", root_wf)
        self.assertNotIn(b"rustup toolchain install", root_wf)


if __name__ == "__main__":
    unittest.main()
