#!/usr/bin/env python3
# tasks2 - Iteration: adds due dates with specific times (e.g. "Nov 20, 2025 3:00 pm").

import argparse, json, os, re, time
from datetime import datetime

DEFAULT_DB = "tasks.json"

def load_db(path: str):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_db(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def gen_id(prefix: str="t") -> str:
    return f"{prefix}_{int(time.time()*1000)}"

# --- Due date parsing ---
_DUE_FORMATS = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %I:%M %p",
    "%b %d, %Y %I:%M %p",
    "%B %d, %Y %I:%M %p",
]

def parse_due(s: str) -> str:
    if not s.strip():
        return ""
    for fmt in _DUE_FORMATS:
        try:
            dt = datetime.strptime(s.strip(), fmt)
            return dt.strftime("%Y-%m-%dT%H:%M")
        except ValueError:
            continue
    raise ValueError("Invalid date format. Try '2025-11-20 15:00' or 'Nov 20, 2025 3:00 pm'.")

def pretty_due(iso: str) -> str:
    if not iso:
        return ""
    try:
        dt = datetime.strptime(iso, "%Y-%m-%dT%H:%M")
        return dt.strftime("%b %d, %Y %I:%M %p")
    except ValueError:
        return iso

# --- Core logic ---
def add_task(tasks, title, priority=3, due=""):
    t = {
        "id": gen_id("t"),
        "title": title.strip(),
        "priority": int(priority),
        "done": False,
        "due": parse_due(due) if due else "",
        "created": time.time(),
    }
    tasks.append(t)
    return t

def mark_done(tasks, task_id):
    for t in tasks:
        if str(t.get("id")) == str(task_id):
            t["done"] = True
            return True
    return False

def list_sorted(tasks):
    def key(t):
        return (t.get("due") or "9999-12-31T23:59", t.get("created", 0))
    return sorted(tasks, key=key)

# --- CLI ---
def build_parser():
    p = argparse.ArgumentParser(description="tasks2 - add due dates with specific times")
    p.add_argument("--db", default=DEFAULT_DB, help="Path to JSON database file")
    sub = p.add_subparsers(dest="cmd")

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title")
    add.add_argument("--priority", type=int, default=3)
    add.add_argument("--due", default="", help="Due date/time (e.g. 'Nov 20, 2025 3:00 pm')")

    sub.add_parser("list", help="List all tasks sorted by due date")
    done = sub.add_parser("done", help="Mark a task done")
    done.add_argument("id")

    return p

def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks = load_db(args.db)

    if args.cmd == "add":
        try:
            t = add_task(tasks, args.title, args.priority, args.due)
        except ValueError as e:
            print(e)
            return
        save_db(args.db, tasks)
        print(f"Added task [{t['id']}]: {t['title']} (due {pretty_due(t['due']) or '-'})")
        return

    if args.cmd == "list":
        rows = list_sorted(tasks)
        if not rows:
            print("No tasks yet.")
            return
        for t in rows:
            status = "✔" if t.get("done") else " "
            print(f"[{t['id']}] {status} P{t['priority']} {t['title']}  due={pretty_due(t['due']) or '-'}")
        return

    if args.cmd == "done":
        ok = mark_done(tasks, args.id)
        save_db(args.db, tasks)
        print("Marked done." if ok else "Task not found.")
        return

    build_parser().print_help()

if __name__ == "__main__":
    main()
