import logging
import urllib.parse

import pandas as pd

from rapi import Client
from rapi.helpers import helpers as hp

pd.set_option('display.max_colwidth', None)
cl = Client()
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.DEBUG)

link=f"schedule"
epsf=cl._get_endpoint_full_json(link)



