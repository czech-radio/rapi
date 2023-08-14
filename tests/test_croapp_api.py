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


def test_get_stations() -> None:
    print()
    api = api_croapp.API(Cfg)
    st = api.get_stations(10)
    assert st is not None


def test_get_station() -> None:
    print()
    api = api_croapp.API(Cfg)
    id = api.get_station(str(11))
    print(id)

def test_get_station_shows() -> None:
    api = api_croapp.API(Cfg)
    # data = api.get_station_shows(str(11),500)
    data = api.get_station_shows(str(11),500)
    print(data)
