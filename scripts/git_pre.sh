#!/bin/bash
scriptpath="${BASH_SOURCE[0]:-$0}"
scriptdir="${scriptpath%/*}"
if [[ "$scriptdir" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi

### pytest: run repo tests
# pytest
### black: format code
black "$repodir"
### isort: sort imports
isort "$repodir"
### flake8: style enforcement

### mypy: static type checks
mypy --install-types
mypy -v --no-namespace-packages "$repodir"
