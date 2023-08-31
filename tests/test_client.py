import sys
from typing import Union

from rapi import _client, _config, _helpers, _model, _params

### test setup
sys.argv = [
    "test3.py",
    "-vv",
]
Cfg = _config.CFG()
Cfg.cfg_runtime_set_defaults()


def test_get_swagger() -> None:
    print()
    acr = _client.Client(Cfg)
    acr.get_swagger()


def test_save_swagger() -> None:
    print()
    acr = _client.Client(Cfg)
    ok = acr.save_swagger()
    assert ok


def test_DB_local_endp_get_json() -> None:
    print()
    acr = _client.DB_local(Cfg)
    res = acr.endp_get_json("stations", 300)
    assert res is not None


def test_DB_local_endp_save_json() -> None:
    print()
    acr = _client.DB_local(Cfg)
    ok = acr.endp_save_json("stations", 300)
    assert ok


def test_DB_local_endps_save_json() -> None:
    print()
    acr = _client.DB_local(Cfg)
    acr.endps_save_json(300)


def test_DB_local_csv_update() -> None:
    print()
    acr = _client.DB_local(Cfg)
    acr.endps_csv_update(10)


def test_DB_local_endp_get_full_json() -> None:
    print("kuk")
    acr = _client.DB_local(Cfg)
    jdict=acr.endp_get_full_json("stations", 9)
    assert len(jdict)==27
    # _helpers.pp(jdict)
