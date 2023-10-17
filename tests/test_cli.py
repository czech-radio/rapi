import sys

import pytest

from rapi._command import commands
from rapi.config._config import Config


@pytest.mark.command
def test_version():
    sys.argv = ["rapi", "--debug-cfg"]
    config = Config("rapi")
    config.cfg_runtime_set_defaults()
    commands(config)


@pytest.mark.command
def test_test_logs_lv1():
    sys.argv = ["rapi", "--test-logs", "-v"]
    config = Config("rapi")
    config.cfg_runtime_set_defaults()
    commands(config)


@pytest.mark.command
def test_test_logs_lv2():
    sys.argv = ["rapi", "--test-logs", "-vv"]
    config = Config("rapi")
    config.cfg_runtime_set_defaults()
    commands(config)
