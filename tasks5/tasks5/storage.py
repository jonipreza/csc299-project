"""JSON storage utilities for tasks-manager.

Provides load_tasks and save_tasks with simple backup and atomic-write semantics.
"""
from typing import Dict, Any
import json
import os
import tempfile


def load_tasks(path: str) -> Dict[str, Any]:
	if not os.path.exists(path):
		return {"tasks": []}
	try:
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	except json.JSONDecodeError:
		bak = path + ".bak"
		if os.path.exists(bak):
			with open(bak, "r", encoding="utf-8") as f:
				return json.load(f)
		raise


def save_tasks(path: str, data: Dict[str, Any]) -> None:
	dirpath = os.path.dirname(path) or "."
	# Read previous content for backup
	prev = None
	if os.path.exists(path):
		with open(path, "r", encoding="utf-8") as f:
			prev = f.read()

	# Write atomically
	fd, tmp_path = tempfile.mkstemp(dir=dirpath)
	try:
		with os.fdopen(fd, "w", encoding="utf-8") as tmp:
			json.dump(data, tmp, indent=2, ensure_ascii=False)
			tmp.flush()
			os.fsync(tmp.fileno())
		os.replace(tmp_path, path)
	finally:
		if os.path.exists(tmp_path):
			os.remove(tmp_path)

	# Create/replace backup with the saved content so future recovery is possible
	bak = path + ".bak"
	try:
		with open(bak, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=2, ensure_ascii=False)
	except Exception:
		# If backup write fails, don't prevent the main save — caller can handle disk errors
		pass

