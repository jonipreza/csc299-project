"""Command-line interface for the final_project package.

This module provides a `main()` entrypoint that implements subcommands for
tasks and notes using `argparse`. It loads and saves JSON data via
`storage.py` and delegates operations to the pure functions in `tasks.py` and
`notes.py`.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import storage, tasks, notes, chat


EXIT_OK = 0
EXIT_USER_ERROR = 2
EXIT_STORAGE_ERROR = 3


def _print_task(t: dict) -> None:
    due = t.get("due") or ""
    status = "DONE" if t.get("completed") else "PENDING"
    print(f"{t.get('id')}: {t.get('title')} [{status}] due={due}")


def _print_note(n: dict) -> None:
    print(f"{n.get('id')}: {n.get('title')}")


def main(argv: Optional[List[str]] = None) -> int:
    """Parse CLI arguments and perform requested action.

    Returns an exit code integer.
    """
    parser = argparse.ArgumentParser(prog="final_project")
    subparsers = parser.add_subparsers(dest="cmd")

    # Task subcommands
    task_parser = subparsers.add_parser("task", help="manage tasks")
    task_sub = task_parser.add_subparsers(dest="subcmd")

    # task add
    t_add = task_sub.add_parser("add", help="add a task")
    t_add.add_argument("title")
    t_add.add_argument("--description", "-d", dest="description", default="")
    t_add.add_argument("--due", dest="due", default=None)
    t_add.add_argument("--tag", dest="tags", action="append", default=[])

    # task list
    t_list = task_sub.add_parser("list", help="list tasks")
    t_list.add_argument("--status", choices=["all", "pending", "completed"], default="all")
    t_list.add_argument("--tag", dest="tag", default=None)

    # task done
    t_done = task_sub.add_parser("done", help="mark task done")
    t_done.add_argument("id")

    # task remove
    t_remove = task_sub.add_parser("remove", help="remove a task")
    t_remove.add_argument("id")

    # task edit
    t_edit = task_sub.add_parser("edit", help="edit a task")
    t_edit.add_argument("id")
    t_edit.add_argument("--title", default=None)
    t_edit.add_argument("--description", default=None)
    t_edit.add_argument("--due", default=None)
    t_edit.add_argument("--tag", dest="tags", action="append", default=None)

    # Note subcommands
    note_parser = subparsers.add_parser("note", help="manage notes")
    note_sub = note_parser.add_subparsers(dest="subcmd")

    n_add = note_sub.add_parser("add", help="add a note")
    n_add.add_argument("title")
    n_add.add_argument("--body", default="")
    n_add.add_argument("--tag", dest="tags", action="append", default=[])

    n_list = note_sub.add_parser("list", help="list notes")
    n_list.add_argument("--tag", default=None)

    n_show = note_sub.add_parser("show", help="show a note")
    n_show.add_argument("id")

    n_search = note_sub.add_parser("search", help="search notes")
    n_search.add_argument("query")

    n_edit = note_sub.add_parser("edit", help="edit a note")
    n_edit.add_argument("id")
    n_edit.add_argument("--title", default=None)
    n_edit.add_argument("--body", default=None)
    n_edit.add_argument("--tag", dest="tags", action="append", default=None)

    n_remove = note_sub.add_parser("remove", help="remove a note")
    n_remove.add_argument("id")

    # Chat subcommands (basic)
    chat_parser = subparsers.add_parser("chat", help="chat with AI helpers")
    chat_sub = chat_parser.add_subparsers(dest="subcmd")
    chat_loop = chat_sub.add_parser("loop", help="start interactive chat loop")
    chat_suggest = chat_sub.add_parser("suggest", help="suggest next tasks")

    args = parser.parse_args(argv)

    # Dispatch
    try:
        if args.cmd == "task":
            # load tasks
            data = storage.load_tasks()
            if args.subcmd == "add":
                data = tasks.create_task(data, title=args.title, description=args.description, due=args.due, tags=args.tags)
                storage.save_tasks(data)
                t = data["tasks"][-1]
                print(f"Created task {t['id']}: {t['title']}")
                return EXIT_OK

            if args.subcmd == "list":
                items = tasks.list_tasks(data, status=args.status, tag=args.tag)
                for it in items:
                    _print_task(it)
                return EXIT_OK

            if args.subcmd == "done":
                try:
                    data = tasks.mark_done(data, args.id)
                    storage.save_tasks(data)
                    print(f"Marked {args.id} done")
                    return EXIT_OK
                except KeyError:
                    print(f"Error: task id {args.id} not found")
                    return EXIT_USER_ERROR

            if args.subcmd == "remove":
                try:
                    data = tasks.remove_task(data, args.id)
                    storage.save_tasks(data)
                    print(f"Removed {args.id}")
                    return EXIT_OK
                except KeyError:
                    print(f"Error: task id {args.id} not found")
                    return EXIT_USER_ERROR

            if args.subcmd == "edit":
                try:
                    data = tasks.edit_task(data, args.id, title=args.title, description=args.description, due=args.due, tags=args.tags)
                    storage.save_tasks(data)
                    print(f"Edited {args.id}")
                    return EXIT_OK
                except KeyError:
                    print(f"Error: task id {args.id} not found")
                    return EXIT_USER_ERROR

            parser.print_help()
            return EXIT_USER_ERROR

        elif args.cmd == "note":
            data = storage.load_notes()
            if args.subcmd == "add":
                data = notes.create_note(data, title=args.title, body=args.body, tags=args.tags)
                storage.save_notes(data)
                n = data["notes"][-1]
                print(f"Created note {n['id']}: {n['title']}")
                return EXIT_OK

            if args.subcmd == "list":
                items = notes.list_notes(data, tag=args.tag)
                for it in items:
                    _print_note(it)
                return EXIT_OK

            if args.subcmd == "show":
                n = notes.get_note(data, args.id)
                if not n:
                    print(f"Error: note id {args.id} not found")
                    return EXIT_USER_ERROR
                print(f"{n['id']}: {n['title']}\n\n{n['body']}")
                return EXIT_OK

            if args.subcmd == "search":
                results = notes.search_notes(data, args.query)
                for r in results:
                    _print_note(r)
                return EXIT_OK

            if args.subcmd == "edit":
                try:
                    data = notes.edit_note(data, args.id, title=args.title, body=args.body, tags=args.tags)
                    storage.save_notes(data)
                    print(f"Edited note {args.id}")
                    return EXIT_OK
                except KeyError:
                    print(f"Error: note id {args.id} not found")
                    return EXIT_USER_ERROR

            if args.subcmd == "remove":
                try:
                    data = notes.remove_note(data, args.id)
                    storage.save_notes(data)
                    print(f"Removed note {args.id}")
                    return EXIT_OK
                except KeyError:
                    print(f"Error: note id {args.id} not found")
                    return EXIT_USER_ERROR

            parser.print_help()
            return EXIT_USER_ERROR

        elif args.cmd == "chat":
            if args.subcmd == "loop":
                chat.chat_loop()
                return EXIT_OK
            if args.subcmd == "suggest":
                # load tasks and call suggest_next_tasks
                data = storage.load_tasks()
                out = chat.suggest_next_tasks(data.get("tasks", []))
                print(out)
                return EXIT_OK
            parser.print_help()
            return EXIT_USER_ERROR

        else:
            parser.print_help()
            return EXIT_USER_ERROR

    except storage.StorageError as exc:
        print(f"Storage error: {exc}")
        return EXIT_STORAGE_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
