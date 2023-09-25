import sys

import pandas as pd
import pytest

from rapi._client import Client
from rapi.config._config import Config
from rapi.helpers import helpers
from rapi.helpers._logger import log_stdout as logo


@pytest.fixture
def client():
    sys.argv = ["rapi", "-vv"]
    cfg = Config("rapi")
    cfg.cfg_runtime_set_defaults()
    _client = Client(cfg)
    assert _client
    return _client


@pytest.mark.client_debug
def test_get_endpoint(client) -> None:
    endpoints = [
        "schedule-day",
        "schedule-day-flat",
        "schedule-day-current",
        "program",
        "schedule/{id}",
    ]
    res = client._get_endpoint("schedule-day-flat")
    assert res
    print(res)
