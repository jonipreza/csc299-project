Final Project — Personal Task Manager & PKMS

This folder contains a scaffold for a small personal task manager and a
personal knowledge management system (PKMS). It provides a CLI, JSON-based
storage, and optional AI helpers (OpenAI gpt-5-mini) for summarization and
suggestions.

Quick contents
- `src/final_project/cli.py` — CLI entrypoint (argparse)
- `src/final_project/tasks.py` — pure-dict task operations
- `src/final_project/notes.py` — pure-dict notes operations
- `src/final_project/storage.py` — atomic JSON load/save and backups
- `src/final_project/chat.py` — OpenAI helpers and interactive chat loop
- `final_project/data/` — `tasks.json` and `notes.json` (runtime data)
- `final_project/tests/` — unit tests (unittest)

Running (convenience)
---------------------

The package uses an `src/` layout (`src/final_project` is the package). To
make running easy from the repository root there are two wrapper scripts:

- `run-final-project.ps1` — PowerShell wrapper for Windows
- `run-final-project.sh`  — POSIX shell wrapper for macOS/Linux

Examples (from the repository root):

PowerShell (Windows):
```powershell
.\run-final-project.ps1 task add "Write report" --description "Summarize Q4 results" --due "2025-11-30" --tag work --tag urgent
.\run-final-project.ps1 task list --status pending
.\run-final-project.ps1 note add "Meeting notes" --body "Discussed roadmap" --tag meeting
```

Shell (macOS / Linux):
```bash
./run-final-project.sh task add "Write report" --description "Summarize Q4 results" --due "2025-11-30" --tag work --tag urgent
./run-final-project.sh task list --status pending
./run-final-project.sh note list
```

Alternative (manual PYTHONPATH):
```powershell
$env:PYTHONPATH = (Get-Location).Path + '\src'
python -m final_project task list
```

AI features
-----------
- Set `OPENAI_API_KEY` in your environment to enable summarization and suggestions.
- Example (PowerShell):
```powershell
$env:OPENAI_API_KEY = 'sk-REPLACE_WITH_YOUR_KEY'
```

Testing
-------
- Run only this package's tests from the repo root:
```powershell
python -m pytest final_project/tests -q
```

Notes
-----
- Storage is JSON files under `final_project/data/` and uses atomic writes
  with `.bak` backups.
- The CLI uses argparse and delegates logic to the pure functions in
  `tasks.py` and `notes.py` so they are easy to test.
TODO: Final Project - Personal Task & PKMS

This folder contains a scaffold for a personal task manager and PKMS.

TODOs:
- Add setup instructions (install dependencies)
- Document `data/` JSON files: `tasks.json`, `notes.json`
- Document how to run the CLI: `python -m final_project.cli`
- Document `OPENAI_API_KEY` usage
