import sys
from typing import Union

from rapi import broadcast, config, helpers, model, params
from rapi.api_croapp import Api_croapp
from rapi.helpers import analyze as an
from rapi.helpers import pprint as pp
from rapi.helpers import ptype as pt

### test setup
sys.argv = [
    "test3.py",
    "--broadcast",
    "-vv",
]
Cfg = config.CFG()
Cfg.cfg_runtime_set_defaults()


def test_api_croapp() -> None:
    print()
    AC = Api_croapp(Cfg)
    # AC.get_endpoint_json("stations")
    AC.update_local_db()
