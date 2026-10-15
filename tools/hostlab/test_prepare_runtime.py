"""Prepared environments recover from damage without trusting cached executables first."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import hostlab
import prepare_runtime


class PreparedRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.addCleanup(patch.stopall)
        patch.object(prepare_runtime, "ROOT", self.workspace).start()
        self.root = prepare_runtime.directory()
        self.identity, self.fingerprint = prepare_runtime.describe("requirements-query.txt")
        self.describe = patch.object(prepare_runtime, "describe",
            return_value=(self.identity, self.fingerprint)).start()
        self.distributions = [["huggingface_hub", "2.1.1"], ["mcp", "2.2.0"]]
        self.probe = patch.object(prepare_runtime, "probe", return_value=self.distributions).start()
        self.build = patch.object(prepare_runtime, "build", side_effect=self.build_fixture).start()

    def build_fixture(self, root, identity, fingerprint):
        root.mkdir(parents=True)
        python = prepare_runtime.interpreter(root)
        python.parent.mkdir(parents=True)
        python.write_bytes(b"test interpreter; never execute")
        package = root / "env" / "packages" / "module.py"
        package.parent.mkdir(parents=True)
        package.write_bytes(b"value = 1\n")
        hostlab.write_json(root / "receipt.json", {"schema": prepare_runtime.POLICY,
            "identity": identity, "fingerprint": fingerprint,
            "files": prepare_runtime.inventory(root, Path(identity["base_python"])),
            "distributions": self.distributions})

    def prepare(self):
        return prepare_runtime.prepare("requirements-query.txt")

    def invalid_copies(self):
        return list(self.root.parent.glob("hostlab-prepared-invalid-*"))

    def assert_rebuilt(self):
        result = self.prepare()
        self.assertFalse(result["cache_hit"])
        self.assertTrue(result["built"])
        self.assertTrue(result["repaired"])
        self.assertEqual(self.build.call_count, 2)
        self.assertEqual(len(self.invalid_copies()), 1)
        return result

    def symlink(self, target, path, directory=False):
        try:
            path.symlink_to(target, target_is_directory=directory)
        except OSError as exc:
            self.skipTest("symlinks unavailable: " + type(exc).__name__)

    def test_valid_cache_is_reverified_without_building_again(self):
        first = self.prepare()
        self.assertTrue(first["built"])
        self.assertFalse(first["cache_hit"])
        self.assertFalse(first["repaired"])
        with patch.object(hostlab, "digest", wraps=hostlab.digest) as digest:
            second = self.prepare()
        self.assertTrue(second["cache_hit"])
        self.assertFalse(second["built"])
        self.build.assert_called_once()
        self.assertEqual(self.probe.call_count, 2)
        self.assertTrue(any(call.args[0].name == "module.py" for call in digest.call_args_list))
        self.assertEqual(set(p.name for p in self.root.iterdir()), {"env", "receipt.json"})

    def test_same_size_tampering_preserves_bad_evidence_and_rebuilds(self):
        self.prepare()
        module = self.root / "env/packages/module.py"
        old_size = module.stat().st_size
        module.write_bytes(b"value = 9\n")
        self.assertEqual(module.stat().st_size, old_size)
        self.assert_rebuilt()
        self.assertEqual(module.read_bytes(), b"value = 1\n")
        self.assertEqual((self.invalid_copies()[0] / "env/packages/module.py").read_bytes(), b"value = 9\n")

    def test_unrecorded_package_file_invalidates_cache_before_probe(self):
        self.prepare()
        extra = self.root / "env/packages/unrecorded.py"
        extra.write_bytes(b"unexpected code")
        self.probe.reset_mock()
        self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
        self.probe.assert_not_called()
        self.assert_rebuilt()
        self.assertFalse(extra.exists())

    def test_changed_environment_identity_cannot_reuse_existing_interpreter(self):
        self.prepare()
        changed = {**self.identity, "image_version": "different-runner-image"}
        self.describe.return_value = changed, "f" * 64
        self.probe.reset_mock()
        self.assertFalse(prepare_runtime.verify(self.root, changed, "f" * 64))
        self.probe.assert_not_called()
        result = self.assert_rebuilt()
        self.assertEqual(result["fingerprint"], "f" * 64)

    def test_partial_build_has_no_trusted_receipt_and_next_call_recovers(self):
        def interrupted(root, identity, fingerprint):
            (root / "env").mkdir(parents=True)
            (root / "env/partial-wheel").write_bytes(b"incomplete")
            raise OSError("interrupted package installation")

        self.build.side_effect = interrupted
        with self.assertRaisesRegex(OSError, "interrupted"):
            self.prepare()
        self.assertFalse((self.root / "receipt.json").exists())
        self.probe.assert_not_called()
        self.build.side_effect = self.build_fixture
        result = self.prepare()
        self.assertTrue(result["repaired"])
        self.assertTrue(result["built"])
        self.assertEqual((self.invalid_copies()[0] / "env/partial-wheel").read_bytes(), b"incomplete")

    def test_corrupt_or_wrong_shape_receipt_is_recoverable(self):
        self.prepare()
        for document in ("{broken", "[]", "null", "23"):
            with self.subTest(document=document):
                (self.root / "receipt.json").write_text(document, encoding="utf-8")
                self.probe.reset_mock()
                self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
                self.probe.assert_not_called()
        result = self.prepare()
        self.assertTrue(result["repaired"])

    def test_cache_root_rejects_private_data_and_unrecorded_siblings(self):
        self.prepare()
        private = self.root / "HF_HOME/token"
        private.parent.mkdir()
        private.write_text("fixture-only", encoding="utf-8")
        self.probe.reset_mock()
        self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
        self.probe.assert_not_called()
        self.assert_rebuilt()
        self.assertFalse((self.root / "HF_HOME").exists())
        self.assertEqual((self.invalid_copies()[0] / "HF_HOME/token").read_text(), "fixture-only")

    def test_windows_reparse_environment_is_rejected_before_probe(self):
        self.prepare()
        original_lstat = Path.lstat

        def linked(path):
            info = original_lstat(path)
            if path == self.root / "env":
                return SimpleNamespace(st_mode=info.st_mode, st_size=info.st_size,
                                       st_file_attributes=0x400)
            return info

        self.probe.reset_mock()
        with patch.object(Path, "lstat", linked):
            self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
        self.probe.assert_not_called()

    def test_linked_env_root_never_executes_or_traverses_external_environment(self):
        self.prepare()
        outside = self.workspace / "outside-env"
        (self.root / "env").rename(outside)
        self.symlink(outside, self.root / "env", directory=True)
        self.probe.reset_mock()
        self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
        self.probe.assert_not_called()
        self.assertEqual((outside / "packages/module.py").read_bytes(), b"value = 1\n")

    def test_unexpected_package_link_is_rejected_before_probe(self):
        self.prepare()
        outside = self.workspace / "outside.py"
        outside.write_bytes(b"fixture-only")
        self.symlink(outside, self.root / "env/packages/linked.py")
        self.probe.reset_mock()
        self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
        self.probe.assert_not_called()
        self.assertEqual(outside.read_bytes(), b"fixture-only")

    def test_receipt_link_is_rejected_before_probe(self):
        self.prepare()
        receipt = self.root / "receipt.json"
        outside = self.workspace / "outside-receipt.json"
        receipt.rename(outside)
        self.symlink(outside, receipt)
        self.probe.reset_mock()
        self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
        self.probe.assert_not_called()

    def test_linked_lock_never_opens_or_changes_external_target(self):
        self.root.parent.mkdir(parents=True)
        outside = self.workspace / "outside-lock"
        outside.write_bytes(b"")
        self.symlink(outside, self.root.parent / "hostlab-prepared.lock")
        with self.assertRaises((ValueError, RuntimeError)):
            self.prepare()
        self.assertEqual(outside.read_bytes(), b"")
        self.build.assert_not_called()
        self.probe.assert_not_called()

    def test_cache_path_outside_dedicated_directory_is_rejected_before_writes(self):
        outside = self.workspace / "other-cache"
        with patch.object(prepare_runtime, "directory", return_value=outside):
            with self.assertRaisesRegex(ValueError, "dedicated"):
                self.prepare()
        self.assertFalse(outside.exists())
        self.build.assert_not_called()

    def test_runtime_parent_link_is_rejected_without_changing_target(self):
        outside = self.workspace / "elsewhere"
        outside.mkdir()
        self.symlink(outside, self.workspace / "runtime", directory=True)
        with self.assertRaisesRegex(ValueError, "linked"):
            self.prepare()
        self.assertEqual(list(outside.iterdir()), [])
        self.build.assert_not_called()

    def test_file_and_byte_budgets_reject_cache_before_probe(self):
        self.prepare()
        for limit, value in (("MAX_FILES", 1), ("MAX_BYTES", 1)):
            with self.subTest(limit=limit), patch.object(prepare_runtime, limit, value):
                self.probe.reset_mock()
                self.assertFalse(prepare_runtime.verify(self.root, self.identity, self.fingerprint))
                self.probe.assert_not_called()

    def test_lock_allows_one_preparer_and_is_released_after_completion(self):
        entered, release = threading.Event(), threading.Event()

        def blocked_build(root, identity, fingerprint):
            entered.set()
            if not release.wait(5):
                raise RuntimeError("test preparation was not released")
            self.build_fixture(root, identity, fingerprint)

        self.build.side_effect = blocked_build
        with ThreadPoolExecutor(max_workers=1) as pool:
            worker = pool.submit(self.prepare)
            try:
                self.assertTrue(entered.wait(5))
                with self.assertRaisesRegex(RuntimeError, "already in progress"):
                    self.prepare()
            finally:
                release.set()
            self.assertTrue(worker.result(timeout=5)["built"])
        self.assertTrue(self.prepare()["cache_hit"])
        self.build.assert_called_once()


class RuntimeBootstrapContractTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.addCleanup(patch.stopall)
        patch.object(prepare_runtime, "ROOT", self.workspace).start()
        self.root = prepare_runtime.directory()
        self.identity, self.fingerprint = prepare_runtime.describe("requirements-query.txt")

    def fake_venv(self, path):
        python = prepare_runtime.interpreter(path.parent)
        python.parent.mkdir(parents=True)
        python.write_bytes(b"test interpreter; never execute")
        (path / "pyvenv.cfg").write_text("fixture-only", encoding="utf-8")

    def test_build_uses_existing_pip_no_compile_and_checks_before_receipt(self):
        builder = Mock()
        builder.create.side_effect = self.fake_venv
        with patch.object(prepare_runtime.venv, "EnvBuilder", return_value=builder) as factory, \
                patch.object(prepare_runtime.subprocess, "run") as run, \
                patch.object(prepare_runtime, "probe", return_value=[["mcp", "2.2.0"]]):
            prepare_runtime.build(self.root, self.identity, self.fingerprint)
        factory.assert_called_once_with(with_pip=False, symlinks=os.name != "nt")
        self.assertEqual(run.call_count, 2)
        install, check = [call.args[0] for call in run.call_args_list]
        self.assertIn("--python", install)
        self.assertIn(str(prepare_runtime.interpreter(self.root)), install)
        self.assertIn("--no-compile", install)
        self.assertEqual(check[-1], "check")
        self.assertEqual(run.call_args_list[0].kwargs["env"]["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertTrue((self.root / "receipt.json").is_file())
        self.assertEqual(set(p.name for p in self.root.iterdir()), {"env", "receipt.json"})

    def test_failed_install_or_probe_never_writes_success_receipt(self):
        for phase in ("install", "probe"):
            with self.subTest(phase=phase):
                case = self.workspace / phase
                case.mkdir()
                with patch.object(prepare_runtime, "ROOT", case):
                    root = prepare_runtime.directory()
                    builder = Mock()
                    builder.create.side_effect = self.fake_venv
                    error = subprocess.CalledProcessError(1, ["fixture"])
                    with patch.object(prepare_runtime.venv, "EnvBuilder", return_value=builder), \
                            patch.object(prepare_runtime.subprocess, "run",
                                side_effect=error if phase == "install" else None), \
                            patch.object(prepare_runtime, "probe", side_effect=error if phase == "probe" else None):
                        with self.assertRaises(subprocess.CalledProcessError):
                            prepare_runtime.build(root, self.identity, self.fingerprint)
                    self.assertFalse((root / "receipt.json").exists())

    def test_probe_uses_isolated_no_bytecode_interpreter_and_exact_versions(self):
        result = SimpleNamespace(stdout='[["mcp", "2.2.0"]]')
        with patch.object(prepare_runtime.subprocess, "run", return_value=result) as run:
            self.assertEqual(prepare_runtime.probe(self.root, "requirements-query.txt"), [["mcp", "2.2.0"]])
        args = run.call_args.args[0]
        self.assertEqual(args[:4], [str(prepare_runtime.interpreter(self.root)), "-I", "-B", "-c"])
        prefix, expected = json.loads(args[-1])
        self.assertEqual(prefix, str(self.root / "env"))
        self.assertIn(["mcp", "2.2.0"], expected)
        self.assertTrue(run.call_args.kwargs["check"])
        self.assertEqual(run.call_args.kwargs["timeout"], 30)

    def test_identity_changes_for_dependency_image_and_workspace_changes(self):
        identity, initial = prepare_runtime.describe("requirements-query.txt")
        self.assertNotEqual(initial, prepare_runtime.describe("requirements.txt")[1])
        with patch.dict(os.environ, {"ImageVersion": "different-exact-image"}):
            self.assertNotEqual(initial, prepare_runtime.describe("requirements-query.txt")[1])
        with patch.object(prepare_runtime, "ROOT", self.workspace / "different"):
            self.assertNotEqual(initial, prepare_runtime.describe("requirements-query.txt")[1])
        self.assertNotIn("HF_TOKEN", identity)
        self.assertNotIn("HF_HOME", identity)

    def test_unknown_requirement_subset_fails_without_touching_runtime(self):
        with self.assertRaisesRegex(ValueError, "subset"):
            prepare_runtime.describe("../../private.txt")
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
