import pytest

from rapi import _model
from rapi._station_ids import StationIDs


@pytest.fixture
def station_ids():
    _station_ids = StationIDs()
    assert _station_ids
    return _station_ids


@pytest.mark.station_ids
def test_get_pkey_list(station_ids) -> None:
    result = station_ids.get_pkey_list()
    assert result


@pytest.mark.station_ids
def test_get_table(station_ids) -> None:
    result = station_ids.get_table()
    assert result


@pytest.mark.station_ids
def test_get_row_by_pkey(station_ids) -> None:
    result = station_ids.get_row_by_pkey(str(11))
    assert result


@pytest.mark.station_ids
def test_get_fkey(station_ids) -> None:
    si = _model.StationIDs()
    sid = si.__dict__
    for k in sid:
        val = station_ids.get_fkey("11", sid[k])
        assert val
