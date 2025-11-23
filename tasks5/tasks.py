"""Core task manipulation functions for tasks-manager.

Keep functions small and return data structures for easy testing.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def add_task(data: Dict[str, Any], title: str, description: Optional[str] = None,
             due: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Return new data dict with a task added.

    The function does not perform persistence; it mutates and returns the provided dict.
    """
    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description or "",
        "created_at": _now_iso(),
        "due": due,
        "completed": False,
        "completed_at": None,
        "tags": tags or [],
    }
    tasks = data.setdefault("tasks", [])
    tasks.append(task)
    return data


def list_tasks(data: Dict[str, Any], *, completed: Optional[bool] = None, tag: Optional[str] = None) -> List[Dict[str, Any]]:
    tasks = data.get("tasks", [])
    result = []
    for t in tasks:
        if completed is not None and bool(t.get("completed")) != completed:
            continue
        if tag and tag not in (t.get("tags") or []):
            continue
        result.append(t)
    return result


def get_task(data: Dict[str, Any], id: str) -> Optional[Dict[str, Any]]:
    for t in data.get("tasks", []):
        if t.get("id") == id:
            return t
    return None


def update_task(data: Dict[str, Any], id: str, **kwargs) -> Dict[str, Any]:
    t = get_task(data, id)
    if t is None:
        raise KeyError(f"task not found: {id}")
    # Allow updates to specific fields
    for k in ("title", "description", "due", "tags"):
        if k in kwargs:
            t[k] = kwargs[k]
    if kwargs.get("completed") is True and not t.get("completed"):
        t["completed"] = True
        t["completed_at"] = _now_iso()
    if kwargs.get("completed") is False and t.get("completed"):
        t["completed"] = False
        t["completed_at"] = None
    return data


def remove_task(data: Dict[str, Any], id: str) -> Dict[str, Any]:
    tasks = data.get("tasks", [])
    new_tasks = [t for t in tasks if t.get("id") != id]
    if len(new_tasks) == len(tasks):
        raise KeyError(f"task not found: {id}")
    data["tasks"] = new_tasks
    return data
