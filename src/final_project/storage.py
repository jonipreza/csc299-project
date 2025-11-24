"""JSON storage helpers for final_project.

This module manages JSON persistence under the `final_project/data/` folder.
All functions use the standard library only and perform atomic writes where
appropriate.
"""

from pathlib import Path
import json
import os
from typing import Any, Dict

# Data directory: <repo-root>/final_project/data
DATA_DIR = Path(__file__).resolve().parents[2] / "final_project" / "data"
TASKS_FILE = DATA_DIR / "tasks.json"
NOTES_FILE = DATA_DIR / "notes.json"


class StorageError(RuntimeError):
    """Raised for fatal storage errors."""


def ensure_data_dir() -> Path:
    """Ensure the data directory exists and return its Path.

    Creates the directory if necessary.
    """
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return DATA_DIR
    except Exception as exc:  # pragma: no cover - IO error paths
        raise StorageError("Could not create data directory") from exc


def _read_json_text(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def load_json(path: Path, root_key: str) -> Dict[str, Any]:
    """Load JSON from `path` and return a mapping with `root_key`.

    If the file does not exist, returns `{root_key: []}`. If the JSON is
    invalid, attempts to load a `.bak` backup file and prints a warning. If
    that also fails, returns `{root_key: []}`.
    """
    p = Path(path)
    if not p.exists():
        return {root_key: []}
    try:
        data = _read_json_text(p)
        # If the file contains a mapping already, return it; otherwise wrap
        if isinstance(data, dict) and root_key in data:
            return data
        # If top-level is a list, wrap it
        if isinstance(data, list):
            return {root_key: data}
        # Unexpected structure: return default
        return {root_key: []}
    except Exception:
        bak = p.with_suffix(p.suffix + ".bak")
        print(f"Warning: failed to parse {p}, attempting backup {bak}")
        if bak.exists():
            try:
                data = _read_json_text(bak)
                if isinstance(data, dict) and root_key in data:
                    return data
                if isinstance(data, list):
                    return {root_key: data}
            except Exception:
                print(f"Warning: failed to parse backup {bak}")
        return {root_key: []}


def save_json(path: Path, data: Dict[str, Any]) -> None:
    """Atomically save `data` as JSON to `path` and write a `.bak` of previous file.

    The operation writes to a temporary file in the same directory and then
    replaces the target file using ``os.replace`` to ensure atomicity on most
    platforms.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # If existing file exists, write a backup
    if p.exists():
        try:
            prev = p.read_text(encoding="utf-8")
            bak = p.with_suffix(p.suffix + ".bak")
            bak.write_text(prev, encoding="utf-8")
        except Exception:
            # Non-fatal: continue to attempt save
            pass

    tmp = p.parent / (p.name + ".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        # Atomic replace
        os.replace(str(tmp), str(p))
    except Exception as exc:  # pragma: no cover - IO error paths
        # Clean up tmp file if it exists
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass
        raise StorageError("Failed to save JSON") from exc


def load_tasks() -> Dict[str, Any]:
    """Convenience: load tasks file and return mapping {"tasks": [...] }.
    """
    ensure_data_dir()
    return load_json(TASKS_FILE, "tasks")


def save_tasks(data: Dict[str, Any]) -> None:
    """Convenience: save the tasks mapping to disk.
    """
    ensure_data_dir()
    save_json(TASKS_FILE, data)


def load_notes() -> Dict[str, Any]:
    """Convenience: load notes file and return mapping {"notes": [...] }.
    """
    ensure_data_dir()
    return load_json(NOTES_FILE, "notes")


def save_notes(data: Dict[str, Any]) -> None:
    """Convenience: save the notes mapping to disk.
    """
    ensure_data_dir()
    save_json(NOTES_FILE, data)
