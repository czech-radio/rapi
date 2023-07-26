import pytest

from rapi import config


def test_load_from_cfg():
    config.get_cfg_vars("../config.ini")
