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
