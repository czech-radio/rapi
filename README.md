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

Fakta:
- Na stanici se vysílají epizody jednotliváýh pořadů.
- Jeden pořad, respektive jeho epizody se mohou vysílat na dvou stanicích zárověň (Plus/Radiožurnál a regionální stanice).
- Každý pořad má přidělěn identifikátor.
- Každý pořad má určeno, kdy a s jakou periodou se vysílá jeho premiéra a reprízy.

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
* create virtual env  
`python -m venv .venv`
`source .venv/bin/activate`
-no sure if correct
`pip install --upgrade pip` ?

* install required packages
`pip install -e .[dev]`
