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
# ## Get all available stations
# ### Create client
# %%
from rapi import Client

cl = Client()

# %% [markdown]
# ### Create stations iterator
# %%
stations_iterator = cl.get_stations()
stations = list(stations_iterator)

# %% [markdown]
# ### Number of stations
# %%
print(len(stations))

# %% [markdown]
# ### List stations as python object
# %%
print(stations[:3])

# %% [markdown]
# ### List stations as string object
# %%
for st in stations[:3]:
    print(st)

