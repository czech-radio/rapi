#!/bin/bash -e
scriptpath="${BASH_SOURCE[0]:-$0}"
scriptdir="${scriptpath%/*}"
if [[ "$scriptdir" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi

echo RUNNING IN: $(realpath "$repodir")

### STATIC TYPE CHECKS
Mypy(){
mypy --install-types
mypy --no-namespace-packages "$repodir"
}


### PYTEST
PytestCurrent(){
  # -o log_cli=true
  pytest --capture=tee-sys -m current
}
PytestAll(){
  pytest
}

### FORMAT CODE
Black(){
  python -m black "$repodir" --exclude "(docs/|build/|dist/|\.git/|\.mypy_cache/|\.tox/|\.venv/\.asv/|env|\.eggs)"
}

Isort(){
# SORT IMPORTS
  python -m isort "$repodir" --profile black
}


### LINTERS
Flake(){
flake8 "${repodir}/src/rapi" --count --select=E9,F63,F7,F82 --show-source --statistics --max-line-length=99 --exit-zero --max-complexity=10
}

Ruff(){
  python -m ruff format .
}

### SPHINX
BuildSphinxDocs(){
  # python -m jupytext --to ipynb --execute ${repodir}/docs/source/notebooks/*.py

  python -m sphinx "${repodir}/docs/source" "${repodir}/docs/build"
}

### AGREGATE
All(){
  local tasks
  declare -a tasks=(
    Mypy
    PytestAll
    Ruff
    Flake
    BuildSphinxDocs
  )
  i=1
  for t in "${tasks[@]}"; do
    echo
    echo "RUNNING TASK ${i}/${#tasks[*]}: $t"
    "$t"
    ((i++))
  done
}


### GIT
GitPush(){
  All
  read -p 'Continue push to git? (y): ' cont
  if [[ $cont == 'y' ]]; then
    echo "yes"
  else
    exit 1
  fi
  git push origin
}

"$@"


