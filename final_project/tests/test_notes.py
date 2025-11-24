import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Ensure package import works from src
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "src"))

from final_project import notes, storage


class NotesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="fp_notes_")
        storage.DATA_DIR = Path(self.tmpdir)
        storage.TASKS_FILE = storage.DATA_DIR / "tasks.json"
        storage.NOTES_FILE = storage.DATA_DIR / "notes.json"
        storage.ensure_data_dir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_create_list_get_edit_search_remove(self):
        data = {"notes": []}
        data = notes.create_note(data, title="Note 1", body="This is a test note.")
        self.assertEqual(len(data["notes"]), 1)
        n = data["notes"][0]
        self.assertEqual(n["title"], "Note 1")

        listed = notes.list_notes(data)
        self.assertTrue(any(item["id"] == n["id"] for item in listed))

        got = notes.get_note(data, n["id"])
        self.assertIsNotNone(got)

        data = notes.edit_note(data, n["id"], title="Updated")
        edited = notes.get_note(data, n["id"])
        self.assertEqual(edited["title"], "Updated")

        results = notes.search_notes(data, "test")
        self.assertTrue(any(r["id"] == n["id"] for r in results))

        data = notes.remove_note(data, n["id"])
        self.assertIsNone(notes.get_note(data, n["id"]))


if __name__ == "__main__":
    unittest.main()
import sys
from pathlib import Path

# Ensure package import works from src/
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "src"))

from final_project import notes


def test_create_list_get_edit_remove_search():
    data = {"notes": []}

    # create
    data = notes.create_note(data, title="Note 1", body="This is a test note.")
    assert len(data["notes"]) == 1
    n = data["notes"][0]
    assert n["title"] == "Note 1"

    # list
    listed = notes.list_notes(data)
    assert any(item["id"] == n["id"] for item in listed)

    # get
    got = notes.get_note(data, n["id"])
    assert got is not None and got["id"] == n["id"]

    # edit
    data = notes.edit_note(data, n["id"], title="Updated")
    edited = notes.get_note(data, n["id"])
    assert edited["title"] == "Updated"

    # search
    results = notes.search_notes(data, "test")
    assert any(r["id"] == n["id"] for r in results)

    # remove
    data = notes.remove_note(data, n["id"])
    assert notes.get_note(data, n["id"]) is None
