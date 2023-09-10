import sys
from typing import Union

import pytest

from rapi import _client, _config, _helpers, _model, _params

### test setup
sys.argv = [
    "test3.py",
    "-vv",
]
Cfg = _config.CFG()
Cfg.cfg_runtime_set_defaults()


@pytest.mark.domain
def test_client() -> None:
    cl = _client.Client()
    station = cl.get_station(str(11))
    assert station


@pytest.mark.domain
def test_get_station() -> None:
    api = _client.Client(Cfg)
    station = api.get_station(str(11))
    assert station


@pytest.mark.domain
def test_get_stations() -> None:
    api = _client.Client(Cfg)
    stations = api.get_stations(10)
    assert len(stations) == 27


@pytest.mark.domain
def test_get_station_shows() -> None:
    api = _client.Client(Cfg)
    data = api.get_station_shows(str(11), 500)
    assert data
    print(data)


sample_shows = [
    "9f36ee8f-73a7-3ed5-aafb-41210b7fb935",
]


@pytest.mark.domain
def test_get_show() -> None:
    api = _client.Client(Cfg)
    data = api.get_show("9f36ee8f-73a7-3ed5-aafb-41210b7fb935", 500)
    assert data


@pytest.mark.domain
def test_get_show_episodes() -> None:
    api = _client.Client()
    data = api.get_show_episodes("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
    # https://mujrozhlas.croapi.cz/shows/9f36ee8f-73a7-3ed5-aafb-41210b7fb935/episodes
    assert data


@pytest.mark.current
@pytest.mark.domain
def test_show_episodes_filter() -> None:
    api = _client.Client()
    data = api.show_episodes_filter(sample_shows[0])
    assert data
    data = api.show_episodes_filter(
        sample_shows[0],
        "2010",
    )
    assert data
    data1 = api.show_episodes_filter(
        sample_shows[0],
        "2014",
        "2014-12",
    )
    data2 = api.show_episodes_filter(
        sample_shows[0],
        "2014",
        "2015-12",
    )
    assert len(data1) < len(data2)
