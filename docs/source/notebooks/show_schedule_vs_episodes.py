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
# # Get schedules for given show
# ## Create client
# %%
from rapi import Client

cl = Client()

# %% [markdown]
# ## Get schedule

# %%
import pandas as pd
show="2226c3be-7f0d-3c82-af47-0ec6abe992a8"
station="4082f63f-30e8-375d-a326-b32cf7d86e02"
since="2023-09-01"
till="2023-10-01"

# %%
data = list(cl.get_schedule(show))
print(len(data))
pdata=pd.DataFrame(data)
output_file_path='../../../runtime/get_schedule.csv'
pdata.to_csv(output_file_path)

# %%
data = list(cl.get_show_episodes(show))
print(len(data))
pdata=pd.DataFrame(data)
output_file_path='../../../runtime/get_show_episodes.csv'
pdata.to_csv(output_file_path)

