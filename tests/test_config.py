import configparser
import json
import os

import pytest

from rapi import config, params

### fixtures
cfg = config.config_default()


def test_config_default_parse():
    cfg = config.config_default()
    assert cfg is not None


def test_cfg() -> None:
    print()
    pdic = {section: dict(cfg[section]) for section in cfg.sections()}
    pdicj = json.dumps(pdic, indent=4)
    print(pdicj)


def test_var_from_env() -> None:
    var = config.var_from_env("", "PATH")
    assert var


def test_var_from_cfg() -> None:
    var = config.var_from_cfg("test", "cfg_loaded", cfg)
    assert var


def test_Cfg_default():
    CFG = config.Cfg_default()
    val = CFG.get_var("test", "cfg_loaded")
    print(val)


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


def test_set_runtime_var() -> None:
    var_sources = [
        config.config_default,
        params.args_read,
    ]
    var = config.set_runtime_var("test", "cfg_loaded", var_sources)
    print(var)
