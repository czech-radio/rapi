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
# # Explore data in pandas
# ## Create client
# %%
from rapi import Client

cl = Client()

# %% [markdown]
# ## Get schedule

# %%
show="2226c3be-7f0d-3c82-af47-0ec6abe992a8"
station="4082f63f-30e8-375d-a326-b32cf7d86e02"
since="2023_09-01"
till="2023_10-01"

# %%
data = list(cl.get_schedule(show,station,since,till))
import pandas as pd

pdata=pd.DataFrame(data)

# %% [markdown]
# ## Show columns in dataframe
# %%
pdata.info()

# %% [markdown]
# ## Select columns, (subset dataframe)
# %%
sdata=(pdata[['title','since']])
print(sdata)

# %% [markdown]
# ## Select columns when creating dataframe
# %%
data = list(cl.get_schedule(show,station,since,till))
pdata=pd.DataFrame(data,columns=['title','since'])

# %% [markdown]
# ## Save dataframe to csv
# %%
output_file_path='../../../runtime/out.csv'
pdata.to_csv(output_file_path)
