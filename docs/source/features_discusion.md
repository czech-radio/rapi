# Features discussion
## Dotaz pro pana Kubelíka na rAPI:
### otázky: Jan Kačaba
1) Potřebovali bychom získat pro zadaný pořad:
a) datum a čas premiér epizody (tj. kdy byla daná epizoda vysílána poprvé)
b) datum a čas repríz epizody (tj. kdy byla daná epizoda opakovaně vysílána)

2) Jaký je prosím rozdíl mezi:
https://api.mujrozhlas.cz a https://mujrozhlas.croapi.cz

3) Je někde podrobnější dokumentace než na adrese https://rapidoc.croapp.cz/?

4) Jaký je rozdíl:
/schedule-day a /schedule-day-flat

5) Jak prosím filtrovat dle stanice?
a) Zkouším filter dle příkladu (https://mockservice.croapp.cz/mock)
https://api.mujrozhlas.cz/schedule-day-flat?station=radiozurnal
result: invalid_parameter_value

b)
Zkouším tyto filtry a bohužel dostanu vždy stejný počet záznamů který není filtrován dle stanice.
https://api.mujrozhlas.cz/schedule-day-flat?station=4082f63f-30e8-375d-a326-b32cf7d86e02
https://api.mujrozhlas.cz/schedule-day-flat?station=c639d927-f37b-3db8-a64f-1d64ee1469b2
https://api.mujrozhlas.cz/schedule-day-flat?station=0134ce01-8684-3556-b568-f208392ac0bd
https://api.mujrozhlas.cz/schedule-day-flat?station=0134ce01-8684-3556-b568-f208392ac0bd
https://api.mujrozhlas.cz/schedule-day-flat?filter[station]=radiozurnal
https://api.mujrozhlas.cz/schedule-day-flat?filter[station]=0134ce01-8684-3556-b568-f208392ac0bd


c) filtrování dle data a stanice:
toto funguje (filtrace jen dle data):
https://api.mujrozhlas.cz/schedule?filter[since][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&page[limit]=500

Následně jsem zkoušel různé varianty s filtrem stanice: (Ani jedna nefunguje: code: "non_filterable_field"

https://api.mujrozhlas.cz/schedule?filter[since][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[relationships.station.data.id]=0134ce01-8684-3556-b568-f208392ac0bd&page[limit]=500

https://api.mujrozhlas.cz/schedule?filter[since][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[station.data.id]=0134ce01-8684-3556-b568-f208392ac0bd&page[limit]=500

https://api.mujrozhlas.cz/schedule?filter[since][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[station.id]=0134ce01-8684-3556-b568-f208392ac0bd&page[limit]=500

https://api.mujrozhlas.cz/schedule?filter[since][ge]=2023-09-17T8:00&filter[till][le]=2023-09-17T9:00&filter[station_code]=5&page[limit]=500

### odpovědi: Jan Hejzl
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
https://api.mujrozhlas.cz/schedule-day-flat-sparse?filter[day]=2023-06-21&filter[stations.id]=4082f63f-30e8-375d-a326-b32cf7d86e02&filter[keepZV]=true
... (filter[keepZV]=true slouží pro zahrnutí Zelené vlny, aby se obešlo pravidlo skrytí epizod kratších než 3 minuty)

Pokud potřebujete filtrovat nějak konkrétně, napište mi, co potřebujete, mrknu se, co všechno EP podporuje a jak to dát dohromady.

### závěr
Croapi nenabízí žádný takový endpoint
Šlo implementovat pravděpodobně jen s replikou databáze případně stažením všech dat s endpointu /schedule to trvá velmi dlouho už pro jediný den. Zkoušel jsem stáhnout vše a trvalo to celou noc a ještě nebyl konec.
To by nemusel být problém. Data by se stáhli jednou a pak by se jen dělal denní update.
Byl vznesen dotaz na pana Kubelíka, jestli není nějaká jiná možnost