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
# # Get all shows for given station
# ## Create client
# %%
from rapi import Client

cl = Client()

# %% [markdown]
# ## Create station shows iterator
# - by default station identificator is openmedia id
# %%
shows_iterator = cl.get_station_shows("11")
shows = list(shows_iterator)

# %% [markdown]
# ## Number of shows
# %%
print(len(shows))

# %% [markdown]
# ## List shows as python object
# %%
print(shows[:3])

# %% [markdown]
# ## List shows as string object
# %%
for sh in shows[:3]:
    print(sh)

