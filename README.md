# rapi

[![main](https://github.com/czech-radio/rapi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/czech-radio/rapi/actions/workflows/main.yml)

**The REST Python client for <https://rapidoc.croapp.cz/>.**

- maintainer: Jan Kačaba
- repository: <https://github.com/czech-radio/rapi>

Under the term Python client, think of classes, methods and functions that will allow you to work with data obtained with the REST API
as Python objects.

## Features (cs)

- [x] 1. Získej všechny pořady aktuálně vysílané na zadané stanici. [usage](./docs/build/notebooks/client_usage.html#get-all-shows-for-given-station)
- [x] 2. Získej všechny epizody vysílané pro zadaný pořad, období, časový úsek a stanici.
- [x] 3. Získej všechny moderátory pro zadaný pořad.
- [ ] 4. Získej premiéry a reprízy pro zadaný pořad.

### Features discussion
4. 
Croapi nenabízí žádný takový endpoint
Šlo implementovat pravděpodobně jen s replikou databáze případně stažením všech dat s endpointu /schedule to trvá velmi dlouho už pro jediný den. Zkoušel jsem stáhnout vše a trvalo to celou noc a ještě nebyl konec.
To by nemusel být problém. Data by se stáhli jednou a pak by se jen dělal denní update.
Byl vznesen dotaz na pana Kubelíka, jestli není nějaká jiná možnost

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

## Usage

### Configure
 
The runtime variables are assigned in following order.
 
1. flags
2. environment
3. config file
4. hard-coded defaults


### Use as library

### Use as program

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



