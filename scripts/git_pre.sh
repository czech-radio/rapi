#!/bin/bash
scriptpath="${BASH_SOURCE[0]:-$0}"
scriptdir="${scriptpath%/*}"
if [[ "$scriptdir" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi

echo RUNNING IN: "$repodir"

### mypy: static type checks
echo
echo RUNNING: mypy
mypy --install-types
mypy --no-namespace-packages "$repodir"

### pytest: run repo tests
# pytest

### black: format code
echo
echo RUNNING: black
black -v "$repodir" --check --extend-exclude "(docs/|build/|/.venv/)"
# --exclude "(docs/|build/|dist/|\.git/|\.mypy_cache/|\.tox/|\.venv/\.asv/|env|\.eggs)"

### isort: sort imports
echo
echo RUNNING: isort
isort "$repodir" --check --profile black

### flake8: style enforcement
echo RUNNING: flake8
flake8 "$repodir" --count --select=E9,F63,F7,F82 --show-source --statistics

### workflow
# black
# isort
# flake8


