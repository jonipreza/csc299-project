"""Command-line interface for tasks-manager.

This module contains `main` which parses arguments and invokes task functions.
"""
from typing import List, Optional
import argparse
import sys
import os

from . import tasks, storage


DEFAULT_FILE = os.environ.get("TASKS_FILE", "tasks.json")


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
	p = argparse.ArgumentParser(prog="tasks")
	sub = p.add_subparsers(dest="cmd")

	a = sub.add_parser("add", help="Add a new task")
	a.add_argument("title")
	a.add_argument("--description", default="")
	a.add_argument("--due")
	a.add_argument("--tags")

	l = sub.add_parser("list", help="List tasks")
	l.add_argument("--all", action="store_true")
	l.add_argument("--completed", action="store_true")
	l.add_argument("--pending", action="store_true")
	l.add_argument("--tag")

	d = sub.add_parser("done", help="Mark task done")
	d.add_argument("id")

	r = sub.add_parser("remove", help="Remove a task")
	r.add_argument("id")
	r.add_argument("--yes", action="store_true")

	e = sub.add_parser("edit", help="Edit a task")
	e.add_argument("id")
	e.add_argument("--title")
	e.add_argument("--description")
	e.add_argument("--due")
	e.add_argument("--tags")

	return p.parse_args(argv)


def _print_task_line(t: dict) -> None:
	status = "✓" if t.get("completed") else " "
	print(f"[{status}] {t.get('id')} {t.get('title')}")


def main(argv: Optional[List[str]] = None) -> int:
	args = _parse_args(argv)
	path = DEFAULT_FILE
	try:
		data = storage.load_tasks(path)
	except Exception as e:
		print(f"Error loading tasks: {e}", file=sys.stderr)
		return 3

	try:
		if args.cmd == "add":
			tags = args.tags.split(",") if args.tags else []
			tasks.add_task(data, args.title, description=args.description, due=args.due, tags=tags)
			storage.save_tasks(path, data)
			print("Added task")
			return 0

		if args.cmd == "list":
			if args.all:
				result = tasks.list_tasks(data, completed=None)
			elif args.completed:
				result = tasks.list_tasks(data, completed=True)
			elif args.pending:
				result = tasks.list_tasks(data, completed=False)
			else:
				result = tasks.list_tasks(data, completed=False)
			for t in result:
				_print_task_line(t)
			return 0

		if args.cmd == "done":
			tasks.update_task(data, args.id, completed=True)
			storage.save_tasks(path, data)
			print("Marked done")
			return 0

		if args.cmd == "remove":
			if not args.yes:
				ans = input(f"Remove task {args.id}? [y/N]: ")
				if ans.lower() != "y":
					print("Aborted")
					return 2
			tasks.remove_task(data, args.id)
			storage.save_tasks(path, data)
			print("Removed")
			return 0

		if args.cmd == "edit":
			kwargs = {k: v for k, v in vars(args).items() if k in ("title", "description", "due", "tags") and v is not None}
			if "tags" in kwargs and kwargs["tags"] is not None:
				kwargs["tags"] = kwargs["tags"].split(",")
			tasks.update_task(data, args.id, **kwargs)
			storage.save_tasks(path, data)
			print("Updated")
			return 0

		print("No command provided; use --help", file=sys.stderr)
		return 2
	except KeyError as e:
		print(str(e), file=sys.stderr)
		return 2
	except Exception as e:
		print(f"Unexpected error: {e}", file=sys.stderr)
		return 3


if __name__ == "__main__":
	raise SystemExit(main())

