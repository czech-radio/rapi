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
# echo
# echo RUNNING: mypy
# mypy --install-types
# mypy --no-namespace-packages "$repodir"


### pytest: run repo tests
# pytest

### BLACK: FORMAT CODE
echo
echo RUNNING: black
black "$repodir" --exclude "(docs/|build/|dist/|\.git/|\.mypy_cache/|\.tox/|\.venv/\.asv/|env|\.eggs)"

### ISORT: SORT IMPORTS
echo
echo RUNNING: isort
isort "$repodir" --profile black

### FLAKE8: Lint the code
echo
echo RUNNING: flake8
flake8 "${repodir}/src/rapi" --count --select=E9,F63,F7,F82 --show-source --statistics --max-line-length=99 --exit-zero --max-complexity=10


