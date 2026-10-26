import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
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
            {"README.md", "AGENTS.md", "ARCHITECTURE.md", "STATE.md"},
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

    def test_evidence_check_rejects_broken_source_claims(self):
        init_memory(self.root, self.memory)
        source = self.root / "service.py"
        source.write_text("def actual_decision():\n    return True\n", encoding="utf-8")
        state = self.memory / "STATE.md"
        state.write_text(
            "Evidence: path=missing.py symbol=run\n"
            "Evidence: path=service.py symbol=wrong_decision\n"
            "Evidence: path=../outside.py symbol=secret\n",
            encoding="utf-8",
        )
        errors, warnings, checked = check_memory(self.root, self.memory)
        self.assertEqual(warnings, [])
        self.assertEqual(checked, 3)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("missing evidence path" in error for error in errors))
        self.assertTrue(any("not found" in error for error in errors))
        self.assertTrue(any("escapes source repository" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
