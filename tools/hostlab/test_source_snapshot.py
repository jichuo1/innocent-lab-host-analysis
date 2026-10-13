import contextlib
import copy
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import source_snapshot as S


class SourceSnapshotTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.source = self.root / S.SOURCE_PREFIX / "com/example"
        self.source.mkdir(parents=True)
        self.one = self.source / "PlainAdapter.kt"
        self.one.write_bytes(b"package example\r\nclass PlainAdapter\r\n")
        for relative in S.FIXED_PATHS:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"fixture\n")
        self.git("init", "--quiet")
        self.git("add", ".")
        self.git("-c", "user.name=Snapshot test", "-c", "user.email=snapshot@example.invalid",
                 "commit", "--quiet", "-m", "test(snapshot): initial fixture")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True,
                              check=True, timeout=30).stdout

    def test_captures_all_sources_and_only_explicit_allowlist(self):
        paths = [self.source / "adapter/Untracked.java", self.source / "runtime/Bridge.kt",
                 self.source / "diagnostics/Catalog.kt", self.source / "settings/Settings.kt"]
        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"// no multipath keywords\n")
        for relative in ("docs/source.kt", "runtime/private.kt", ".env", "sample.apk",
                         S.SOURCE_PREFIX + "NotSource.txt"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"private excluded bytes")
        ctx = S.capture(self.root)
        actual = {r["path"] for r in ctx["source_records"]}
        self.assertEqual(actual, {p.relative_to(self.root).as_posix() for p in [self.one, *paths]} | set(S.FIXED_PATHS))
        self.assertTrue(ctx["working_tree_dirty"])
        self.assertEqual(S.validate(ctx), ctx)

    def test_bom_and_crlf_are_hashed_and_serialized_as_original_bytes(self):
        raw = b"\xef\xbb\xbf// Kotlin Compose\r\nclass A\r\n"
        self.one.write_bytes(raw)
        ctx = S.capture(self.root)
        record = next(r for r in ctx["source_records"] if r["path"].endswith("PlainAdapter.kt"))
        self.assertEqual(record["source"].encode("utf-8"), raw)
        self.assertEqual(record["bytes"], len(raw))
        self.assertEqual(record["sha256"], hashlib.sha256(raw).hexdigest())
        loaded = json.loads(S.serialize(ctx))
        self.assertEqual(loaded, ctx)
        S.validate(loaded, hashlib.sha256(S.serialize(ctx)).hexdigest())

    def test_canonical_json_and_capture_time_independent_tree_identity(self):
        ctx = S.capture(self.root)
        shuffled = dict(reversed(list(ctx.items())))
        shuffled["source_records"] = [dict(reversed(list(r.items()))) for r in ctx["source_records"]]
        self.assertEqual(S.serialize(ctx), S.serialize(shuffled))
        recaptured = S.capture(self.root)
        self.assertEqual(ctx["source_tree_sha256"], recaptured["source_tree_sha256"])
        changed_time = dict(ctx, captured_at="2026-10-13T00:00:00Z")
        S.validate(changed_time)
        self.assertNotEqual(S.serialize(ctx), S.serialize(changed_time))

    def test_same_head_edit_add_delete_and_head_change_change_identity(self):
        ctx = S.capture(self.root)
        self.one.write_bytes(b"changed")
        modified = S.capture(self.root)
        self.assertEqual(ctx["repository_head"], modified["repository_head"])
        self.assertNotEqual(ctx["source_tree_sha256"], modified["source_tree_sha256"])
        extra = self.source / "New.kt"
        extra.write_bytes(b"new")
        added = S.capture(self.root)
        self.assertNotEqual(modified["source_tree_sha256"], added["source_tree_sha256"])
        self.one.unlink()
        removed = S.capture(self.root)
        self.assertNotEqual(added["source_tree_sha256"], removed["source_tree_sha256"])
        self.git("add", ".")
        self.git("-c", "user.name=Snapshot test", "-c", "user.email=snapshot@example.invalid",
                 "commit", "--quiet", "-m", "test(snapshot): changed fixture")
        committed = S.capture(self.root)
        self.assertNotEqual(removed["source_tree_sha256"], committed["source_tree_sha256"])

    def test_mid_capture_changes_retry_and_freeze_a_consistent_set(self):
        original = S._read_records
        old = self.source / "Removed.kt"
        old.write_bytes(b"removed")
        new = self.source / "Added.kt"
        calls = 0
        def read(root):
            nonlocal calls
            calls += 1
            if calls == 2:
                self.one.write_bytes(b"latest\r\n")
                old.unlink()
                new.write_bytes(b"added\n")
            return original(root)
        with patch.object(S, "_read_records", side_effect=read):
            ctx = S.capture(self.root)
        self.assertEqual(calls, 4)
        paths = {r["path"] for r in ctx["source_records"]}
        self.assertIn(new.relative_to(self.root).as_posix(), paths)
        self.assertNotIn(old.relative_to(self.root).as_posix(), paths)
        self.assertEqual(next(r["source"] for r in ctx["source_records"] if r["path"].endswith("PlainAdapter.kt")), "latest\r\n")

    def test_continuous_changes_stop_after_bounded_attempts(self):
        original = S._read_records
        calls = 0
        def read(root):
            nonlocal calls
            calls += 1
            self.one.write_bytes(str(calls).encode("ascii"))
            return original(root)
        with patch.object(S, "_read_records", side_effect=read):
            with self.assertRaisesRegex(ValueError, "bounded capture"):
                S.capture(self.root, max_attempts=3)
        self.assertEqual(calls, 6)

    def test_head_change_during_capture_retries(self):
        head = S._head(self.root)
        new_head = "a" * 40 if head != "a" * 40 else "b" * 40
        with patch.object(S, "_head", side_effect=[head, new_head, new_head, new_head]) as reader:
            ctx = S.capture(self.root)
        self.assertEqual(reader.call_count, 4)
        self.assertEqual(ctx["repository_head"], new_head)

    def test_manifest_and_payload_tampering_are_rejected(self):
        ctx = S.capture(self.root)
        for field, value in (("source", "tampered"), ("sha256", "0" * 64), ("bytes", 0)):
            altered = copy.deepcopy(ctx)
            altered["source_records"][0][field] = value
            with self.assertRaises(ValueError):
                S.validate(altered)
        with self.assertRaisesRegex(ValueError, "payload SHA-256"):
            S.validate(ctx, "0" * 64)
        changed = dict(ctx, source_tree_sha256="0" * 64)
        with self.assertRaisesRegex(ValueError, "tree identity"):
            S.validate(changed)

    def test_schema_paths_scope_sorting_and_empty_manifest_are_rejected(self):
        ctx = S.capture(self.root)
        for schema in (1, True, "2"):
            with self.assertRaises(ValueError):
                S.validate(dict(ctx, schema=schema))
        for path in ("../secret.kt", "/absolute.kt", "C:/outside.kt", "docs/example.kt",
                     S.SOURCE_PREFIX + "../escape.kt", S.SOURCE_PREFIX + "foo\\bar.kt",
                     S.SOURCE_PREFIX + "hidden.env", S.SOURCE_PREFIX + "file:stream.kt",
                     S.SOURCE_PREFIX + "control\nname.kt"):
            invalid = copy.deepcopy(ctx)
            invalid["source_records"][0]["path"] = path
            with self.assertRaisesRegex(ValueError, "allowlist"):
                S.validate(invalid)
        for records in ([], ctx["source_records"][::-1], [*ctx["source_records"], ctx["source_records"][0]]):
            with self.assertRaises(ValueError):
                S.validate(dict(ctx, source_records=records))

    def test_bounds_are_enforced_by_capture_and_validator(self):
        ctx = S.capture(self.root)
        for name, limit in (("MAX_FILES", 1), ("MAX_FILE_BYTES", 3), ("MAX_TOTAL_BYTES", 10)):
            with patch.object(S, name, limit):
                with self.assertRaises(ValueError):
                    S.capture(self.root)
                with self.assertRaises(ValueError):
                    S.validate(ctx)
        for attempts in (0, 11, True):
            with self.assertRaises(ValueError):
                S.capture(self.root, max_attempts=attempts)

    def test_empty_production_tree_is_rejected(self):
        self.one.unlink()
        with self.assertRaisesRegex(ValueError, "empty"):
            S.capture(self.root)

    def test_obvious_private_keys_tokens_and_secret_assignments_are_rejected_without_values(self):
        examples = ["-----BEGIN PRIVATE KEY-----", "-----BEGIN RSA PRIVATE KEY-----",
                    "hf_" + "aB7" * 12, "ghp_" + "cD8" * 12, "github_pat_" + "eF9" * 24,
                    "sk-proj-" + "gH1" * 16, 'const val API_KEY = "' + "kL2" * 12 + '"',
                    'const val AUTH_TOKEN = "' + "mN3" * 12 + '"',
                    'const val PASSWORD = "' + "oP4" * 12 + '"']
        clean = S.capture(self.root)
        for secret in examples:
            self.one.write_bytes(secret.encode("utf-8"))
            with self.assertRaisesRegex(ValueError, "Source secret gate rejected") as error:
                S.capture(self.root)
            self.assertNotIn(secret, str(error.exception))
            self.assertIn(self.one.relative_to(self.root).as_posix(), str(error.exception))
            tampered = copy.deepcopy(clean)
            record = next(r for r in tampered["source_records"] if r["path"].endswith("PlainAdapter.kt"))
            record.update(source=secret, bytes=len(secret.encode("utf-8")),
                          sha256=hashlib.sha256(secret.encode("utf-8")).hexdigest())
            tampered["source_tree_sha256"] = S._tree_identity(tampered["repository_head"], tampered["source_records"])
            with self.assertRaisesRegex(ValueError, "Source secret gate rejected"):
                S.validate(tampered)

    def test_public_keys_and_explicit_placeholders_are_allowed(self):
        text = ('const val PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----' + "aB7" * 24 + '"\n' +
                'const val API_KEY = "your_api_key_here_with_placeholder"\n' +
                'const val TOKEN = "placeholder_token_for_configuration"\n' +
                'const val PASSWORD = "replace_password_before_use_0000"\n' +
                'val token = "${context.packageName}.action"\n' +
                'const val KEY_PROVIDER_API_KEY = "settings_provider_api_key_2"\n' +
                '// hf_' + "x" * 40 + '\n// sk-' + "0" * 40)
        self.one.write_bytes(text.encode("utf-8"))
        S.validate(S.capture(self.root))

    def test_external_file_and_directory_links_are_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        target = outside / "External.kt"
        target.write_bytes(b"outside source")
        link = self.source / "External.kt"
        try:
            link.symlink_to(target)
        except OSError as error:
            self.skipTest("Symlink creation unavailable: " + type(error).__name__)
        with self.assertRaisesRegex(ValueError, "links or junctions"):
            S.capture(self.root)
        link.unlink()
        link = self.source / "linked"
        link.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "links or junctions"):
            S.capture(self.root)

    def test_reparse_probe_stops_the_walker_before_source_reads(self):
        external = self.source / "external"
        external.mkdir()
        (external / "Hidden.kt").write_bytes(b"external source")
        original = S._linked
        def linked(path):
            return path == external or original(path)
        with patch.object(S, "_linked", side_effect=linked), patch.object(Path, "open") as opened:
            with self.assertRaisesRegex(ValueError, "links or junctions"):
                S._paths(self.root)
            opened.assert_not_called()

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior")
    def test_windows_external_junction_is_rejected_without_traversal(self):
        outside = self.root / "outside-junction"
        outside.mkdir()
        (outside / "External.kt").write_bytes(b"outside source")
        link = self.source / "junction"
        self.assertTrue(link.absolute().is_relative_to(self.root))
        self.assertTrue(outside.resolve().is_relative_to(self.root))
        command = ("New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") +
                   "' -Target '" + str(outside).replace("'", "''") + "' | Out-Null")
        subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                       capture_output=True, check=True, timeout=30)
        try:
            with patch.object(S, "_read_records", wraps=S._read_records) as reader:
                with self.assertRaisesRegex(ValueError, "links or junctions"):
                    S.capture(self.root)
                self.assertEqual(reader.call_count, 1)
            self.assertEqual((outside / "External.kt").read_bytes(), b"outside source")
        finally:
            link.rmdir()

    def test_public_metadata_redacts_sources_and_unapproved_binding_values(self):
        self.one.write_bytes(b"unique-private-source-value")
        ctx = S.capture(self.root)
        binding = {"schema": 1, "repo": "private/source", "revision": "a" * 40,
                   "path": "sources/snapshot.json", "snapshot_sha256": "b" * 64,
                   "source_tree_sha256": ctx["source_tree_sha256"], "repository_head": ctx["repository_head"],
                   "captured_at": ctx["captured_at"], "verified_at": ctx["captured_at"], "origin": "worktree",
                   "working_tree_dirty": True, "file_count": len(ctx["source_records"]), "selection_version": 1}
        public = S.public_context(ctx, dict(binding, token="unique-secret-value", source="unique-private-source-value"))
        encoded = json.dumps(public)
        self.assertNotIn("unique-private-source-value", encoded)
        self.assertNotIn("unique-secret-value", encoded)
        self.assertEqual(public["binding"], binding)
        self.assertTrue(all("source" not in record for record in public["source_records"]))
        self.assertEqual(S.public_context(public), S.public_context(ctx))

    def test_compare_reports_current_drift_unavailable_and_legacy_without_source(self):
        public = S.public_context(S.capture(self.root))
        self.assertEqual(S.compare(public, self.root)["status"], "current")
        extra = self.source / "New.kt"
        extra.write_bytes(b"new-private")
        fixed = self.root / S.FIXED_PATHS[0]
        fixed.unlink()
        self.one.write_bytes(b"changed-private")
        result = S.compare(public, self.root)
        self.assertEqual(result["status"], "drift")
        self.assertEqual(result["changed"], [self.one.relative_to(self.root).as_posix()])
        self.assertEqual(result["added"], [extra.relative_to(self.root).as_posix()])
        self.assertEqual(result["removed"], [S.FIXED_PATHS[0]])
        self.assertNotIn("private", json.dumps(result))
        self.assertEqual(S.compare(public, self.root / "missing")["status"], "unavailable")
        self.assertEqual(S.compare({"source_records": []}, self.root)["status"], "legacy")
        self.assertEqual(S.compare(dict(public, selection_version=99), self.root)["status"], "unavailable")

    def test_cli_import_has_no_io_and_cli_prints_only_metadata(self):
        import snapshot_context
        with patch.object(S, "capture") as capture, patch.object(Path, "write_bytes") as write:
            importlib.reload(snapshot_context)
            capture.assert_not_called()
            write.assert_not_called()
        output = self.root / "output/context.json"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(snapshot_context.main(["--root", str(self.root), "--output", str(output)]), 0)
        raw = output.read_bytes()
        ctx = json.loads(raw)
        metadata = json.loads(stdout.getvalue())
        self.assertNotIn("source_records", ctx["source_records"][0])
        self.assertNotIn("PlainAdapter", stdout.getvalue())
        self.assertEqual(metadata["snapshot_sha256"], hashlib.sha256(raw).hexdigest())
        S.validate(ctx, metadata["snapshot_sha256"])


if __name__ == "__main__":
    unittest.main()
