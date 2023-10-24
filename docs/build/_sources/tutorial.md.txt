# rapi userguide

## Použití

- rapi je knihovna, která dotazuje rest api dostupné na adrese <https://api.mujrozhlas.cz> například tento endpoint <https://api.mujrozhlas.cz/stations>, který vrátí metadata všech stanic ve formě JSON. JSON formát je nutné pro využití v analýzách sparsovat/reprezentovat jako objekt.
Tato knihovna tedy převádí JSON textové řetězce na python objekty nebo list objektů, které lze přímo využít při analýze.

## Příklad použití (workflow)

1. nejdříve se vytvoří instance rapi clientu
2. následně se pomocí rapi clienta zavolá požadovaná funkce s požadovanými parametry:
například: chci získat všechny pořady pro zadanou stanici. Standardně je id stanice číslo tzv. openmedia_id. Tabulka id stanic je [zde](../../src/rapi/data/stations_ids.csv)
3. rapi client vrátí objekt, který obsahuje jednotlivé stanice: list[Stations], se kterým lze přímo pracovat jako s list of dictionaries nebo lze převést jednoduše na pandas dataframe: pandas.DataFrame(data). Tento dataframe lze pak uložit jako csv soubor, nebo s ním pracovat podobně jako s tabulkou.

## Jednotlivé příklady použití

- Pořady na zadané stanici [usage](./notebooks/station_shows.ipynb)
- Epizody vysílané pro zadaný pořad, období, časový úsek a stanici. [usage](./notebooks/show_episodes.ipynb)
- Moderátoři pro zadaný pořad. [usage](./notebooks/moderators.ipynb)
- Plán vysílaných epizod pro zadaný pořad, stanici, období, časový úsek [usage](./notebooks/show_schedules.ipynb)
- Příklad prozkoumání objektu v pandas
[usage](./notebooks/explore_in_pandas.ipynb)

## Dokumentace

- api url:
<https://api.mujrozhlas.cz>

- api original "documentation"
<https://rapidoc.croapp.cz/>

- rapi client documentation
[documentation index](index.rst)


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
