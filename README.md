# rapi

[![main](https://github.com/czech-radio/rapi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/czech-radio/rapi/actions/workflows/main.yml)

**The Python REST API client for [mujrozhlas.cz](https://rapidoc.croapp.cz/).**

- maintainer: Jan Kačaba
- repository: <https://github.com/czech-radio/rapi>

Under the term Python client, think of classes, methods and functions that will allow you to work with data obtained with the REST API
as Python objects.

## Features (cs)

- [x] 1. Získej všechny pořady aktuálně vysílané na zadané stanici. [usage](./docs/build/notebooks/station_shows.html)
- [x] 2. Získej všechny epizody vysílané pro zadaný pořad, období, časový úsek a stanici. [usage](./docs/build/notebooks/show_episodes.html)
- [x] 3. Získej všechny moderátory pro zadaný pořad. [usage](./docs/build/notebooks/moderators.html)
- [partial] 4. Získej premiéry a reprízy pro zadaný pořad. [usage](./docs/build/notebooks/show_schedules.html)

## Model (Terms, Facts, Rules)

Doménový model json třídy reprezentující jednotlivé objekty se musí namodelovat s citem.
Zatím jasně vidíme tyto entity:

### Terms

- `Station`: Stanice (např. celostátní Plus, dále regionální)
- `Show`: Pořad vysílaný na jedné či více stanicích.
- `Serial`: Série epizod (asi potřeba lépe definovat)
- `Schedule`: Program vysílání (naše priorita)
- `Episode`: Epizoda pořadu
- `Genre`: Žánr epizody/pořadu
- `Person`: Osoba vystupující v epizodě (pouze moderátor nikoliv host)
- `Topic`: Téma epizody/pořadu

### Facts and Rules

- Na stanici se vysílají epizody jednotlivých pořadů.
- Jeden pořad, respektive jeho epizody se mohou vysílat na dvou stanicích zároveň (např. Plus/Radiožurnál a regionální stanice).
- Každý pořad má určeno, kdy a s jakou periodou se vysílá jeho premiéry a reprízy.

### Filters

- *stanice* např Plus, Radiožurnál
- *období* (dny) např. od 1. 1. 2023 do 1. 2. 2023 
- *rozsah* (čas) např. od 12:00 do 15:00 
- *název* pořadu např. Zprávy
- *premiéra/repríza*

## Installation

- Create a virtual environment (recommended).
  
	Unix (Use desired version of Python e.g 3.11.)
  
	```shell
	python -m venv .venv
  ```
  Windows (Use the [`py.exe`](https://docs.python.org/3/using/windows.html) launcher.)
  
	```powershell
	py -3.11 -m venv .venv
  ```
 
- Activate the virtual environment.
  
	Unix
  
	```shell
	source .venv/bin/activate
  ````
  Windows
  
	```powershell
	.venv\Scripts\activate
  ```
 
- Upgrade pip to latest version (recommended).

	```shell
	pip install --upgrade pip
	```

- Install required packages for development (editable mode).
	
	```shell
	pip install -e .[dev]
	```
- Run a tests.
    
	```shell
	pytest
	```

- Build documentation.
	
	```shell
	todo
	```
## Documentation

- api documentation 

<https://rapidoc.croapp.cz/>

- rapi client documentation
<./docs/build/index.html>

## Usage

### Configure
 
The runtime variables are assigned in following order.
 
1. flags
2. environment
3. config file
4. hard-coded defaults


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

- get station guid (globaly unique id)
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



