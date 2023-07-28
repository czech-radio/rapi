import configparser
import json
import os

import pytest

from rapi import config

cfgfile = "./config.ini"
cfg = config.config_parse(cfgfile)
assert os.path.exists(cfgfile), f"File '{cfgfile}' does not exist."
cfg.read(cfgfile)


def test_cfg() -> None:
    print()
    pdic = {section: dict(cfg[section]) for section in cfg.sections()}
    pdicj = json.dumps(pdic, indent=4)
    print(pdicj)


def test_var_from_env() -> None:
    var = config.var_from_env("","PATH")
    assert var


def test_var_from_cfg() -> None:
    var = config.var_from_cfg("test", "cfg_loaded", cfg)
    assert var


def test_get_var() -> None:
    ### VAR NOT DEFINED
    var = config.get_var("", "dummy_val", cfg)
    assert var is None

    ### VAR ONLY IN CONFIG
    var = None
    var = config.get_var("test", "cfg_loaded", cfg)
    assert var

    ### VAR ONLY IN ENV
    var = None
    myvar_name = "MY_VARIABLE"
    myvar_value = "Hello, World!"
    os.environ[myvar_name] = myvar_value
    var = config.get_var(myvar_name, "", cfg)
    assert var == myvar_value
