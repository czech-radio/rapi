import configparser
import json
import os
import sys

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


t1 = ["test", "cfg_loaded"]


def test_Cfg_default():
    cfg = config.Cfg_default()
    val = cfg.get_value(t1)
    assert val


def test_Cfg_file():
    cfg = config.Cfg_file("./defaults_alt.yml")
    val = cfg.get_value(t1)
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
    for k in cfg.cfg:
        print(cfg.cfg[k])
    val = cfg.get_value(t1)
    assert val == myvar_value


def test_Cfg_params():
    sys.argv = ["test3.py", "-vv"]
    cfg = config.Cfg_params()
    val = cfg.get_value(["verbose"])
    assert val == 2


def test_CFG() -> None:
    cfg = config.CFG()
    val = cfg.cfg_default.get_value(t1)
    assert val
    # print(val)

    ### add source
    #### param source
    sys.argv = ["test3.py", "-vv"]
    cfgp = config.Cfg_params()
    #### env source
    myvar_name = "test_cfg_loaded"
    myvar_value = "ich_bin_loaded"
    os.environ[myvar_name] = myvar_value
    cfge = config.Cfg_env()
    #### file source
    cfgf = config.Cfg_file("./defaults_alt.yml")
    cfg.add_source([cfgf,cfge])

    for i in cfg.cfg_sources:
        print(i.get_value(["test"]))
    # cfg.set_cfg_runtime()
