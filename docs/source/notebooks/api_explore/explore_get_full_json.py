from rapi import Client
from rapi.helpers import helpers as hp
import pandas as pd
import urllib.parse
import logging
pd.set_option('display.max_colwidth', None)
cl = Client()
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.DEBUG)

link=f"schedule"
epsf=cl._get_endpoint_full_json(link)



