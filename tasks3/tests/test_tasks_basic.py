# tests/test_tasks_basic.py
#2 tests added
from tasks3.core import add_task, list_sorted, parse_due

def test_add_task_with_due_and_sort(tmp_path):
    # Start with empty data structure (like freshly loaded DB)
    tasks = []
    add_task(tasks, "A later thing", due="2025-12-01 10:00")
    add_task(tasks, "An earlier thing", due="2025-11-20 15:00")
    add_task(tasks, "No due date")  # should sort after those with due

    rows = list_sorted(tasks)
    titles_order = [t["title"] for t in rows]
    assert titles_order[:2] == ["An earlier thing", "A later thing"]
    assert titles_order[-1] == "No due date"

def test_parse_due_formats():
    assert parse_due("2025-11-20 15:00") == "2025-11-20T15:00"
    assert parse_due("Nov 20, 2025 3:00 pm") == "2025-11-20T15:00"
