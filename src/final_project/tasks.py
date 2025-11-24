"""Task utilities for final_project.

This module implements pure functions that operate on an in-memory `data`
structure (a mapping containing a `"tasks"` list). Functions do not perform
file I/O; callers are responsible for persisting via `storage.py`.

Task schema (dict):
  - id: str
  - title: str
  - description: str | None
  - created_at: ISO 8601 str
  - due: ISO 8601 str | None
  - completed: bool
  - completed_at: ISO 8601 str | None
  - tags: list[str]

All functions mutate and return the `data` mapping for convenience.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from .utils import iso_now
import uuid


def _next_id(data: Dict[str, Any]) -> str:
    """Generate a numeric-ish id as a string when possible, fallback to uuid.

    Uses existing task ids that parse as integers to pick the next number.
    """
    tasks = data.get("tasks") or []
    max_id = 0
    for t in tasks:
        tid = t.get("id")
        if isinstance(tid, str) and tid.isdigit():
            try:
                n = int(tid)
                if n > max_id:
                    max_id = n
            except Exception:
                pass
    if max_id >= 0:
        return str(max_id + 1)
    # fallback
    return uuid.uuid4().hex


def create_task(
    data: Dict[str, Any],
    title: str,
    description: Optional[str] = None,
    due: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Append a new task to ``data['tasks']`` and return the updated data.

    The function generates a new `id` and `created_at` timestamp. It does not
    persist anything to disk.

    Args:
        data: mapping with a `tasks` key holding a list of task dicts.
        title: short title for the task.
        description: optional longer description.
        due: optional ISO 8601 due datetime string.
        tags: optional list of tags.

    Returns:
        The same ``data`` mapping passed in (mutated) for convenience.
    """
    if "tasks" not in data or data["tasks"] is None:
        data["tasks"] = []

    new_task: Dict[str, Any] = {
        "id": _next_id(data),
        "title": title,
        "description": description or "",
        "created_at": iso_now(),
        "due": due,
        "completed": False,
        "completed_at": None,
        "tags": tags or [],
    }

    data["tasks"].append(new_task)
    return data


def list_tasks(
    data: Dict[str, Any], *, status: Optional[str] = None, tag: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Return tasks filtered by `status` and/or `tag`.

    Args:
        data: mapping with `tasks` list.
        status: one of "all", "pending", "completed". If None, treated as
            "all".
        tag: if provided, only return tasks that contain this tag.
    """
    tasks = list(data.get("tasks") or [])
    if not status or status == "all":
        filtered = tasks
    elif status == "pending":
        filtered = [t for t in tasks if not t.get("completed")]
    elif status == "completed":
        filtered = [t for t in tasks if t.get("completed")]
    else:
        raise ValueError("status must be one of 'all', 'pending', 'completed'")

    if tag:
        tag_low = tag.lower()
        filtered = [t for t in filtered if any(tag_low == (tg or "").lower() for tg in t.get("tags", []))]

    return filtered


def mark_done(data: Dict[str, Any], task_id: str) -> Dict[str, Any]:
    """Mark the task with `task_id` as completed and set `completed_at`.

    Returns the mutated `data` mapping.
    """
    for t in data.get("tasks", []):
        if t.get("id") == task_id:
            if not t.get("completed"):
                t["completed"] = True
                t["completed_at"] = iso_now()
            return data
    raise KeyError(f"task id {task_id} not found")


def edit_task(
    data: Dict[str, Any],
    task_id: str,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Edit fields of the task with `task_id`.

    Only provided keyword arguments are updated.
    """
    for t in data.get("tasks", []):
        if t.get("id") == task_id:
            if title is not None:
                t["title"] = title
            if description is not None:
                t["description"] = description
            if due is not None:
                t["due"] = due
            if tags is not None:
                t["tags"] = tags
            return data
    raise KeyError(f"task id {task_id} not found")


def remove_task(data: Dict[str, Any], task_id: str) -> Dict[str, Any]:
    """Remove the task with `task_id` from `data['tasks']`.

    Returns the mutated `data` mapping.
    """
    tasks = data.get("tasks", [])
    new_tasks = [t for t in tasks if t.get("id") != task_id]
    if len(new_tasks) == len(tasks):
        raise KeyError(f"task id {task_id} not found")
    data["tasks"] = new_tasks
    return data


# Backwards-compatible aliases (optional)
def add_task(data: Dict[str, Any], *args, **kwargs):
    """Deprecated alias for create_task for backwards compatibility."""
    return create_task(data, *args, **kwargs)

