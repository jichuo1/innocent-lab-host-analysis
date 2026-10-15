"""Tooling CI reuses dependency bytes without skipping its real runtime checks."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CACHE_ACTION = "caa296126883cff596d87d8935842f9db880ef25"
CACHE_KEY = "hostlab-runtime-v1-${{ runner.os }}-${{ runner.arch }}-${{ steps.runtime-key.outputs.fingerprint }}"


class ToolingRuntimeWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / ".github/workflows/tooling-tests.yml").read_text(encoding="utf-8")

    def step(self, name):
        marker = "      - name: " + name + "\n"
        self.assertEqual(self.text.count(marker), 1, name)
        return self.text.split(marker, 1)[1].split("      - ", 1)[0]

    def test_full_suite_and_pinned_dependencies_remain_before_runtime_smoke(self):
        self.assertIn("python-version: '3.13'", self.text)
        self.assertIn("python -m pip install -r tools/hostlab/requirements.txt", self.text)
        suite = self.step("Offline source, dispatch, AI and report checks")
        self.assertIn("working-directory: tools/hostlab", suite)
        self.assertIn("python -B -m unittest discover -p 'test_*.py' -v", suite)
        names = ["Offline source, dispatch, AI and report checks", "Fingerprint dependency runtime",
                 "Restore verified dependency runtime", "Prepare and verify query dependencies",
                 "Verify actual isolated runtime and prepared bytecode", "Save verified dependency runtime"]
        positions = [self.text.index("      - name: " + name + "\n") for name in names]
        self.assertEqual(positions, sorted(positions))

    def test_cache_identity_and_dependency_only_path_match_analysis_workflow(self):
        analysis = (ROOT / ".github/workflows/host-analysis.yml").read_text(encoding="utf-8")
        for name, action in (("Restore verified dependency runtime", "restore"),
                             ("Save verified dependency runtime", "save")):
            block = self.step(name)
            self.assertIn("actions/cache/" + action + "@" + CACHE_ACTION, block)
            self.assertIn("continue-on-error: true", block)
            self.assertIn("path: runtime/hostlab-prepared", block)
            self.assertIn("key: " + CACHE_KEY, block)
            self.assertNotIn("restore-keys:", block)
        self.assertIn("key: " + CACHE_KEY, analysis)
        self.assertIn("prepare_runtime.py fingerprint --requirements requirements-query.txt",
                      self.step("Fingerprint dependency runtime"))

    def test_only_successful_trusted_main_push_may_write_the_verified_cache(self):
        block = self.step("Save verified dependency runtime")
        guard = "if: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' && " \
                "github.repository == 'jichuo1/innocent-lab-host-analysis' && " \
                "steps.runtime.outputs.built == 'true' && steps.runtime-cache.outputs.cache-hit != 'true' }}"
        self.assertIn(guard, block)
        self.assertNotIn("always()", block)
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertNotIn("secrets.", self.text)
        self.assertNotIn("contents: write", self.text)

    def test_cached_bytes_are_verified_before_real_mcp_and_second_hit_check(self):
        prepare = self.step("Prepare and verify query dependencies")
        self.assertIn("id: runtime", prepare)
        self.assertIn("prepare_runtime.py prepare --requirements requirements-query.txt", prepare)
        smoke = self.step("Verify actual isolated runtime and prepared bytecode")
        self.assertIn("runtime/hostlab-prepared/env/bin/python -B tools/hostlab/test_remote_mcp.py", smoke)
        self.assertIn("assert p.verify(p.directory(),identity,fingerprint)", smoke)
        self.assertIn("assert p.prepare('requirements-query.txt')['cache_hit']", smoke)
        self.assertIn("PYTHONDONTWRITEBYTECODE: '1'", self.text.split("    steps:", 1)[0])


if __name__ == "__main__":
    unittest.main()
