import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from arch_memory import check_memory, init_memory


class ArchMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_init_creates_only_core_files_and_does_not_overwrite(self):
        created = init_memory(self.root)
        self.assertEqual({p.name for p in created}, {"README.md", "AGENTS.md", "ARCHITECTURE.md", "STATE.md"})
        architecture = self.root / ".arch" / "ARCHITECTURE.md"
        architecture.write_text("human-maintained", encoding="utf-8")
        self.assertEqual(init_memory(self.root), [])
        self.assertEqual(architecture.read_text(encoding="utf-8"), "human-maintained")

    def test_valid_evidence_path_and_symbol(self):
        init_memory(self.root)
        source = self.root / "src" / "service.py"
        source.parent.mkdir()
        source.write_text("def classify_request():\n    return True\n", encoding="utf-8")
        note = self.root / ".arch" / "flows" / "dialogue.md"
        note.parent.mkdir()
        note.write_text(
            "Evidence: path=src/service.py symbol=classify_request\n",
            encoding="utf-8",
        )
        errors, warnings, checked = check_memory(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(checked, 1)

    def test_missing_path_is_error(self):
        init_memory(self.root)
        note = self.root / ".arch" / "STATE.md"
        note.write_text("Evidence: path=src/missing.py symbol=run\n", encoding="utf-8")
        errors, _, checked = check_memory(self.root)
        self.assertEqual(checked, 1)
        self.assertIn("missing evidence path", errors[0])

    def test_missing_symbol_is_error(self):
        init_memory(self.root)
        source = self.root / "service.py"
        source.write_text("def actual_name():\n    pass\n", encoding="utf-8")
        note = self.root / ".arch" / "STATE.md"
        note.write_text("Evidence: path=service.py symbol=wrong_name\n", encoding="utf-8")
        errors, _, _ = check_memory(self.root)
        self.assertIn("not found", errors[0])

    def test_path_escape_is_error(self):
        init_memory(self.root)
        note = self.root / ".arch" / "STATE.md"
        note.write_text("Evidence: path=../outside.py symbol=foo\n", encoding="utf-8")
        errors, _, _ = check_memory(self.root)
        self.assertIn("escapes repository", errors[0])

    def test_impact_finds_notes_that_cite_changed_files(self):
        init_memory(self.root)
        source = self.root / "src" / "service.py"
        source.parent.mkdir()
        source.write_text("def classify_request():\n    return True\n", encoding="utf-8")
        note = self.root / ".arch" / "flows" / "dialogue.md"
        note.parent.mkdir()
        note.write_text(
            "Evidence: path=src/service.py symbol=classify_request\n",
            encoding="utf-8",
        )
        from arch_memory import impact_memory
        results, errors = impact_memory(self.root, ["src/service.py"])
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], note)
        self.assertEqual(results[0][1], ["src/service.py"])

    def test_impact_ignores_paths_outside_repository(self):
        init_memory(self.root)
        from arch_memory import impact_memory
        results, errors = impact_memory(self.root, ["../outside.py"])
        self.assertEqual(results, [])
        self.assertIn("outside repository", errors[0])

    def test_source_change_after_recorded_commit_is_stale_warning(self):
        import subprocess

        def run(*args):
            return subprocess.run(args, cwd=self.root, check=True, capture_output=True, text=True)

        run("git", "init", "-q")
        run("git", "config", "user.name", "Skill Test")
        run("git", "config", "user.email", "skill-test@example.invalid")
        source = self.root / "src" / "service.py"
        source.parent.mkdir()
        source.write_text("def classify_request():\n    return 1\n", encoding="utf-8")
        run("git", "add", "src/service.py")
        run("git", "commit", "-qm", "add source")
        evidence_commit = run("git", "rev-parse", "--short", "HEAD").stdout.strip()
        init_memory(self.root)
        note = self.root / ".arch" / "STATE.md"
        note.write_text(
            f"Evidence: path=src/service.py symbol=classify_request at={evidence_commit}\n",
            encoding="utf-8",
        )
        run("git", "add", ".arch/STATE.md")
        run("git", "commit", "-qm", "record evidence")
        source.write_text("def classify_request():\n    return 2\n", encoding="utf-8")
        run("git", "add", "src/service.py")
        run("git", "commit", "-qm", "change behavior")
        errors, warnings, checked = check_memory(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(checked, 1)
        self.assertTrue(any("changed after" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
