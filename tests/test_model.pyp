import pytest

from rapi import _model
from rapi.helpers import helpers


@pytest.mark.model
def test_str_patcher() -> None:
    print(_model.StationIDs())


@pytest.mark.model
def test_station_anotation():
    # _helpers.class_assign_attrs_by_anotation(
    # _model.station_anotation,
    # )
    pass
