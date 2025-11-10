
#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from typing import List, Dict, Any
from storage import load_db, save_db, DEFAULT_DB, gen_id

def add_task(db: Dict[str,Any], title: str, priority: int = 3, tags: str = "", due: str = "") -> Dict[str,Any]:
    t = {"id": gen_id("t"), "title": title.strip(), "priority": int(priority), "done": False,
         "due": due.strip(), "tags": [s.strip() for s in tags.split(",") if s.strip()] if isinstance(tags, str) else list(tags)}
    db["tasks"].append(t); return t

def list_tasks(db: Dict[str,Any]):
    return list(db.get("tasks", []))

def search_tasks(db: Dict[str,Any], query: str):
    q = query.lower().strip()
    if not q: return []
    import re
    words = [w for w in re.split(r"\W+", q) if w]
    out = []
    for t in db.get("tasks", []):
        hay = (t["title"] + " " + " ".join(t.get("tags",[])) + " " + t.get("due"," ")).lower()
        score = sum(hay.count(w) for w in words) + (5 if any(w in t.get("tags",[]) for w in words) else 0)
        if score > 0:
            tt = dict(t); tt["_score"] = float(score); out.append(tt)
    out.sort(key=lambda x: (-x["_score"], -x["priority"]))
    return out

def mark_done(db: Dict[str,Any], task_id: str) -> bool:
    for t in db.get("tasks", []):
        if str(t["id"]) == str(task_id):
            t["done"] = True; return True
    return False

def delete_task(db: Dict[str,Any], task_id: str) -> bool:
    tasks = db.get("tasks", [])
    before = len(tasks)
    db["tasks"] = [t for t in tasks if str(t["id"]) != str(task_id)]
    return len(db["tasks"]) != before

def edit_task(db: Dict[str,Any], task_id: str, title=None, priority=None, due=None, tags=None) -> bool:
    for t in db.get("tasks", []):
        if str(t["id"]) == str(task_id):
            if title is not None: t["title"] = title.strip()
            if priority is not None: t["priority"] = int(priority)
            if due is not None: t["due"] = due.strip()
            if tags is not None: t["tags"] = [s.strip() for s in tags.split(",") if s.strip()]
            return True
    return False

def add_note(db: Dict[str,Any], title: str, body: str = "", tags: str = "") -> Dict[str,Any]:
    n = {"id": gen_id("n"), "title": title.strip(), "body": body, "tags": [s.strip() for s in tags.split(",") if s.strip()]}
    db["notes"].append(n); return n

def list_notes(db: Dict[str,Any]): return list(db.get("notes", []))

def search_notes(db: Dict[str,Any], query: str):
    q = query.lower().strip()
    if not q: return []
    import re
    words = [w for w in re.split(r"\W+", q) if w]
    out = []
    for n in db.get("notes", []):
        hay = (n["title"] + " " + n.get("body"," ") + " " + " ".join(n.get("tags",[]))).lower()
        score = sum(hay.count(w) for w in words) + (2 * sum(1 for w in words if w in n.get("tags",[])))
        if score > 0:
            nn = dict(n); nn["_score"] = float(score); out.append(nn)
    out.sort(key=lambda x: (-x["_score"]))
    return out

def build_parser():
    p = argparse.ArgumentParser(prog="tasks2", description="tasks2 — Tasks + minimal PKMS (JSON storage)")
    p.add_argument("--db", default=DEFAULT_DB, help="Path to JSON database file (default: tasks2.json)")
    sub = p.add_subparsers(dest="cmd")

    # tasks
    tp = sub.add_parser("tasks", help="Task commands")
    tsub = tp.add_subparsers(dest="tcmd")

    addp = tsub.add_parser("add", help="Add a task")
    addp.add_argument("title"); addp.add_argument("--priority", type=int, default=3)
    addp.add_argument("--tags", default=""); addp.add_argument("--due", default="")

    tsub.add_parser("list", help="List tasks")

    sp = tsub.add_parser("search", help="Search tasks"); sp.add_argument("query")
    dp = tsub.add_parser("done", help="Mark task done"); dp.add_argument("id")
    delp = tsub.add_parser("delete", help="Delete task"); delp.add_argument("id")
    ep = tsub.add_parser("edit", help="Edit task fields"); ep.add_argument("id")
    ep.add_argument("--title"); ep.add_argument("--priority", type=int); ep.add_argument("--due"); ep.add_argument("--tags")

    # notes
    np = sub.add_parser("notes", help="Note commands (PKMS)")
    nsub = np.add_subparsers(dest="ncmd")
    nadd = nsub.add_parser("add", help="Add a note"); nadd.add_argument("title")
    nadd.add_argument("--tags", default=""); nadd.add_argument("--body", default="")
    nsub.add_parser("list", help="List notes")
    ns = nsub.add_parser("search", help="Search notes"); ns.add_argument("query")
    return p

def main(argv=None):
    args = build_parser().parse_args(argv)
    db = load_db(args.db)

    if args.cmd == "tasks":
        if args.tcmd == "add":
            t = add_task(db, args.title, args.priority, args.tags, args.due)
            print(f"Added task #{t['id']}: {t['title']}")
        elif args.tcmd == "list":
            rows = list_tasks(db)
            if not rows: print("No tasks yet.")
            for t in rows:
                print(f"[{t['id']}] {'✔' if t['done'] else ' '} P{t['priority']} {t['title']}  tags={','.join(t.get('tags',[]))} due={t.get('due','')}")
        elif args.tcmd == "search":
            for t in search_tasks(db, args.query):
                print(f"[{t['id']}] P{t['priority']} {t['title']}  tags={','.join(t.get('tags',[]))}")
        elif args.tcmd == "done":
            print("Marked done." if mark_done(db, args.id) else "Task not found.")
        elif args.tcmd == "delete":
            print("Deleted." if delete_task(db, args.id) else "Task not found.")
        elif args.tcmd == "edit":
            ok = edit_task(db, args.id, args.title, args.priority, args.due, args.tags)
            print("Updated." if ok else "Task not found.")
        else:
            print("Use: tasks {add|list|search|done|delete|edit} ...")
        save_db(args.db, db); return

    if args.cmd == "notes":
        if args.ncmd == "add":
            n = add_note(db, args.title, body=args.body, tags=args.tags)
            print(f"Added note #{n['id']}: {n['title']}")
        elif args.ncmd == "list":
            rows = list_notes(db)
            if not rows: print("No notes yet.")
            for n in rows:
                print(f"[{n['id']}] {n['title']}  tags={','.join(n.get('tags',[]))}")
        elif args.ncmd == "search":
            for n in search_notes(db, args.query):
                print(f"[{n['id']}] {n['title']}  score={n.get('_score',0):.2f}")
        else:
            print("Use: notes {add|list|search}")
        save_db(args.db, db); return

    build_parser().print_help()

if __name__ == "__main__":
    main()
