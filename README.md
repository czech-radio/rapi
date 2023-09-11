# rapi

**The REST Python client for <https://rapidoc.croapp.cz/>.**

- maintainer: Jan Kačaba
- repository: <https://github.com/czech-radio/rapi>

Under the term Python client, think of classes, methods and functions that will allow you to work with data obtained with the REST API
as Python objects.

## Features (cs)

- [ ] Získej všechny pořady aktuálně vysílané na zadané stanici.
- [ ] Získej všechny epizody vysíláné pro zadaný pořad, období, časový úsek a stanici.
- [ ] Získej všechny moderátory pro zadaný pořad.
- [ ] Získej premiéry a reprízy pro zadaný pořad.

## Model (Terms, Facts, Rules)

Doménový model jsoy třídy reprezentující jednotlivé objekty se musí namodelovat s citem.
Zatím jasně vídíme tyto entity:

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
- Jeden pořad, respektive jeho epizody se mohou vysílat na dvou stanicích zárověň (např. Plus/Radiožurnál a regionální stanice).
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

Test the REST API <https://rapidev.croapp.cz/> with CURL (use `-g, --globoff flag`) e.g.

```shell
curl -g -X GET "https://rapidev.croapp.cz/stations?page[offset]=0&page[limit]=4" -H  "accept: application/vnd.api+json"
```
