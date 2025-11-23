---
agent: speckit.specify
name: tasks-manager-spec
version: 1.0
language: python
data_store: json
package_manager: uv
scope: specification for command-line tasks manager
---

# Specification — tasks-manager

This file specifies the concrete contracts for the `tasks-manager` project described in
`.github/speckit.constitution.md`. It defines the JSON schema, CLI commands, module APIs,
testing expectations, and example runs so students can implement the project consistently.

Data schema (JSON)
- Filename: `tasks.json` (default, configurable via environment variable `TASKS_FILE`)
- Root: an object with a single key `tasks` which is an array of task objects.

Task object schema (JSON Schema-like)
- id: string (uuid or simple incrementing string) — required
- title: string — required, non-empty
- description: string — optional
- created_at: ISO 8601 datetime string — required
- due: ISO 8601 date string — optional
- completed: boolean — required (default false)
- completed_at: ISO 8601 datetime string or null — optional
- tags: array of strings — optional

Example tasks.json
{
  "tasks": [
    {
      "id": "1",
      "title": "Finish lab 3",
      "description": "Complete exercises 1-4",
      "created_at": "2025-11-23T12:00:00Z",
      "due": "2025-11-30",
      "completed": false,
      "completed_at": null,
      "tags": ["lab","csc299"]
    }
  ]
}

CLI commands and options
- `add <title> [--description TEXT] [--due YYYY-MM-DD] [--tags TAGS]`
  - Creates a new task. Prints the new task id and title.
  - `--tags` accepts comma-separated tags.

- `list [--all] [--completed] [--pending] [--tag TAG] [--due-before YYYY-MM-DD]`
  - Lists tasks in a readable table. Default: pending tasks only.
  - `--all` shows all tasks; `--completed` shows only completed; `--pending` only pending.

- `done <id>`
  - Marks a task completed and sets `completed_at`.

- `remove <id>`
  - Removes a task permanently (ask for confirmation unless `--yes` provided).

- `edit <id> [--title TITLE] [--description TEXT] [--due YYYY-MM-DD] [--tags TAGS]`
  - Update fields on a task.

- `help` or `-h`/`--help`
  - Shows CLI help and available commands.

Exit codes and error handling
- Exit code 0: success
- Exit code 2: user error (invalid args, missing arguments)
- Exit code 3: storage error (cannot read/write tasks file)
- CLI must print human-friendly errors to stderr.

Module and function contracts

storage.py
- load_tasks(path: str) -> dict
  - Loads JSON file at `path`. If file missing, returns {'tasks': []}.
  - On JSON decode error, attempt to load `path + '.bak'` and warn the user.
  - Raises FileNotFoundError only if both primary and backup are missing and path is required.

- save_tasks(path: str, data: dict) -> None
  - Writes data atomically: write to temp file then rename.
  - On success, create/replace `path + '.bak'` with previous content.

tasks.py
- add_task(data: dict, title: str, description: Optional[str], due: Optional[str], tags: Optional[List[str]]) -> dict
  - Mutates `data` or returns new data structure with task added.
  - Generates `id` and `created_at`.

- list_tasks(data: dict, filter: dict) -> List[dict]
  - Return tasks matching filter; does not print.

- get_task(data: dict, id: str) -> Optional[dict]

- update_task(data: dict, id: str, **kwargs) -> dict

- remove_task(data: dict, id: str) -> dict

cli.py
- main(argv: Optional[List[str]] = None) -> int
  - Parse args, call functions above, print results, and return an exit code.
  - Avoid raising uncaught exceptions; convert to proper exit codes.

Testing specification
- Use `unittest` library (no external deps).
- tests/test_tasks.py should cover:
  - Adding a task and verifying fields set.
  - Marking a task done updates `completed` and `completed_at`.
  - Saving and loading tasks preserves data (use temporary file).
  - Handling invalid JSON by recovering from `.bak` (simulate corrupted file).

File I/O strategy for tests
- Use Python's `tempfile.TemporaryDirectory` or `tmp_path` fixture to isolate file writes.

Examples
- Add a task:
  uv run python -m tasks5 add "Finish lab 3" --due 2025-11-30 --tags lab,csc299

- List pending tasks:
  uv run python -m tasks5 list

- Mark done:
  uv run python -m tasks5 done 1

Notes
- Keep functions returning data structures (not printing) so they are easy to unit test. CLI should only handle printing and exit codes.

Files created/updated by implementers
- `tasks.py`, `storage.py`, `cli.py`, `__main__.py`, `tests/test_tasks.py`, `README.md`.

---
Specification written: 2025-11-23
