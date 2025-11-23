---
agent: speckit.constitution
name: tasks-manager
version: 1.0
language: python
package_manager: uv
data_store: json
scope: command-line tasks manager for CSC 299
target_folder: tasks5
author_instructions: |
  This constitution documents the conventions, contracts, and minimal requirements
  for the `tasks-manager` project so other contributors (students) can understand,
  run, and maintain the code easily.
---

# Project Constitution — tasks-manager

Purpose
- Provide a small, clear, and maintainable command-line tasks manager written in Python
  for CSC 299 course exercises.

Design Principles
- Simplicity over cleverness: prefer clear code and small functions.
- Minimal dependencies: only Python standard library + whatever `uv` needs to run the project.
- Explicit CLI contract and helpful help text for each command and option.
- Robust error handling: validate input and never crash on user mistakes.
- Small, testable units with basic automated tests.

Technology & Tools
- Language: Python (3.9+ recommended)
- Package/tool manager: uv (project uses `uv` for running/installing; document assumes `uv` is available)
- Storage: JSON file (simple file in the user config directory or repo for teaching)
- Runtime: terminal/console (no GUI)

Project layout (minimal and copy-friendly into `tasks5`)
- tasks5/
  - tasks.py            # core task model + logic (add, list, remove, update, query)
  - storage.py          # JSON persistence functions (load/save with backups and atomic write)
  - cli.py              # command-line interface and argument parsing (help text included)
  - __main__.py         # optional runner so `python -m tasks5` works
  - tests/
    - test_tasks.py     # unit tests (happy path + a couple edge cases)
  - README.md           # short usage + install with uv

CLI contract (high level)
- Commands: add, list, done, remove, edit, help
- Inputs: simple flags and positional arguments (e.g., `add "Finish lab" --due 2025-11-30`)
- Outputs: printed text to stdout (machine-friendly options optional, e.g., --json)
- Error modes: print a helpful error message to stderr and return non-zero exit code. Do not raise uncaught exceptions.

Coding conventions
- Keep functions small (single responsibility). Each public function should be testable.
- Use type hints for public functions where helpful.
- Docstrings: short one-line then brief details for non-trivial functions.
- Logging: minimal; prefer clear user-facing messages on CLI; use `logging` only for internal debug (not required).

Storage guarantees
- Use a single JSON file as the canonical store (default name: `tasks.json`).
- Writes must be atomic: write to a temp file then rename.
- Maintain a simple history/backup file `tasks.json.bak` on each successful save.

Error handling
- Validate user input and print helpful messages.
- For corrupted JSON: attempt a safe recovery strategy (load from `.bak` if available) and notify the user.

Testing rules
- Provide at minimum:
  - tests/test_tasks.py with unit tests for add/list/remove and storage load/save.
  - tests should run with Python's `unittest` or `pytest` if `uv` installs it; prefer `unittest` to avoid extra dependencies.
- Tests must be fast and isolated (use temporary files or tmp_path fixtures).

How to run & developer notes
- Running locally (developer): use `uv` to run the module or tests. Example (documented in README):
  - `uv run python -m tasks5`  # runs the CLI using uv's runner
  - `uv run python -m unittest`  # run tests

Acceptance criteria for course grading
- The CLI supports basic add/list/remove/done commands with help text.
- Data is persisted in JSON and survives program restarts.
- Code is readable and small functions are present.
- Basic unit tests exist and pass.

Contributions & style
- Keep PRs small. Prefer readability and tests.
- If adding dependencies, justify why and get instructor approval.

Assumptions & notes
- The repository may not contain `uv` config; this constitution assumes `uv` is the requested tool for running/packaging. If `uv` is not available to students, substitute with `python -m venv` + `pip` in README.
- File paths and module names are intentionally simple so code can be copied into a `tasks5` folder in other repos.

Contact
- For course help, include instructor or TA contact details in `README.md` (not included here).

---
Constitution written: 2025-11-23
