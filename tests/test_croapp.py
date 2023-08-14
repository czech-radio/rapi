import sys
from typing import Union

from rapi import api_croapp, config, helpers, model, params

### test setup
sys.argv = [
    "test3.py",
    "-vv",
]
Cfg = config.CFG()
Cfg.cfg_runtime_set_defaults()


def test_get_swagger() -> None:
    print()
    acr = api_croapp.API(Cfg)
    acr.get_swagger()


def test_save_swagger() -> None:
    print()
    acr = api_croapp.API(Cfg)
    ok=acr.save_swagger()
    assert ok


def test_DB_local_csv_endpoint_get_json() -> None:
    print()
    acr = api_croapp.DB_local_csv(Cfg)
    res = acr.endpoint_get_json("stations",300)
    assert res is not None

def test_DB_local_csv_endpoint_save_json() -> None:
    print()
    acr = api_croapp.DB_local_csv(Cfg)
    ok = acr.endpoint_save_json("stations",300)
    assert ok

def test_DB_local_csv_endpoints_save_json() -> None:
    print()
    acr = api_croapp.DB_local_csv(Cfg)
    acr.endpoints_save_json(300)

def test_DB_local_csv() -> None:
    print()
    acr = api_croapp.DB_local_csv(Cfg)
    acr.update_db()


def test_API() -> None:
    api = api_croapp.API(Cfg)
    api.get_station("11")
    # api.get_station_guid("11")
