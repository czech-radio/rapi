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


def test_get_station() -> None:
    print()
    api = _client.Client(Cfg)
    station = api.get_station(str(11))
    assert station
    print(station)


def test_get_stations() -> None:
    print()
    api = _client.Client(Cfg)
    stations = api.get_stations(10)
    assert len(stations) == 27
    print(stations)


def test_get_station_shows() -> None:
    api = _client.Client(Cfg)
    # data = api.get_station_shows(str(11),500)
    data = api.get_station_shows(str(11), 500)
    print(data)
