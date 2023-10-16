# rapi

## Použití

- rapi je knihovna, která dotazuje rest api dostupné na adrese <https://api.mujrozhlas.cz> například tento endpoint <https://api.mujrozhlas.cz/stations>, který vrátí metadata všech stanic ve formě JSON. JSON formát je nutné pro využití v analýzách sparsovat/reprezentovat jako objekt.
Tato knihovna tedy převádí JSON textové řetězce na python objekty nebo list objektů, které lze přímo využít při analýze.

## Příklad použití (workflow)

1.nejdříve se vytvoří instance rapi clientu
2. následně se pomocí rapi clienta zavolá požadovaná funkce s požadovanými parametry:
například: chci získat všechny pořady pro zadanou stanici. Standardně je id stanice číslo tzv. openmedia_id. Tabulka id stanic je zde ./src/data/stations_ids.csv
3. rapi client vrátí objekt, který obsahuje jednotlivé stanice: list[Stations], se kterým lze přímo pracovat jako s list of dictionaries nebo lze převézt jednoduše na pandas dataframe: pandas.DataFrame(data). Tento dataframe lze pak uložit jako csv soubor, nebo s ním pracovat podobně jako s tabulkou.

## Jednotlivé příklady použití
- Pořady na zadané stanici [usage](./docs/build/notebooks/station_shows.html)
- Epizody vysílané pro zadaný pořad, období, časový úsek a stanici. [usage](./docs/build/notebooks/show_episodes.html)
- Moderátoři pro zadaný pořad. [usage](./docs/build/notebooks/moderators.html)
- Plán vysílaných epizod pro zadaný pořad, období, časový úsek a stanic [usage](./docs/build/notebooks/show_schedules.html)
- Příklad prozkoumání objektu v pandas
[usage](./docs/build/notebooks/explore_in_pandas.html)

## Dokumentace
- api url: 
<https://api.mujrozhlas.cz>

- api original "documentation"
<https://rapidoc.croapp.cz/>

- rapi client documentation
<./docs/build/index.html>

