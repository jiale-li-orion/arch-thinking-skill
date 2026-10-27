import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "arch-thinking-skill" / "scripts"))
from arch_memory import check_memory, init_memory, impact_memory


class ArchitectureMemoryLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "source"
        self.memory = Path(self.temp.name) / "architecture-memory"
        self.root.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def test_external_memory_lifecycle_survives_source_evolution(self):
        self.git("init", "-q")
        self.git("config", "user.name", "Skill Test")
        self.git("config", "user.email", "skill-test@example.invalid")
        source = self.root / "src" / "dialogue.py"
        source.parent.mkdir()
        source.write_text("def classify_request():\n    return 'follow_up'\n", encoding="utf-8")
        self.git("add", "src/dialogue.py")
        self.git("commit", "-qm", "implement dialogue decision")
        source_revision = self.git("rev-parse", "--short", "HEAD")

        created = init_memory(self.root, self.memory)
        self.assertEqual(
            {path.name for path in created},
            {"README.md", "AGENTS.md", "engineering-thinking.md", "ARCHITECTURE.md", "STATE.md"},
        )
        self.assertFalse((self.root / ".arch").exists())

        architecture = self.memory / "ARCHITECTURE.md"
        architecture.write_text("# Reviewed system boundary\n", encoding="utf-8")
        self.assertEqual(init_memory(self.root, self.memory), [])
        self.assertEqual(architecture.read_text(encoding="utf-8"), "# Reviewed system boundary\n")

        flow = self.memory / "flows" / "dialogue.md"
        flow.parent.mkdir()
        flow.write_text(
            f"The dialogue decision emits a follow-up action.\n"
            f"Evidence: path=src/dialogue.py symbol=classify_request at={source_revision}\n",
            encoding="utf-8",
        )
        errors, warnings, checked = check_memory(self.root, self.memory)
        self.assertEqual((errors, warnings, checked), ([], [], 1))

        affected, errors = impact_memory(self.root, ["src/dialogue.py"], self.memory)
        self.assertEqual(errors, [])
        self.assertEqual(affected, [(flow, ["src/dialogue.py"])])

        source.write_text("def classify_request():\n    return 'end_session'\n", encoding="utf-8")
        self.git("add", "src/dialogue.py")
        self.git("commit", "-qm", "change dialogue decision")
        errors, warnings, checked = check_memory(self.root, self.memory)
        self.assertEqual(errors, [])
        self.assertEqual(checked, 1)
        self.assertTrue(any("changed after" in warning for warning in warnings))

    def test_workspace_init_preserves_project_and_checks_real_evidence(self):
        readme = self.root / "README.md"
        readme.write_text("# Existing project\nKeep this contract.\n", encoding="utf-8")
        init_memory(self.root)
        self.assertEqual(readme.read_text(encoding="utf-8"), "# Existing project\nKeep this contract.\n")
        self.assertFalse((self.root / ".arch").exists())
        source = self.root / "service.py"
        source.write_text("def actual_decision():\n    return True\n", encoding="utf-8")
        state = self.root / "STATE.md"
        state.write_text(
            "Evidence: path=missing.py symbol=run\n"
            "Evidence: path=service.py symbol=wrong_decision\n"
            "Evidence: path=../outside.py symbol=secret\n",
            encoding="utf-8",
        )
        unrelated = self.root / "docs" / "release.md"
        unrelated.parent.mkdir()
        unrelated.write_text("Evidence: path=release-only.py\n", encoding="utf-8")
        flow = self.root / "flows" / "service.md"
        flow.parent.mkdir()
        flow.write_text("Evidence: path=service.py symbol=actual_decision\n", encoding="utf-8")
        errors, warnings, checked = check_memory(self.root)
        self.assertEqual(warnings, [])
        self.assertEqual(checked, 4)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("missing evidence path" in error for error in errors))
        self.assertTrue(any("not found" in error for error in errors))
        self.assertTrue(any("escapes source repository" in error for error in errors))
        hits, errors = impact_memory(self.root, ["service.py"])
        self.assertEqual(errors, [])
        self.assertEqual(hits, [(state, ["service.py"]), (flow, ["service.py"])])

    def test_existing_legacy_workspace_keeps_its_evidence_and_state(self):
        legacy = self.root / ".arch"
        legacy.mkdir()
        legacy_method = legacy / "工程思维.md"
        legacy_method.write_text("# Original project-specific engineering rules\n", encoding="utf-8")
        state = legacy / "STATE.md"
        state.write_text("Existing task and recovery point\n", encoding="utf-8")
        source = self.root / "worker.py"
        source.write_text("def execute():\n    return 1\n", encoding="utf-8")
        (legacy / "ARCHITECTURE.md").write_text(
            "Evidence: path=worker.py symbol=execute\n", encoding="utf-8"
        )
        init_memory(self.root)
        self.assertEqual(state.read_text(encoding="utf-8"), "Existing task and recovery point\n")
        self.assertEqual(legacy_method.read_text(encoding="utf-8"), "# Original project-specific engineering rules\n")
        self.assertFalse((legacy / "engineering-thinking.md").exists())
        self.assertIn("工程思维.md", (legacy / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "ARCHITECTURE.md").exists())
        self.assertEqual(check_memory(self.root), ([], [], 1))
        hits, errors = impact_memory(self.root, ["worker.py"])
        self.assertEqual(errors, [])
        self.assertEqual(hits, [(legacy / "ARCHITECTURE.md", ["worker.py"])])


if __name__ == "__main__":
    unittest.main()
