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
    ok = acr.save_swagger()
    assert ok


def test_DB_local_endpoint_get_json() -> None:
    print()
    acr = api_croapp.DB_local(Cfg)
    res = acr.endpoint_get_json("stations", 300)
    assert res is not None


def test_DB_local_endpoint_save_json() -> None:
    print()
    acr = api_croapp.DB_local(Cfg)
    ok = acr.endpoint_save_json("stations", 300)
    assert ok


def test_DB_local_endpoints_save_json() -> None:
    print()
    acr = api_croapp.DB_local(Cfg)
    acr.endpoints_save_json(300)


def test_DB_local_csv_update() -> None:
    print()
    acr = api_croapp.DB_local(Cfg)
    acr.endpoints_csv_update(10)
