# RAPI

[![main](https://github.com/czech-radio/rapi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/czech-radio/rapi/actions/workflows/main.yml)  ![version](https://img.shields.io/badge/version-0.9.0-blue.svg)  ![language](https://img.shields.io/badge/language-Python-blue.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/238d42622d25443c8dc71b60e38efb6b)](https://app.codacy.com/gh/czech-radio/rapi/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) ![GitHub stars](https://img.shields.io/github/stars/czech-radio/rapi?style=social) 

**Python REST API client for [mujrozhlas.cz](https://rapidoc.croapp.cz/).**

The *rapi* package is a library that queries the REST API available at <https://api.mujrozhlas.cz>. For example, this endpoint <https://api.mujrozhlas.cz/stations>, which returns the metadata of all stations in JSON form. The JSON is then converted to Python domain object for further work. This library therefore converts JSON into Python objects that can be directly used in Python code.

## Usage

1. nejdříve se vytvoří instance rapi clientu
2. následně se pomocí rapi clienta zavolá požadovaná funkce s požadovanými parametry:
například: chci získat všechny pořady pro zadanou stanici. Standardně je id stanice číslo tzv. openmedia_id. Tabulka id stanic je [zde](../../src/rapi/data/stations_ids.csv)
3. rapi client vrátí objekt, který obsahuje jednotlivé stanice: list[Stations], se kterým lze přímo pracovat jako s list of dictionaries nebo lze převést jednoduše na pandas dataframe: pandas.DataFrame(data). Tento dataframe lze pak uložit jako csv soubor, nebo s ním pracovat podobně jako s tabulkou.

## Examples

- Get shows for the given station. [usage](notebooks/get_shows_for_the_given_station.ipynb)
- Get episodes for the given show. [usage](notebooks/get_episodes_for_the_given_show.ipynb)
- Get participants for the given show. [usage](notebooks/get_participants_for_the_given_show.ipynb)
- Get schedules for the given show. [usage](notebooks/get_schedules_for_the_given_show.ipynb)

## Installation

Install the lates package version from repository main branch.

```shell
python -m pip install git+https://github.com/czech-radio/rapi.git
```

## Documentation

See the published [documentation](https://czech-radio.githup.io/rapi) for more information.

You can build documentation localy with help of Sphinx. Be sure you have [Pandoc](https://pandoc.org/installing.html) installed and in the path. Go to `docs` folder in the project direcotry and build it with following command. The result is located in `docs/build` folder, open the `index.html` in your browser.

```shell
sphinx-build source build
```
