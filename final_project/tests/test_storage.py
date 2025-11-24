import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Ensure `src` is on sys.path so `final_project` package can be imported
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "src"))

from final_project import storage


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="fp_store_")
        storage.DATA_DIR = Path(self.tmpdir)
        storage.TASKS_FILE = storage.DATA_DIR / "tasks.json"
        storage.NOTES_FILE = storage.DATA_DIR / "notes.json"
        storage.ensure_data_dir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_load_missing_returns_empty(self):
        # ensure no file exists
        p = storage.DATA_DIR / "nope.json"
        data = storage.load_json(p, "tasks")
        self.assertEqual(data, {"tasks": []})

    def test_save_and_load_tasks(self):
        d = {"tasks": [{"id": "1", "title": "t"}]}
        storage.save_json(storage.TASKS_FILE, d)
        loaded = storage.load_json(storage.TASKS_FILE, "tasks")
        self.assertIn("tasks", loaded)
        self.assertIsInstance(loaded["tasks"], list)


if __name__ == "__main__":
    unittest.main()
