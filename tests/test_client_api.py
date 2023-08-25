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


def test_get_stations() -> None:
    print()
    api = _client.Client(Cfg)
    st = api.get_stations(10)
    print(st)
    assert st is not None


def test_get_station() -> None:
    print()
    api = _client.Client(Cfg)
    id = api.get_station(str(11))
    print(id)


def test_get_station_shows() -> None:
    api = _client.Client(Cfg)
    # data = api.get_station_shows(str(11),500)
    data = api.get_station_shows(str(11), 500)
    print(data)
