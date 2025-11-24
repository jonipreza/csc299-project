"""Module entrypoint for `python -m final_project`.

This simply forwards to the CLI `main()` function so the package can be
executed with `-m final_project` as expected.
"""
from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
