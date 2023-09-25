import logging

import pytest


# @pytest.fixture(autouse=True,scope="session")
def log_settings() -> None:
    lg = logging.getLogger("log_stdout")
    lg.setLevel(logging.DEBUG)
