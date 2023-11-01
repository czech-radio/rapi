import pytest

from rapi import _model
from rapi._station_ids import StationIDs


@pytest.fixture
def station_ids():
    _station_ids = StationIDs()
    return _station_ids


@pytest.mark.station_ids
def test_that_primary_keys_are_retuned(station_ids) -> None:
    result = station_ids.get_primary_keys()
    assert len(result) > 0


# FIXME Use better naming for all methods bellow.
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
    sid = _model.StationIDs().__dict__
    for key in sid:
        assert station_ids.get_fkey("11", sid[key])
