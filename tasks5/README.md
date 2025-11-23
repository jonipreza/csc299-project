# tasks-manager (CSC 299)

Minimal command-line tasks manager for course exercises.

Quickstart
- Ensure `uv` is available in your environment.
- Run the CLI:

```bash
uv run python -m tasks5 add "Finish lab" --due 2025-11-30 --tags lab,csc299
uv run python -m tasks5 list
```

Environment
- `TASKS_FILE` environment variable can be used to set the JSON file path (defaults to `tasks.json`).

Testing
- Run unit tests with:

```bash
uv run python -m unittest
```

Notes
- See `.github/speckit.constitution.md` and `.github/speckit.specify.md` for the project's constitution and specification.
