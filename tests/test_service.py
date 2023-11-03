import pytest

from rapi import _domain
from rapi._service import StationsProvider


@pytest.fixture
def station_provider():
    _station_provider = StationsProvider()
    return _station_provider


@pytest.mark.service
def test_that_primary_keys_are_retuned(station_provider) -> None:
    result = list(station_provider.station_primary_keys)
    assert len(result) > 0


# FIXME Use better naming for all methods bellow.
@pytest.mark.service
def test_that_station_stored_items_are_retrieved(station_provider) -> None:
    result = station_provider.items
    assert len(result) > 0


# @pytest.mark.service
# def test_thata_station_item_is_found(station_provider) -> None:
#     result = station_provider.get_by_primary_key(str(11))
#     assert result


@pytest.mark.service
def test_get_fkey(station_provider) -> None:
    sid = _domain.StationIDs().__dict__
    for key in sid:
        assert station_provider.find("11", sid[key])
