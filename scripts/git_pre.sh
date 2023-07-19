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
