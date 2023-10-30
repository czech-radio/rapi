#!/bin/bash -eEu
SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="${SCRIPT_PATH%/*}"
NOTEBOOK_DIR="${SCRIPT_DIR}/../docs/source/notebooks/"

build_pyscript(){
  notebook="$1"
  jupytext --to ipynb "$notebook"
}

build_notebook(){
  local pfile=$1
  jupytext --to ipynb "$pfile"
  jupytext --execute "$pfile"
}

build_notebooks_indir(){
  declare -a notebooks=(
  $(find "$NOTEBOOK_DIR" -type f -iname "*.py")
  )
  for f in "${notebooks[@]}"; do
    build_notebook "$f"
  done
}

"$@"


