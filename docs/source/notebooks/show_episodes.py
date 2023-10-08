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
# # Get episodes for given show
# ## Create client
# %%
from rapi import Client
cl = Client()

# %% [markdown]
# ## Create episodes iterator
# %%
show_uuid = "739a46c7-35e3-336e-a7d5-08a20b7e7677"
episodes_iterator = cl.get_show_episodes(show_uuid)
episodes = list(episodes_iterator)

# %% [markdown]
# ## Number of episodes
# %%
print(len(episodes))

# %% [markdown]
# ## List episodes as python object
# %%
print(episodes[:3])

# %% [markdown]
# ## List episodes as string object
# %%
for ep in episodes[:3]:
    print(ep)

# %% [markdown]
# ## Filter show episodes by date
# %%
show_uuid = "739a46c7-35e3-336e-a7d5-08a20b7e7677"
since = "2022-01-01T8:00"
to = "2023-01-02T9:00"
episodes_iterator = cl.show_episodes_filter(show_uuid, since, to)
episodes = list(episodes_iterator)
print(len(episodes))
