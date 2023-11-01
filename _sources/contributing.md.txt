# Contributing

## Install for local development 

```shell
...
```

## Write and build documentation

You can build documentation localy with help of Sphinx. Be sure you have [Pandoc](https://pandoc.org/installing.html) installed and in the path. 
Go to `docs` folder in the project direcotry and build it with following command. 
The result is located in `docs/build` folder, open the `index.html` in your browser.

```shell
sphinx-build source build
```

## Development


```shell
ruff src
ruff --fix src
ruff scripts
ruff --fix src
black . 
isort . 
pydocstyle src

pytest

cd docs
sphinx-build source build
```
