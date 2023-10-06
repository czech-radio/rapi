#!/bin/bash
scriptpath="${BASH_SOURCE[0]:-$0}"
scriptdir="${scriptpath%/*}"
echo "CURRENT WORKING DIR: $PWD"
if [[ "$scriptdir" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi
sphinx-build "${repodir}/docs/source" "${repodir}/docs/build"
