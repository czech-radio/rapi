import configparser
import os

import pytest

from rapi import config


def test_var_from_env() -> None:
    var = config.var_from_env("", "PATH")
    assert var


def test_var_from_cfg() -> None:
    cfg = configparser.ConfigParser()
    cfgfile = "./config.ini"
    assert os.path.exists(cfgfile), f"File '{cfgfile}' does not exist."
    cfg.read(cfgfile)
    var = config.var_from_cfg(cfg, "test", "cfg_loaded")
    assert var


def test_load_from_cfg() -> None:
    print()
    config.get_cfg_vars("../config.ini")
