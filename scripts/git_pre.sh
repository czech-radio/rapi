#!/bin/bash -e
scriptpath="${BASH_SOURCE[0]:-$0}"
scriptdir="${scriptpath%/*}"
if [[ "$scriptdir" == "." ]] ; then
  repodir=".."
else
  repodir="."
fi

echo RUNNING IN: "$repodir"

Mypy(){
### mypy: static type checks
# echo
# echo RUNNING: mypy
mypy --install-types
mypy --no-namespace-packages "$repodir"
}


PytestCurrent(){
 # -o log_cli=true
  pytest --capture=tee-sys -m current
}
PytestAll(){
### pytest: run repo tests
pytest
}

Black(){
### BLACK: FORMAT CODE
echo
echo RUNNING: black
black "$repodir" --exclude "(docs/|build/|dist/|\.git/|\.mypy_cache/|\.tox/|\.venv/\.asv/|env|\.eggs)"
}

Isort(){
### ISORT: SORT IMPORTS
echo
echo RUNNING: isort
isort "$repodir" --profile black
}

### FLAKE8: Lint the code
Flake(){
echo
echo RUNNING: flake8
flake8 "${repodir}/src/rapi" --count --select=E9,F63,F7,F82 --show-source --statistics --max-line-length=99 --exit-zero --max-complexity=10
}

BuildSphinxDocs(){
  ### build jupyter notebooks from jupytext
  jupytext --to ipynb --execute ${repodir}/docs/source/notebooks/*.py

  ### build sphinx docs
  sphinx-build "${repodir}/docs/source" "${repodir}/docs/build"
}

All(){
  Mypy
  PytestAll
  Black
  Isort
  Flake
  BuildSphinxDocs
}

GitPush(){
  All
  read -p 'Continue push to git? (y): ' cont
  if [[ $cont == 'y' ]]; then
    echo "yes"
  else
    exit 1
  fi
  git push origin
  echo fuck
}

"$@"


