import pytest

from rapi import _model


@pytest.mark.model
def test_str_patcher() -> None:
    print(_model.StationIDs())
