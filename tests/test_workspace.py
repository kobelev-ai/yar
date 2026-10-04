"""Data-preservation tests for actual filesystem operations, without model calls."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("yar_workspace", REPO / "scripts/yar_workspace.py")
yar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yar)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode())
        return path

    def test_reinitialization_preserves_all_existing_data(self):
        yar.initialize(self.root, "Existing owner")
        for path in ["ops/tasks/todo.md", "context/me.md", "ops/meetings/index.json", "context/me/decisions.md"]:
            self.write(path, "Owner's actual content\n")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(yar.initialize(self.root, "Another name"), [])
        for path, content in before.items():
            self.assertEqual((self.root / path).read_bytes(), content)

    def test_existing_queue_paths_are_respected(self):
        self.write("ops/tasks/review/queues.json", json.dumps({"closures": "ops/tasks/review/custom.md", "insights": "ops/tasks/review/custom_ideas.md"}))
        yar.initialize(self.root)
        self.assertTrue((self.root / "ops/tasks/review/custom.md").is_file())
        self.assertFalse((self.root / "ops/tasks/review/closures.md").exists())

    def test_legacy_init_requires_migration_before_second_todo(self):
        old = self.write("tasks/todo.md", "- [ ] Actual commitment\n")
        with self.assertRaises(ValueError):
            yar.initialize(self.root)
        self.assertTrue(old.exists())
        self.assertFalse((self.root / "ops/tasks/todo.md").exists())

    def test_nested_task_reuses_current_pointer_and_keeps_inputs(self):
        folder = yar.create_task(self.root, "Customer/Compare", "Compare these proposals")
        original = self.write("tasks/Customer/Compare/materials/Proposal.pdf", b"original input")
        readme = folder / "README.md"
        readme.write_text("Current result: result.md; resume from here.")
        yar.create_task(self.root, "Customer/Compare", "Changed goal")
        self.assertEqual(original.read_bytes(), b"original input")
        self.assertEqual(readme.read_text(), "Current result: result.md; resume from here.")

    def test_task_rejects_parent_paths_and_symlink_escape(self):
        for name in ["../escape", "/outside", ".", "a/../b", ""]:
            with self.assertRaises(ValueError):
                yar.create_task(self.root, name)
        (self.root / "tasks").mkdir()
        (self.root / "tasks/linked").symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            yar.create_task(self.root, "linked/escape")

    def test_demo_is_separate_and_repeated_runs_never_reset_main(self):
        yar.initialize(self.root)
        live = self.write("ops/tasks/todo.md", "- [ ] Real confidential commitment\n")
        first = yar.create_demo(self.root)
        second = yar.create_demo(self.root)
        self.assertNotEqual(first, second)
        self.assertEqual(live.read_text(), "- [ ] Real confidential commitment\n")
        self.assertTrue((first / ".yar-root").exists())
        inputs = first / "tasks/Compare_proposals"
        self.assertEqual(len(list(inputs.glob("offer_*.md"))), 2)
        self.assertIn("fictional", (first / "context/me.md").read_text().lower())
        subprocess.run(["python3", str(first / "scripts/yar_workspace.py"), "--root", str(first), "init"], check=True, capture_output=True)

    def test_root_is_found_from_inside_task_and_explicit_wins(self):
        yar.initialize(self.root)
        nested = yar.create_task(self.root, "Nested/Work")
        before = Path.cwd()
        try:
            os.chdir(nested)
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(yar.workspace_root(), self.root)
                self.assertEqual(yar.workspace_root(str(self.root / "other")), self.root / "other")
        finally:
            os.chdir(before)

    def legacy_files(self):
        self.write("tasks/todo.md", b"- [ ] Keep this\n- [x] Already done\n")
        self.write("tasks/archive/2026-W20.md", b"- [x] Original archived action\n")
        self.write("context/meetings/processed/Meeting original.txt", b"Speaker 1: original wording\n")
        self.write("context/meetings/index.json", json.dumps([{"file": "context/meetings/processed/Meeting original.txt"}]))
        self.write("context/meetings/speaker_mappings.json", "{}")

    def test_migration_preview_does_not_change_files(self):
        self.legacy_files()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = yar.migrate(self.root)
        self.assertFalse(result["applied"])
        self.assertEqual(len(result["moves"]), 5)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_migration_preserves_content_backups_and_resolves_index(self):
        self.legacy_files()
        original_todo = (self.root / "tasks/todo.md").read_bytes()
        result = yar.migrate(self.root, apply=True)
        self.assertEqual((self.root / "ops/tasks/todo.md").read_bytes(), original_todo)
        self.assertFalse((self.root / "tasks/todo.md").exists())
        index = json.loads((self.root / "ops/meetings/index.json").read_text())
        self.assertEqual(index[0]["file"], "ops/meetings/processed/Meeting original.txt")
        self.assertTrue((self.root / index[0]["file"]).is_file())
        backup = Path(result["backup"])
        for row in json.loads((backup / "manifest.json").read_text()):
            self.assertEqual(yar.digest(backup / "originals" / row["from"]), row["sha256"])
        self.assertEqual(yar.migrate(self.root, apply=True)["moves"], [])
        self.assertEqual((self.root / "ops/tasks/todo.md").read_bytes(), original_todo)

    def test_migration_conflict_stops_before_any_move(self):
        self.legacy_files()
        self.write("ops/meetings/speaker_mappings.json", '{"actual": "map"}')
        with self.assertRaises(ValueError):
            yar.migrate(self.root, apply=True)
        self.assertTrue((self.root / "tasks/todo.md").is_file())
        self.assertFalse((self.root / "ops/tasks/todo.md").exists())
        self.assertFalse((self.root / ".yar/backups").exists())

    def test_invalid_legacy_json_stops_before_any_move(self):
        self.legacy_files()
        self.write("context/meetings/index.json", "invalid json")
        with self.assertRaises(ValueError):
            yar.migrate(self.root, apply=True)
        self.assertTrue((self.root / "tasks/todo.md").is_file())
        self.assertFalse((self.root / "ops/tasks/todo.md").exists())

    def test_failed_migration_restores_originals(self):
        self.legacy_files()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch.object(yar, "initialize", side_effect=OSError("simulated initialization failure")):
            with self.assertRaises(OSError):
                yar.migrate(self.root, apply=True)
        for path, data in before.items():
            self.assertEqual((self.root / path).read_bytes(), data)
        self.assertFalse((self.root / "ops/tasks/todo.md").exists())

    def test_symlink_legacy_source_is_not_moved(self):
        self.write("external.txt", "original")
        (self.root / "tasks").mkdir()
        (self.root / "tasks/todo.md").symlink_to(self.root / "external.txt")
        with self.assertRaises(ValueError):
            yar.migrate(self.root, apply=True)
        self.assertEqual((self.root / "external.txt").read_text(), "original")

    def test_distribution_contract_and_data_exclusions(self):
        self.assertEqual((REPO / "AGENTS.md").read_bytes(), (REPO / "CLAUDE.md").read_bytes())
        private = ["tasks/Client/input.pdf", "tasks/Client/README.md", "ops/tasks/todo.md",
                   "ops/tasks/review/closures.md", "ops/meetings/index.json",
                   "context/me.md", ".yar/installed.md", "demos/test/README.md"]
        result = subprocess.run(["git", "check-ignore", "--no-index", "--stdin"], cwd=REPO,
                                input="\n".join(private) + "\n", text=True, capture_output=True, check=True)
        self.assertEqual(set(result.stdout.splitlines()), set(private))

    def test_fetcher_paths_use_workspace_marker_and_validate_configuration(self):
        fetch_spec = importlib.util.spec_from_file_location("fetch_paths", REPO / "scripts/plaud_fetcher/paths.py")
        paths = importlib.util.module_from_spec(fetch_spec)
        fetch_spec.loader.exec_module(paths)
        yar.initialize(self.root)
        inbox = self.root / "custom/import/inbox"
        actual, processed = paths.transcript_paths({"MEETINGS_INBOX": str(inbox)})
        self.assertEqual(actual, inbox)
        self.assertEqual(processed, self.root / "ops/meetings/processed")
        explicit = self.root / "other-processed"
        self.assertEqual(paths.transcript_paths({"MEETINGS_INBOX": str(inbox), "MEETINGS_PROCESSED": str(explicit)})[1], explicit)
        for config in [{}, {"MEETINGS_INBOX": " "}, {"MEETINGS_INBOX": "relative/path"}]:
            with self.assertRaises(ValueError):
                paths.transcript_paths(config)


if __name__ == "__main__":
    unittest.main()
