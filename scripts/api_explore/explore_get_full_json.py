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

# EPISODES
## Get show episodes
for show_idx in range(len(spdf)):
    show_title = spdf["title"].values[show_idx]
    print(show_idx, show_title)
    # show_uuid=spdf['uuid'].values[show_idx]
    # plink=f"schedule?filter[title][like]="
    # eps=list(cl.get_show_episodes(show_uuid))
    # epspdf=pd.DataFrame(eps,columns=['uuid','title','since','till'])

# plink=f"schedule?filter[title][like]="
# filter_string=cl._get_endpoint_full_json(link)
# filter_string="00004622-799e-3679-8b9d-54fde4e9f776"
# filter_string="Hitparáda"
# filter_string=urllib.parse.quote(show_title)
# link=f"{plink}{filter_string}"
# res=cl._get_endpoint_full_json(link)
# print("positive",show_idx,len(res))
