---
hide-toc: true
---

# RAPI

Balík `rapi` je knihovna, která dotazuje rest api dostupné na adrese <https://api.mujrozhlas.cz> například tento endpoint <https://api.mujrozhlas.cz/stations>, který vrátí metadata všech stanic ve formě JSON. JSON formát je nutné pro využití v analýzách sparsovat/reprezentovat jako objekt. Tato knihovna tedy převádí JSON textové řetězce na python objekty nebo list objektů, které lze přímo využít při analýze.

## Usage

1. nejdříve se vytvoří instance rapi clientu
2. následně se pomocí rapi clienta zavolá požadovaná funkce s požadovanými parametry:
například: chci získat všechny pořady pro zadanou stanici. Standardně je id stanice číslo tzv. openmedia_id. Tabulka id stanic je [zde](../../src/rapi/data/stations_ids.csv)
3. rapi client vrátí objekt, který obsahuje jednotlivé stanice: list[Stations], se kterým lze přímo pracovat jako s list of dictionaries nebo lze převést jednoduše na pandas dataframe: pandas.DataFrame(data). Tento dataframe lze pak uložit jako csv soubor, nebo s ním pracovat podobně jako s tabulkou.


```{toctree}
:maxdepth: 2
:caption: Overview
:hidden:

original
```

```{toctree}
:maxdepth: 2
:caption: Examples
:hidden:

notebooks/get_stations.ipynb
notebooks/get_shows_for_the_given_station.ipynb
notebooks/get_episodes_for_the_given_show.ipynb
notebooks/get_participants_for_the_given_show.ipynb
notebooks/get_schedules_for_the_given_show.ipynb
notebooks/explore_data_with_pandas.ipynb
```

```{toctree}
:maxdepth: 2
:caption: Development
:hidden:

contributing
discusion
```

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

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
