# Discussion

## TODO

Please, remove when resolved.

- Check the development dependencies in `requirements.txt` and `pyproject.toml` whenever they are up-to-date.
- Check the pytest markers in `pyproject.toml` whenever they are up-to-date.
- Check the script in `scripts/` names and whenever they are up-to-date.
- Change parameter `date_from` and `date_to` to `since` and `till` in `Client.show_episodes_filter()`.

## Automatic schema parsing

url="<https://rapidoc.croapp.cz/apifile/openapi.yaml>"

- the api may change in future
- considering dynamic parsing
- there are currently 3 parsers:
  - swagger-parser
  - openapi-parser
  - openapi3-parser

- I was unable to parse the schema successfully with any of the parsers

- swagger_parser gives error:
Object at "/components/schemas" does not contain key: timeGroupItem_relationships'
- it means there is missing definition for timeGroupItem_relationship. It is only referenced in schema.
- will try adding dummy variable definition

## Stations IDs

- added ./data/stations_ids_table.csv
- compiled table from:
a) <https://github.com/czech-radio/organization/blob/main/analytics/reporting/specification.md#stanice>
b) <https://rapidoc.croapp.cz/stations-all>

- missing or incompatible data for some stations
- the compiled table should be checked by someone else

## src/rapi/__init__.py

**DL (resolved): You must place `py.typed` to the package root diretory.**

-there is problem using mypy.
-importing __version__ from __init__.py to use it in command.py to print version results in error:

src/rapi/command.py:9: error: Skipping analyzing "rapi.__init__": module is installed, but missing library stubs or py.typed marker  [import]
src/rapi/command.py:9: note: See <https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports>

-without iporting __version__ checking with mypy is susccesful

-will have to find another way automatic versioning using "single point of truth" to update: git tag, projcet.toml version, hardcoded version in code, version in README.md

## Dotaz pro pana Kubelíka na rAPI

### Otázky: Jan Kačaba

1) Potřebovali bychom získat pro zadaný pořad:
a) datum a čas premiér epizody (tj. kdy byla daná epizoda vysílána poprvé)
b) datum a čas repríz epizody (tj. kdy byla daná epizoda opakovaně vysílána)

2) Jaký je prosím rozdíl mezi:
<https://api.mujrozhlas.cz> a <https://mujrozhlas.croapi.cz>

3) Je někde podrobnější dokumentace než na adrese <https://rapidoc.croapp.cz/>?

4) Jaký je rozdíl:
/schedule-day a /schedule-day-flat

5) Jak prosím filtrovat dle stanice?
a) Zkouším filter dle příkladu (<https://mockservice.croapp.cz/mock>)
<https://api.mujrozhlas.cz/schedule-day-flat?station=radiozurnal>
result: invalid_parameter_value

b)
Zkouším tyto filtry a bohužel dostanu vždy stejný počet záznamů který není filtrován dle stanice.
<https://api.mujrozhlas.cz/schedule-day-flat?station=4082f63f-30e8-375d-a326-b32cf7d86e02>
<https://api.mujrozhlas.cz/schedule-day-flat?station=c639d927-f37b-3db8-a64f-1d64ee1469b2>
<https://api.mujrozhlas.cz/schedule-day-flat?station=0134ce01-8684-3556-b568-f208392ac0bd>
<https://api.mujrozhlas.cz/schedule-day-flat?station=0134ce01-8684-3556-b568-f208392ac0bd>
<https://api.mujrozhlas.cz/schedule-day-flat?filter[station]=radiozurnal>
<https://api.mujrozhlas.cz/schedule-day-flat?filter[station]=0134ce01-8684-3556-b568-f208392ac0bd>

c) filtrování dle data a stanice:
toto funguje (filtrace jen dle data):
<https://api.mujrozhlas.cz/schedule?filter[since>][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&page[limit]=500

Následně jsem zkoušel různé varianty s filtrem stanice: (Ani jedna nefunguje: code: "non_filterable_field"

<https://api.mujrozhlas.cz/schedule?filter[since>][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[relationships.station.data.id]=0134ce01-8684-3556-b568-f208392ac0bd&page[limit]=500

<https://api.mujrozhlas.cz/schedule?filter[since>][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[station.data.id]=0134ce01-8684-3556-b568-f208392ac0bd&page[limit]=500

<https://api.mujrozhlas.cz/schedule?filter[since>][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[station.id]=0134ce01-8684-3556-b568-f208392ac0bd&page[limit]=500

<https://api.mujrozhlas.cz/schedule?filter[since>][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[station_code]=5&page[limit]=500

### Odpovědi: Jan Hejzl

1. Tohle, obávám se, nepůjde, v rámci rapi se premiéra prostě přepíše reprízou, což plyne z flow redakční systém → rapi. Editoři většinou řeší reprízu tak, že prostě přečasují premiéru, čímž epizodu flow zachytí jako aktualizovanou a obsahově všechno zůstává.

2. To by mělo být jedno a totéž (osobně používám všude spíš api.mujrozhlas.cz).

3. Máte na mysli nějaké konkrétní endpointy? Tohle je po nějakou dobu neudržovaná dokumentace. Nově píšeme vždy aktuální stav společně se vznikajícím EP (dokumentace je u něj v kódu, ne v externím souboru). Takových je, bohužel, zatím poskrovnu a většinou to nejsou EP z těch obsahových. Ta stará dokumentace pokrývá tak 99 % všeho, ale je možné, že jste se trefili právě do toho procenta...

4. Pro program postupně vzniklo několik EP:
a) /schedule -- asi nejstarší s nejširší podporou filtrů, nevýhoda je v tom, že by měl obsahovat celou strukturu včetně zanořených položek (což je pro běžný provoz a filtraci málo praktické), časově se musí filtrovat explicitně (něco jako since/till)
b) /schedule-day -- program pro den, pokud vím, nepoužívá se podobně jako /schedule, protože obsahuje vnořené položky
c) /schedule-day-flat -- program pro den bez vnořených položek
d) /schedule-day-flat-sparse -- program pro den bez vnořených položek + bez epizod kratších než 3 minuty

Programové enpointy nám slouží hlavně pro reálné zobrazení v aplikacích, takže podporují jen velmi omezenou množinu parametrů. Záleží, co potřebujete.

5. Ano, chápu, filtry u těchto programových EP můžou být frustrující. Je to dáno hlavně historickými důvody, kdy docházelo z zpětným úpravám možností daného EP, který už se naostro dlouho používal.
Příklad typické filtrace, jak ji používáme:
<https://api.mujrozhlas.cz/schedule-day-flat-sparse?filter[day]=2023-06-21&filter[stations.id]=4082f63f-30e8-375d-a326-b32cf7d86e02&filter[keepZV]=true>
... (filter[keepZV]=true slouží pro zahrnutí Zelené vlny, aby se obešlo pravidlo skrytí epizod kratších než 3 minuty)

Pokud potřebujete filtrovat nějak konkrétně, napište mi, co potřebujete, mrknu se, co všechno EP podporuje a jak to dát dohromady.

### Závěr

1. Croapi nenabízí žádný endpoint k získání repríz nebo premiér. Datum vysílání premiéry je přepsáno po opakování epizody.

2. Veřejně přístupná dokumentace k croapi neexistuje mimo <https://rapidoc.croapp.cz>.
Není tedy zcela jasné, co jednotlivé endpointy vrací a kde data vznikají. Některé filtry nefungují.

## I DONT KNOW

### station IDs

- csv [file](./src/rapi/data/stations_ids.csv) containing table of station IDs and their equivalents

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

- get station guid (globally unique id)

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
