#!/usr/bin/env bash
# Wrapper to run final_project with src on PYTHONPATH
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$REPO_ROOT/src:$PYTHONPATH"
echo "PYTHONPATH=$PYTHONPATH"
echo "Running: python -m final_project $*"
python -m final_project "$@"
