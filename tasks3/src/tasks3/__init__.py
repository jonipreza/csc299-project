# src/tasks3/__init__.py
from .core import (
    DEFAULT_DB, load_db, save_db, add_task, list_sorted, mark_done, pretty_due
)

def inc(n: int) -> int:
    return n + 1

def main() -> None:
    # Minimal CLI: tasks3 add "Title" --due "Nov 20, 2025 3:00 pm"
    #              tasks3 list
    #              tasks3 done <id>
    import argparse
    p = argparse.ArgumentParser(prog="tasks3", description="tasks3 CLI (iteration of tasks2)")
    p.add_argument("--db", default=DEFAULT_DB, help="Path to tasks JSON")
    sub = p.add_subparsers(dest="cmd")

    addp = sub.add_parser("add", help="Add a task")
    addp.add_argument("title")
    addp.add_argument("--priority", type=int, default=3)
    addp.add_argument("--due", default="")

    sub.add_parser("list", help="List tasks")
    donep = sub.add_parser("done", help="Mark done"); donep.add_argument("id")

    args = p.parse_args()
    tasks = load_db(args.db)

    if args.cmd == "add":
        t = add_task(tasks, args.title, args.priority, args.due)
        save_db(args.db, tasks)
        print(f"Added task [{t['id']}]: {t['title']} (due {pretty_due(t['due']) or '-'})")
        return
    if args.cmd == "list":
        rows = list_sorted(tasks)
        if not rows:
            print("No tasks yet."); return
        for t in rows:
            status = "✔" if t.get("done") else " "
            print(f"[{t['id']}] {status} P{t['priority']} {t['title']}  due={pretty_due(t['due']) or '-'}")
        return
    if args.cmd == "done":
        ok = mark_done(tasks, args.id)
        save_db(args.db, tasks)
        print("Marked done." if ok else "Task not found.")
        return

    p.print_help()
