import sys
from typing import Union

# from rapi.api_croapp import Api_croapp
from rapi import api_croapp, broadcast, config, helpers, model, params

### test setup
sys.argv = [
    "test3.py",
    "--broadcast",
    "-vv",
]
Cfg = config.CFG()
Cfg.cfg_runtime_set_defaults()


def test_DB_local_csv() -> None:
    print()
    acr = api_croapp.DB_local_csv(Cfg)
    acr.update_db()


def test_API() -> None:
    api = api_croapp.API(Cfg)
    api.get_station("11")
    # api.get_station_guid("11")
