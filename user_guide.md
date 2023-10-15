# rapi
## Použití
- rapi je knihovna, která dotazuje rest api dostupné na adrese <https://api.mujrozhlas.cz> například tento endpoint <https://api.mujrozhlas.cz/stations>, který vrátí metadata všech stanic ve formě JSON. JSON formát je nutné pro využití v analýzách sparsovat/reprezentovat jako objekt.
Tato knihovna tedy převádí JSON textové řetězce na python objekty nebo list objektů, které lze přímo využít při analýze.

## Příklad použití (workflow)
1) Nejprve se vytvoří instance rapi clienta.
2) Pomocí rapi clienta lze pak volat požadvouvné funkce, se zadanými parametry. Například chci získat všechny pořady pro zadanou stanici.
3) Rapi client se dotáže implicitně croapi na odpovídající url adresu.
4) Rapi client vrátí python objekt, který lze přímo prozkoumávat po jednotlivých stanicích jako dictionary nebo lze objekt převést na list of dictionaries, případně na padas dataframe a pracovat s objektem jako tabulkou. Případně uložit dataframe jako tabulku do csv souboru.

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

