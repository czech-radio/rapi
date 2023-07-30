import configparser
import json
import os

import pytest

from rapi import config, params


def test_config_yml_default():
    cfg = config.config_yml_default()
    test = cfg["test"]
    assert test
    print(test)
    val = test["cfg_loaded"]
    assert val
    print(val)


def test_CFG() -> None:
    t1 = ["test", "cfg_loaded"]
    cfg = config.CFG(None)
    val = cfg.cfg_default.get_value(*t1)
    assert val

    ### add source
    cfgy = config.config_yml_file("./defaults_alt.yml")
    cfg.add_source([cfgy])
    val = cfg.cfg_runtime.get_value(*t1)
    assert val


def test_Cfg_env():
    print()
    myvar_name = "nomek"
    myvar_value = "Hello, World!"
    os.environ[myvar_name] = myvar_value
    myvar_name = "test_cfg_loaded"
    myvar_value = "ich_bin_loaded"
    os.environ[myvar_name] = myvar_value

    cfg = config.Cfg_env()
    print()
    print("results")
    for k in cfg.cfg:
        print(cfg.cfg[k])
