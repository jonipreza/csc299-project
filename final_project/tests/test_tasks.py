import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Ensure package import works from src
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "src"))

from final_project import tasks, storage


class TaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="fp_tests_")
        # override storage paths to isolate from real data
        storage.DATA_DIR = Path(self.tmpdir)
        storage.TASKS_FILE = storage.DATA_DIR / "tasks.json"
        storage.NOTES_FILE = storage.DATA_DIR / "notes.json"
        storage.ensure_data_dir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_create_task(self):
        data = {"tasks": []}
        data = tasks.create_task(data, title="T1", description="desc1", tags=["a"])
        self.assertEqual(len(data["tasks"]), 1)
        t = data["tasks"][0]
        self.assertEqual(t["title"], "T1")

    def test_list_filters_and_mark_remove(self):
        data = {"tasks": []}
        data = tasks.create_task(data, title="A", description="", tags=["x"])  # id 1
        data = tasks.create_task(data, title="B", description="", tags=["y"])  # id 2
        # mark task 1 done
        tid1 = data["tasks"][0]["id"]
        data = tasks.mark_done(data, tid1)
        # list completed
        completed = tasks.list_tasks(data, status="completed")
        self.assertTrue(any(t["id"] == tid1 for t in completed))
        # list pending
        pending = tasks.list_tasks(data, status="pending")
        self.assertTrue(all(not t["completed"] for t in pending))
        # filter by tag
        tag_x = tasks.list_tasks(data, status="all", tag="x")
        self.assertTrue(any(t["id"] == tid1 for t in tag_x))
        # remove
        data = tasks.remove_task(data, tid1)
        self.assertFalse(any(t["id"] == tid1 for t in data["tasks"]))


if __name__ == "__main__":
    unittest.main()
import sys
from pathlib import Path

# Ensure package import works from src/
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "src"))

from final_project import tasks


def test_create_list_mark_edit_remove():
    data = {"tasks": []}

    # create
    data = tasks.create_task(data, title="Write tests", description="Write tests for tasks module")
    assert len(data["tasks"]) == 1
    t = data["tasks"][0]
    assert t["title"] == "Write tests"

    # list
    listed = tasks.list_tasks(data)
    assert any(item["id"] == t["id"] for item in listed)

    # mark done
    data = tasks.mark_done(data, t["id"])
    done_task = next(item for item in data["tasks"] if item["id"] == t["id"])
    assert done_task["completed"] is True
    assert done_task["completed_at"] is not None

    # edit
    data = tasks.edit_task(data, t["id"], title="New title", tags=["x", "y"]) 
    edited = next(item for item in data["tasks"] if item["id"] == t["id"])
    assert edited["title"] == "New title"
    assert edited["tags"] == ["x", "y"]

    # remove
    data = tasks.remove_task(data, t["id"])
    assert not any(item["id"] == t["id"] for item in data["tasks"])
