import urllib.parse

import pandas as pd

from rapi import Client
from rapi.helpers import helpers as hp

pd.set_option('display.max_colwidth', None)
import logging

log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.DEBUG)
cl = Client()

# # Get stations shows
shows = list(cl.get_station_shows("11"))
spdf = pd.DataFrame(shows,columns=["uuid", "title",])
spdf_uniq=spdf.drop_duplicates(subset=['title'])
assert len(spdf)==len(spdf_uniq)

# EPISODES
## Get show episodes
for show_idx in range(len(spdf)):
    show_title=spdf['title'].values[show_idx]
    print(show_idx,show_title)
    show_uuid=spdf['uuid'].values[show_idx]
    eps=list(cl.get_show_episodes(show_uuid))
    epspdf=pd.DataFrame(eps,columns=['uuid','title','since','till'])


    ## Get episodes filter
    epars=urllib.parse.quote(show_title)
    link=f"schedule"
    epsf=cl._get_endpoint_full_json(link)
    if len(epsf) > 0:
        print("correct",len(epsf),show_idx,show_title,show_uuid)
    break



