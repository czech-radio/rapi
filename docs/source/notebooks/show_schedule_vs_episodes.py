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
import logging

import pandas as pd

lg = logging.getLogger("log_stdout")
# lg.setLevel(logging.DEBUG)

show="2226c3be-7f0d-3c82-af47-0ec6abe992a8"
station="4082f63f-30e8-375d-a326-b32cf7d86e02"
since="2023-09-01"
till="2023-10-01"

# %%
data1 = list(cl.get_schedule(show))
print(len(data1))
pdata1=pd.DataFrame(data1)
output_file_path='../../../runtime/get_schedule.csv'
pdata1.info()
# pdata.to_csv(output_file_path)

# %%
data2 = list(cl.get_show_episodes(show))
print(len(data2))
pdata2=pd.DataFrame(data2)
pdata2.info()
output_file_path='../../../runtime/get_show_episodes.csv'
# pdata.to_csv(output_file_path)

def FindSameDate(dataframe,value):
    for idx, row in dataframe.iterrows():
        if row['since'] == value:
            print("found",idx)


for idx, row in pdata2.iterrows():
    FindSameDate(pdata1,row['updated'])

out1=list()
for idx, row in pdata2.iterrows():
    out1.append(row['updated'])

out2=list()
for idx, row in pdata1.iterrows():
    out2.append(row['since'])

print(len(out1))
print(len(list(set(out1))))
print(len(out2))
print(len(list(set(out2))))
out3=out2+list(set(out1))
print(len(out3))
