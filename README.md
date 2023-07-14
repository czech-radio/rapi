# rapi

The Python client for <https://rapidoc.croapp.cz/>.

## Zadání

Vytvořme Python klienta pro REST API <https://rapidoc.croapp.cz/>.
Pod pojmem Python klient si představuji třídy, metody a funkce, které umožní pracovat s daty získanými s REST API
jako s objekty nikoliv jako s JSON. 

- Stations: Stanic (celostátní, regionální)
- Shows: Pořady
- Serials: Seriály epizod
- Schedule: Program vysílání
- Episodes: Epizody pořadu
- Genres: Žánry
- Persons: Informace o osobách
- Topics: Témata

Doménový model tj. třídy (entity) reprezentující jednotlivé objekty vracející se z API se musí namodelovat s citem.
Zatím jasně vídíme tyto entity: Stanice (Station), Pořad (Show), Program (Schedule), Epizoda (Episode).

### Fakta

- Na stanici se vysílají epizody jednotlivých pořadů.
- Jeden pořad, respektive jeho epizody se mohou vysílat na dvou stanicích zárověň (např. Plus/Radiožurnál a regionální stanice).
- Každý pořad má určeno, kdy a s jakou periodou se vysílá jeho premiéry a reprízy.

## Use cases

- Získej všechny pořady aktuálně vysíláné na zadané stanici.
- Získej všechny epizody (premiéry)  vysíláné pro zadaný pořad, období, časový úsek a stanici.
- Získej všecny moderátory pro zadaný pořad.
- Získej premiéry a reprízy pro zadaný pořad.

Zatím identifikuji tyto filtry:
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
    ````
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
