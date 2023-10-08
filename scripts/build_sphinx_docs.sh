#!/bin/bash
SCRIPTPATH="${BASH_SOURCE[0]:-$0}"
SCRIPTDIR="${SCRIPTPATH%/*}"
echo "CURRENT WORKING DIR: $PWD"
if [[ "$SCRIPTDIR" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi

### build jupyter notebooks from jupytext
jupytext --to ipynb --execute ${repodir}/docs/source/notebooks/*.py

### build sphinx docs
sphinx-build "${repodir}/docs/source" "${repodir}/docs/build"
