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
# # Get all participants for given show
# ## Create client
# %%
from rapi import Client
cl = Client()

# %% [markdown]
# ## Create show participants iterator
# - by default station identificator is openmedia id
# %%
show_uuid = "c7374f41-ae14-3b5c-8c04-385e3241deb4"
participants_iterator = cl.get_show_moderators(show_uuid)
participants = list(participants_iterator)

# %% [markdown]
# ## Number of participants
# %%
print(len(participants))

# %% [markdown]
# ## List participants as python object
# %%
print(participants[:3])

# %% [markdown]
# ## List participants as string object
# %%
for p in participants[:3]:
    print(p)

