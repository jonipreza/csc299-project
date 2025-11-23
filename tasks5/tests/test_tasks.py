"""Unit tests for tasks-manager."""
import sys
import os
import unittest
import tempfile

# Ensure the package root is importable when tests are executed directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tasks5 import tasks, storage


class TestTasks(unittest.TestCase):
    def test_add_and_list(self):
        data = {"tasks": []}
        tasks.add_task(data, "Buy milk", description="2 liters")
        self.assertEqual(len(data["tasks"]), 1)
        t = data["tasks"][0]
        self.assertEqual(t["title"], "Buy milk")
        self.assertFalse(t["completed"])

    def test_done_updates(self):
        data = {"tasks": []}
        tasks.add_task(data, "Task A")
        tid = data["tasks"][0]["id"]
        tasks.update_task(data, tid, completed=True)
        t = tasks.get_task(data, tid)
        self.assertTrue(t["completed"])
        self.assertIsNotNone(t["completed_at"])

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.json")
            data = {"tasks": []}
            tasks.add_task(data, "X")
            storage.save_tasks(path, data)
            loaded = storage.load_tasks(path)
            self.assertEqual(len(loaded.get("tasks", [])), 1)

    def test_recover_from_corrupt(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.json")
            # write a valid file first
            data = {"tasks": []}
            tasks.add_task(data, "Valid")
            storage.save_tasks(path, data)
            # corrupt primary file
            with open(path, "w") as f:
                f.write("{ not json")
            # load should recover from bak
            loaded = storage.load_tasks(path)
            self.assertEqual(len(loaded.get("tasks", [])), 1)


if __name__ == "__main__":
    unittest.main()
import unittest
import tempfile
import os
import json

from tasks5 import tasks, storage


class TestTasks(unittest.TestCase):
    def test_add_and_list(self):
        import unittest
        import tempfile
        import os

        from tasks5 import tasks, storage


        class TestTasks(unittest.TestCase):
            def test_add_and_list(self):
                data = {"tasks": []}
                tasks.add_task(data, "Buy milk", description="2 liters")
                self.assertEqual(len(data["tasks"]), 1)
                t = data["tasks"][0]
                self.assertEqual(t["title"], "Buy milk")
                self.assertFalse(t["completed"])

            def test_done_updates(self):
                data = {"tasks": []}
                tasks.add_task(data, "Task A")
                tid = data["tasks"][0]["id"]
                tasks.update_task(data, tid, completed=True)
                t = tasks.get_task(data, tid)
                self.assertTrue(t["completed"])
                self.assertIsNotNone(t["completed_at"])

            def test_save_and_load(self):
                with tempfile.TemporaryDirectory() as d:
                    path = os.path.join(d, "t.json")
                    data = {"tasks": []}
                    tasks.add_task(data, "X")
                    storage.save_tasks(path, data)
                    loaded = storage.load_tasks(path)
                    self.assertEqual(len(loaded.get("tasks", [])), 1)

            def test_recover_from_corrupt(self):
                with tempfile.TemporaryDirectory() as d:
                    path = os.path.join(d, "t.json")
                    # write a valid file first
                    data = {"tasks": []}
                    tasks.add_task(data, "Valid")
                    storage.save_tasks(path, data)
                    import sys
                    import os
                    import unittest
                    import tempfile

                    # Ensure the project root is on sys.path so tests can import tasks5 when executed directly
                    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                    if ROOT not in sys.path:
                        sys.path.insert(0, ROOT)

                    from tasks5 import tasks, storage


                    class TestTasks(unittest.TestCase):
                        def test_add_and_list(self):
                            data = {"tasks": []}
                            tasks.add_task(data, "Buy milk", description="2 liters")
                            self.assertEqual(len(data["tasks"]), 1)
                            t = data["tasks"][0]
                            self.assertEqual(t["title"], "Buy milk")
                            self.assertFalse(t["completed"])

                        def test_done_updates(self):
                            data = {"tasks": []}
                            tasks.add_task(data, "Task A")
                            tid = data["tasks"][0]["id"]
                            tasks.update_task(data, tid, completed=True)
                            t = tasks.get_task(data, tid)
                            self.assertTrue(t["completed"])
                            self.assertIsNotNone(t["completed_at"])

                        def test_save_and_load(self):
                            with tempfile.TemporaryDirectory() as d:
                                path = os.path.join(d, "t.json")
                                data = {"tasks": []}
                                tasks.add_task(data, "X")
                                storage.save_tasks(path, data)
                                loaded = storage.load_tasks(path)
                                self.assertEqual(len(loaded.get("tasks", [])), 1)

                        def test_recover_from_corrupt(self):
                            with tempfile.TemporaryDirectory() as d:
                                path = os.path.join(d, "t.json")
                                # write a valid file first
                                data = {"tasks": []}
                                tasks.add_task(data, "Valid")
                                storage.save_tasks(path, data)
                                """Unit tests for tasks-manager.

                                These tests can be run via discovery or directly. When run directly, ensure the project root
                                is on sys.path so `from tasks5 import ...` works.
                                """
                                import sys
                                import os
                                import unittest
                                import tempfile

                                # If tests are executed directly, add project root to sys.path so `tasks5` imports work.
                                ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                                if ROOT not in sys.path:
                                    sys.path.insert(0, ROOT)

                                from tasks5 import tasks, storage


                                class TestTasks(unittest.TestCase):
                                    def test_add_and_list(self):
                                        data = {"tasks": []}
                                        tasks.add_task(data, "Buy milk", description="2 liters")
                                        self.assertEqual(len(data["tasks"]), 1)
                                        t = data["tasks"][0]
                                        self.assertEqual(t["title"], "Buy milk")
                                        self.assertFalse(t["completed"])

                                    def test_done_updates(self):
                                        data = {"tasks": []}
                                        tasks.add_task(data, "Task A")
                                        tid = data["tasks"][0]["id"]
                                        tasks.update_task(data, tid, completed=True)
                                        t = tasks.get_task(data, tid)
                                        self.assertTrue(t["completed"])
                                        self.assertIsNotNone(t["completed_at"])

                                    def test_save_and_load(self):
                                        with tempfile.TemporaryDirectory() as d:
                                            path = os.path.join(d, "t.json")
                                            data = {"tasks": []}
                                            tasks.add_task(data, "X")
                                            storage.save_tasks(path, data)
                                            loaded = storage.load_tasks(path)
                                            self.assertEqual(len(loaded.get("tasks", [])), 1)

                                    def test_recover_from_corrupt(self):
                                        with tempfile.TemporaryDirectory() as d:
                                            path = os.path.join(d, "t.json")
                                            # write a valid file first
                                            data = {"tasks": []}
                                            tasks.add_task(data, "Valid")
                                            storage.save_tasks(path, data)
                                            # corrupt primary file
                                            with open(path, "w") as f:
                                                f.write("{ not json")
                                            # load should recover from bak
                                            loaded = storage.load_tasks(path)
                                            self.assertEqual(len(loaded.get("tasks", [])), 1)


                                if __name__ == "__main__":
                                    unittest.main()
