# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Library Showcase

# %% [markdown]
# FIXME: Add some description

# %%
# %reload_ext autoreload
# %autoreload 2

# %%
from rapi import Client

# %%
cl = Client()

# %% [markdown]
# ## Get all available stations

# %%
stations = cl.get_stations()
len(list(stations))

# %% [markdown]
# ## Get all shows for given station

# %%
shows = cl.get_station_shows("11")

# %%
list(shows)[:3]

# %% [markdown]
# ## Get particular show by UUID

# %%
cl.get_show("739a46c7-35e3-336e-a7d5-08a20b7e7677")

# %% [markdown]
# ## Get show episodes

# %%
episodes = cl.get_show_episodes("739a46c7-35e3-336e-a7d5-08a20b7e7677")

# %%
list(episodes)[:3]

# %% [markdown]
# ## Filter show episodes by date

# %%
episodes = cl.show_episodes_filter(
    "739a46c7-35e3-336e-a7d5-08a20b7e7677", "2022", "2023"
)

# %%
list(episodes)[:3]

# %%
episodes = cl.show_episodes_filter(
    "739a46c7-35e3-336e-a7d5-08a20b7e7677",
    "2022-08-11",
    "2023-09-11",
)

# %%
list(episodes)[:3]

# %%
eps_schedule = cl.get_schedule("2023-09-17", "2023-09-18")

# %%
list(eps_schedule)[:3]

# %%
eps_schedule = cl.get_schedule("2023-09-17T8:00", "2023-09-17T9:00")

# %%
list(eps_schedule)[:3]

# %% [markdown]
# ### Get schedule filter by date and station (slow)list(eps_schedule)[:3]

# %%
eps_schedule = cl.get_schedule("2023-09-17T8:00", "2023-09-17T9:00", "11")

# %%
list(eps_schedule)[:3]

# %% [markdown]
# ## Get show participants with role

# %%
participants = cl.get_show_participants_with_roles(
    "c7374f41-ae14-3b5c-8c04-385e3241deb4"
)

# %%
list(participants)

# %% [markdown]
# ## Get show moderators

# %%
moderators = cl.get_show_moderators("c7374f41-ae14-3b5c-8c04-385e3241deb4")

# %%
mls = list(moderators)

# %%
print(mls[0])

# %% [markdown]
# ## Get station schedule day

# %% [markdown]
# ### Get station schedule day flat

# %%
day_schedule = cl.get_station_schedule_day_flat("2023-09-11", "11")

# %%
list(day_schedule)[:3]

# %% [markdown]
# ### Get station schedule day

# %%
data = cl.get_station_schedule_day("2023-09-11", "11")

# %%
ldata = list(data)

# %%
ldata[:3]

# %%
ldata[1]

# %%
print(ldata[1])

# %%
