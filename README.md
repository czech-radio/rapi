# RAPI

[![main](https://github.com/czech-radio/rapi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/czech-radio/rapi/actions/workflows/main.yml)  ![version](https://img.shields.io/badge/version-0.9.0-blue.svg)  ![GitHub stars](https://img.shields.io/github/stars/czech-radio/rapi?style=social)

**Python REST API client for [mujrozhlas.cz](https://rapidoc.croapp.cz/).**

*Under the term Python client, think of classes, methods and functions that will allow you to work with data obtained with the REST API
as Python objects.*

## TODO

Please, remove when resolved.

- Check the development dependencies in `requirements.txt` whenever they are up-to-date.

## Features (cs)

- [x] 1. Získej všechny pořady aktuálně vysílané na zadané stanici. [usage](./docs/build/notebooks/station_shows.html)
- [x] 2. Získej všechny epizody vysílané pro zadaný pořad, období, časový úsek a stanici. [usage](./docs/build/notebooks/show_episodes.html)
- [x] 3. Získej všechny moderátory pro zadaný pořad. [usage](./docs/build/notebooks/moderators.html)
- [partial] 4. Získej premiéry a reprízy pro zadaný pořad. [usage](./docs/build/notebooks/show_schedules.html)

## Installation

Install package from GitHub repository.

```shell
python -m pip install git+https://github.com/czech-radio/rapi.git
```

## Documentation

See the published [documentation](https://czech-radio.githup.io/rapi) for more information.

You can build documentation localy with help of Sphinx. Be sure you have [Pandoc](https://pandoc.org/installing.html) installed and in the path. Go to `docs` folder in the project direcotry and build it with following command. The result is located in `docs/build` folder, open the `index.html` in your browser.

```shell
sphinx-build source build
```

#### station IDs

- csv [file](./src/rapi/data/stations_ids.csv) containing table of station IDs and their equivalents

### Use as library

- instantiate client

```python
import pandas as pd
from rapi import Client
cl = Client()
```

- request some data

```python
stations=cl.get_station_shows("11")
```

- create list from data and loop over it

```python
stations_list=list(stations)
for i in range(station_list):
    print(i)
```
- create pandas dataframe and loop over it

```python
stations_df=pd.DataFrame(stations_list)
stations_df.info()
for idx, row in stations_df.iterrows():
    print(idx,row['id','title'])

```

### Use as program

- get help

```shell
rapi -h
```

- get list of station_ids (default openmedia_id)

```shell
rapi station_ids
```

- get station guid (globally unique id)

```shell
rapi station_guid -id 11
```

- get station shows

```shell
rapi station_shows -id 11
```

- get show episodes

```shell
rapi show_episodes -id "9f36ee8f-73a7-3ed5-aafb-41210b7fb935"
```

## Tests

### Api test

Test the REST API <https://rapidev.croapp.cz/> with CURL (use `-g, --globoff flag`) e.g.

```shell
curl -g -X GET "https://rapidev.croapp.cz/stations?page[offset]=0&page[limit]=4" -H  "accept: application/vnd.api+json"
```

### rapi package testing

- test client

```shell
pytest -m client 
```

- show also test debug logs

```shell
pytest -o log_cli=true -m client 
```

- show also tests outputs

```shell
pytest --capture=tee-sys -m client 
```
