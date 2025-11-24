"""Pure-dict notes utilities for final_project.

Functions operate on an in-memory ``data`` mapping with a ``"notes"`` key
holding a list of note dicts. No file I/O is performed here; callers should
persist via `storage.py` when needed.

Note schema (dict):
  - id: str
  - title: str
  - body: str
  - created_at: ISO 8601 str
  - tags: list[str]
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from .utils import iso_now
import uuid


def _next_id(data: Dict[str, Any]) -> str:
    """Generate the next numeric id if possible; otherwise use a uuid hex."""
    notes = data.get("notes") or []
    max_id = 0
    for n in notes:
        nid = n.get("id")
        if isinstance(nid, str) and nid.isdigit():
            try:
                val = int(nid)
                if val > max_id:
                    max_id = val
            except Exception:
                pass
    if max_id >= 0:
        return str(max_id + 1)
    return uuid.uuid4().hex


def create_note(data: Dict[str, Any], title: str, body: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Append a new note to ``data['notes']`` and return the mutated mapping.

    Args:
        data: mapping containing a `notes` list.
        title: note title.
        body: full note body.
        tags: optional list of tags.

    Returns:
        The same ``data`` mapping (mutated).
    """
    if "notes" not in data or data["notes"] is None:
        data["notes"] = []

    note = {
        "id": _next_id(data),
        "title": title,
        "body": body,
        "created_at": iso_now(),
        "tags": tags or [],
    }

    data["notes"].append(note)
    return data


def list_notes(data: Dict[str, Any], tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return notes, optionally filtered by a tag.

    Tag matching is case-insensitive and exact for tag entries.
    """
    notes = list(data.get("notes") or [])
    if tag:
        tag_low = tag.lower()
        notes = [n for n in notes if any((tg or "").lower() == tag_low for tg in n.get("tags", []))]
    return notes


def get_note(data: Dict[str, Any], note_id: str) -> Optional[Dict[str, Any]]:
    """Return the note dict with `note_id` or None if not found."""
    for n in data.get("notes", []):
        if n.get("id") == note_id:
            return n
    return None


def edit_note(
    data: Dict[str, Any], note_id: str, *, title: Optional[str] = None, body: Optional[str] = None, tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Edit fields of a note. Only provided kwargs are updated.

    Raises KeyError if the note id does not exist.
    """
    for n in data.get("notes", []):
        if n.get("id") == note_id:
            if title is not None:
                n["title"] = title
            if body is not None:
                n["body"] = body
            if tags is not None:
                n["tags"] = tags
            return data
    raise KeyError(f"note id {note_id} not found")


def remove_note(data: Dict[str, Any], note_id: str) -> Dict[str, Any]:
    """Remove the note with `note_id` and return the mutated mapping.

    Raises KeyError if the note id is not present.
    """
    notes = data.get("notes", [])
    new = [n for n in notes if n.get("id") != note_id]
    if len(new) == len(notes):
        raise KeyError(f"note id {note_id} not found")
    data["notes"] = new
    return data


def search_notes(data: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
    """Return notes where `query` is a substring of the title or body (case-insensitive)."""
    q = (query or "").lower()
    results: List[Dict[str, Any]] = []
    for n in data.get("notes", []):
        if q in (n.get("title") or "").lower() or q in (n.get("body") or "").lower():
            results.append(n)
    return results

