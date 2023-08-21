import sys
from typing import Union

from rapi import client, config, helpers, model, params

### test setup
sys.argv = [
    "test3.py",
    "-vv",
]
Cfg = config.CFG()
Cfg.cfg_runtime_set_defaults()


def test_get_stations() -> None:
    print()
    api = client.API(Cfg)
    st = api.get_stations(10)
    print(st)
    assert st is not None


def test_get_station() -> None:
    print()
    api = client.API(Cfg)
    id = api.get_station(str(11))
    print(id)


def test_get_station_shows() -> None:
    api = client.API(Cfg)
    # data = api.get_station_shows(str(11),500)
    data = api.get_station_shows(str(11), 500)
    print(data)
