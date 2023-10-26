# Overview

## API URLs

- [REST API URL](https://api.mujrozhlas.cz)
- [REST API Documentation](https://rapidoc.croapp.cz/)
- [REST API Swagger Specification](https://rapidoc.croapp.cz/apifile/openapi.yaml)

## Domain model overview

- `Station`
- `Show`
- `Episode`
- `ScheduleEpisode`
- `Person` (participant/moderator)

### Episode vs ScheduleEpisode

- ScheduleEpisode je programová epizoda, kterou nám dodává systém AIS. Slouží většinou jen k zobrazení v programu, v některých případech k vytváření samotných 'episode' epizod (více způsoby). Epizoda typu 'episode' je pak základní kámen celého obsahu v rAPI stejně jako webu mujRozhlas. Ta už má přímou a jistou (deterministickou) návaznost na pořady, seriály, případně stanice.
- scheduleEpisode (since/till), to je opravdu čas vysílání (plánovaného vysílání), a opravdu bez rozlišení premiéry/reprízy.
- Můžete to brát tak, že scheduleEpisodes jsou hrubá data, která slouží spíš procesu vytváření obsahu, než že by odpovídala obsahu samotnému.
- Vztah episode a scheduleEpisode je spíš obsahový a nepřímý.
- Vztah scheduleEpisode a show je obsahově takový, že scheduleEpisode vzniká přímo z dat AISu, podle kterých vytváříme poměrně komplikovanou heuristikou show. Důležité je, že i když jsou tyto pořady mezi běžně, editorsky vytvářenými pořady v DB, v pohodě se může stát, že když jsou data z AISu nešikovně poskládaná, pro každou epizodu nějakého seriálu může ad hoc vzniknout pořad, který se použije pouze pro zobrazení v programu. V řadě případů se ale dohromady spárují s existujícím pořadem správně (jako třeba v tom příkladu, co posíláte). Spárování na úrovni programu (schedule) je jen pro optiku, obsahově potřebujeme rozumný titulek do programu a tím to v podstatě hasne. Tam vůbec nezáleží na tom, jestli se scheduleEpisode v DB přiřadí správně k pořadu Zprávy, nebo k pořadu Páteční zprávy 123.
- ScheduleEpisodes a z nich odvozené pořady, shows, jsou víceméně dočasná záležitost. Vůbec to nelze brát ani jako archiv čehokoli, protože za normálního stavu je po půl roce mažeme. Teď toho tam bude víc, protože jsme nechali mazání od letního hacku dočasně vypnuté kvůli rekonstrukci dat.
- Není moc jak zjistit, jestli je to nová věc, nebo věc vydaná znovu po dvou letech na jiné stanici. (Spousta pořadů probíhá samozřejmě na více stanicích a stanice si je navzájem přebírají.)

## Endpoints and client methods

- `/stations`
  - `Client.get_stations()`:  returns all stations
  - `Client.get_station("11")`: -> returns station with given id

- `/stations/{show_guid}/shows`
  - `Client.get_station_shows()`

- `/shows/{show_guid}`: returns show object
  - `Client.get_show()`
  - `Client.get_show_participants_with_roles()`
      (calls Client.get_person for each member guid in participants relation table and filters result by role="moderator".)
`/shows/{show_guid}/participants`: returns persons (participants/moderators)
  - `Client.get_show_participants()`

- `/shows/{show_guid}/schedule-episodes`
  - `Client.get_show_episodes()`
  - `Client.show_episodes_filter()`

- `/shows/{show_guid}/schedule-episodes?sort=since`
  - `Client.get_show_episodes_schedule`
- `/schedule`: vrací scheduleEpisodes podle posloupnosti vysílání bez ohledu na to, jestli se jedná o premiéru/reprízu. asi nejstarší s nejširší podporou filtrů, nevýhoda je v tom, že by měl obsahovat celou strukturu včetně zanořených položek (což je pro běžný provoz a filtraci málo praktické), časově se musí filtrovat explicitně (něco jako since/till)
  - `Client.get_schedule()`
  - `Client.get_schedule_by_date()`

- `/schedule-day`: vrací scheduleEpisode
  program pro den, pokud vím, nepoužívá se podobně jako /schedule, protože obsahuje vnořené položky
  - `Client.get_station_schedule_day`

- `/schedule-day-flat`: vrací scheduleEpisode, program pro den bez vnořených položek (relationship)
  - `Client.get_station_schedule_day_flat`
- `/schedule-day-flat-sparse`: vrací scheduleEpisode, program pro den bez vnořených položek + bez epizod kratších než 4 minuty

- `/persons/{person_guid}`
  - `Client.get_person()`

## Použití filtrů při přímém volání api

<https://api.mujrozhlas.cz/schedule-day-flat-sparse?filter[day]=2023-06-21&filter[stations.id]=4082f63f-30e8-375d-a326-b32cf7d86e02&filter[keepZV]=true>

- filter[keepZV]=true slouží pro zahrnutí Zelené vlny, aby se obešlo pravidlo skrytí epizod kratších než 3 minuty)

## REST API with CURL

Uyou can call REST API with CURL `-g/--globoff` flag e.g.

```shell
curl -g -X GET "https://rapidev.croapp.cz/stations?page[offset]=0&page[limit]=4" -H  "accept: application/vnd.api+json"
```
