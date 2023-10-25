import logging

import pandas as pd

from rapi import Client

pd.set_option("display.max_colwidth", None)
cl = Client()
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.DEBUG)

# # Get stations shows
shows = list(cl.get_station_shows("11"))
spdf = pd.DataFrame(shows, columns=["uuid", "title", ""])
spdf_uniq = spdf.drop_duplicates(subset=["title"])
assert len(spdf) == len(spdf_uniq)

## Get show episodes
for show_idx in range(len(spdf)):
    show_title = spdf["title"].values[show_idx]
    print(show_idx, show_title)
