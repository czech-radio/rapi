import logging
import urllib.parse

import pandas as pd

from rapi import Client

pd.set_option("display.max_colwidth", None)

cl = Client()


log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.DEBUG)

show_noepsschedule = "9f36ee8f-73a7-3ed5-aafb-41210b7fb935"
show_withepsschedule = "c7374f41-ae14-3b5c-8c04-385e3241deb4"
sch1 = cl.get_show_episodes_schedule(show_noepsschedule)
sch2 = cl.get_show_episodes_schedule(show_withepsschedule)

# Get stations shows
shows = list(cl.get_station_shows("11"))
spdf = pd.DataFrame(
    shows,
    columns=[
        "uuid",
        "title",
    ],
)
spdf_uniq = spdf.drop_duplicates(subset=["title"])
assert len(spdf) == len(spdf_uniq)
print(spdf)

## Get show episodes
for s in range(len(spdf)):
    show_idx = s
    show_title = spdf["title"].values[show_idx]
    print(s, show_title)
    show_uuid = spdf["uuid"].values[show_idx]
    show_uuid1 = "9f36ee8f-73a7-3ed5-aafb-41210b7fb935"
    eps = list(cl.get_show_episodes(show_uuid))
    epspdf = pd.DataFrame(eps, columns=["uuid", "title", "since", "till"])

    # Get show episodes schedule
    epssch = list(cl.get_show_episodes_schedule(show_uuid))

    # Get episodes filter
    epars = urllib.parse.quote(show_title)
    link = "episodes?filter[since]=2014-10-02"
    epsf = cl._get_endpoint_full_json(link)
    if len(epsf) > 0:
        print("correct", len(epsf), show_idx, show_title, show_uuid)
