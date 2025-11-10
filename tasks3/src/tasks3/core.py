# src/tasks3/core.py
import json, os, re, time
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

_DUE_FORMATS = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %I:%M %p",
    "%b %d, %Y %I:%M %p",
    "%B %d, %Y %I:%M %p",
]

def parse_due(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    for fmt in _DUE_FORMATS:
        try:
            dt = datetime.strptime(s, fmt)
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
