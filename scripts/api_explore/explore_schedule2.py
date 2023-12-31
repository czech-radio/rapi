import logging

import pandas as pd

from rapi import Client

pd.set_option("display.max_colwidth", None)

cl = Client()

log_stdout = logging.getLogger("log_stdout")

show = "2226c3be-7f0d-3c82-af47-0ec6abe992a8"
station = "4082f63f-30e8-375d-a326-b32cf7d86e02"

#
schedule = list(cl.get_schedule(show, station))
print("number of episodes", len(schedule))
frame_schedule = pd.DataFrame(schedule, columns=["since", "title"])
print(frame_schedule)

#
show_episodes = list(cl.get_show_episodes(show))
print("nuber of episodes", len(show_episodes))
frame_show_episodes = pd.DataFrame(show_episodes, columns=["since", "title"])
print(frame_show_episodes)

#
show_episodes_schedule = list(cl.get_show_episodes_schedule(show))
print("nuber of episodes", len(show_episodes_schedule))
frame_show_episodes_schedule = pd.DataFrame(
    show_episodes_schedule, columns=["since", "title"]
)
print(frame_show_episodes_schedule)
