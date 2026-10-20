import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import hostlab
import source_intake as intake


class SourceAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.receipt = dict(schema=1, source="appshare", channel="official",
                            version_code=9160200, version_name="9.16.0")
        self.policy = dict(schema=1, package="tv.danmaku.bili", channel="official",
                           signer_sets=[["a" * 64]])
        self.row = dict(package="tv.danmaku.bili", version_code=9160200,
                        version_name="9.16.0", certificate_sha256=["a" * 64],
                        sha256="b" * 64, size=10, abis=["arm64-v8a"])
        self.identity = patch.object(hostlab, "identity", return_value=self.row).start()
        self.addCleanup(patch.stopall)

    def test_accepts_exact_identity_without_network(self):
        result = intake.verify("host.apk", self.receipt, self.policy)
        self.assertEqual(result["source"], {"provider": "appshare", "channel": "official"})
        self.assertEqual(result["sha256"], "b" * 64)

    def test_unknown_receipt_fields_reject_urls_and_secrets(self):
        for field in ("url", "cookie", "token", "certificate_sha256"):
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                intake.verify("x", {**self.receipt, field: "secret"}, self.policy)
        self.identity.assert_not_called()

    def test_wrong_identity_and_extra_signer_fail_closed(self):
        for key, value in (("package", "com.other"), ("version_code", 1),
                           ("version_name", "9.15.0"),
                           ("certificate_sha256", ["a" * 64, "c" * 64]),
                           ("certificate_sha256", [])):
            with self.subTest(key=key), self.assertRaises(RuntimeError):
                self.identity.return_value = {**self.row, key: value}
                intake.verify("x", self.receipt, self.policy)

    def test_invalid_policy_and_channel_fail_before_sdk(self):
        for update in ({"signer_sets": []}, {"signer_sets": [["bad"]]},
                       {"signer_sets": [["a" * 64, "a" * 64]]},
                       {"channel": "another"}, {"schema": True}):
            with self.subTest(update=update), self.assertRaises(RuntimeError):
                intake.verify("x", self.receipt, {**self.policy, **update})
        self.identity.assert_not_called()

    def test_invalid_receipt_types_and_labels(self):
        for update in ({"version_code": True}, {"version_code": "9160200"},
                       {"channel": "https://secret"}, {"version_name": "x\ny"},
                       {"source": "unknown"}):
            with self.subTest(update=update), self.assertRaises(RuntimeError):
                intake.verify("x", {**self.receipt, **update}, self.policy)

    def test_sdk_failure_propagates_without_admitting(self):
        self.identity.side_effect = subprocess.CalledProcessError(1, "sdk")
        with self.assertRaises(subprocess.CalledProcessError):
            intake.verify("x", self.receipt, self.policy)


class SdkPlatformTests(unittest.TestCase):
    def test_numeric_stable_version_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for version in ("9.0.0", "35.0.0", "36.0.0-rc1"):
                tool = root / "build-tools" / version / "aapt"
                tool.parent.mkdir(parents=True)
                tool.touch()
            with patch.dict(os.environ, {"ANDROID_HOME": directory}), patch.object(hostlab.sys, "platform", "linux"):
                self.assertEqual(hostlab.sdk_tool("aapt").parent.name, "35.0.0")

    def test_platform_commands(self):
        with patch.object(hostlab, "sdk_tool", return_value=Path("sdk/apksigner")):
            with patch.object(hostlab.sys, "platform", "linux"):
                self.assertEqual(hostlab.sdk_command("apksigner", "verify", "a.apk"),
                                 ["sdk/apksigner", "verify", "a.apk"])
            with patch.object(hostlab.sys, "platform", "win32"):
                self.assertEqual(hostlab.sdk_command("apksigner", "verify")[:3], ["cmd.exe", "/d", "/c"])

    def test_sdk_root_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            tool = Path(directory) / "build-tools" / "35.0.0" / "aapt"
            tool.parent.mkdir(parents=True)
            tool.touch()
            with patch.dict(os.environ, {"ANDROID_SDK_ROOT": directory}, clear=True), patch.object(hostlab.sys, "platform", "linux"):
                self.assertEqual(hostlab.sdk_tool("aapt"), tool)


class IdentityTests(unittest.TestCase):
    def test_identity_uses_posix_tools_and_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            apk = Path(directory) / "host.apk"
            apk.write_bytes(b"fixture")
            badging = "package: name='tv.danmaku.bili' versionCode='9160200' versionName='9.16.0'\nnative-code: 'arm64-v8a' 'armeabi-v7a'\n"
            cert = "Signer #1 certificate SHA-256 digest: " + "a" * 64
            with patch.object(hostlab, "sdk_tool", side_effect=lambda name: Path(name)), patch.object(hostlab.sys, "platform", "linux"), patch.object(hostlab.subprocess, "check_output", side_effect=[badging, cert]) as call:
                row = hostlab.identity(apk)
            self.assertEqual(row["sha256"], hostlab.digest(apk))
            self.assertEqual(row["abis"], ["arm64-v8a", "armeabi-v7a"])
            self.assertEqual(call.call_args_list[0].args[0][0], "aapt")
            self.assertEqual(call.call_args_list[1].args[0][0], "apksigner")

    def test_mutation_during_inspection_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            apk = Path(directory) / "host.apk"
            apk.write_bytes(b"original")
            def sdk(command, **kwargs):
                if command[0] == "aapt":
                    return "package: name='tv.danmaku.bili' versionCode='1' versionName='1'"
                apk.write_bytes(b"changed")
                return "Signer #1 certificate SHA-256 digest: " + "a" * 64
            with patch.object(hostlab, "sdk_tool", side_effect=lambda name: Path(name)), patch.object(hostlab.sys, "platform", "linux"), patch.object(hostlab.subprocess, "check_output", side_effect=sdk), self.assertRaisesRegex(RuntimeError, "changed"):
                hostlab.identity(apk)

    def test_source_flags_fail_before_private_repo_access(self):
        with patch.object(hostlab.sys, "argv", ["hostlab.py", "upload", "x.apk", "--source-receipt", "x.json"]), patch.object(hostlab, "config") as config, self.assertRaisesRegex(RuntimeError, "both"):
            hostlab.main()
        config.assert_not_called()


class UploadSnapshotTests(unittest.TestCase):
    def test_snapshot_survives_source_mutation_and_is_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            apk = Path(directory) / "host.apk"
            apk.write_bytes(b"original")
            row = {"sha256": hostlab.digest(apk), "size": apk.stat().st_size}
            with hostlab.verified_upload_file(apk, row) as snapshot:
                apk.write_bytes(b"changed")
                self.assertEqual(snapshot.read_bytes(), b"original")
            self.assertFalse(snapshot.exists())

    def test_changed_input_never_reaches_upload(self):
        with tempfile.TemporaryDirectory() as directory:
            apk = Path(directory) / "host.apk"
            apk.write_bytes(b"original")
            row = {"sha256": hostlab.digest(apk), "size": apk.stat().st_size}
            apk.write_bytes(b"tampered")
            with self.assertRaisesRegex(RuntimeError, "changed before upload"):
                with hostlab.verified_upload_file(apk, row):
                    self.fail("unverified bytes exposed to uploader")


if __name__ == "__main__":
    unittest.main()
