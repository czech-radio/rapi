import configparser
import json
import os
import sys

import pytest

from rapi import config, helpers, params


def test_config_yml_default():
    cfg = config.config_yml_default()
    test = cfg["test"]
    assert test
    print(test)
    val = test["cfg_loaded"]
    assert val
    print(val)


### TESTS PREPARE
TCASES = [
    # ["test", "cfg_loaded"], "ich_bin_loaded",
    ["test", "cfg_loaded"], "fenv",
    ["test", "env"], "fenv",
    ["nomek"], "Hello, world!",
]
TIN = []
TOUT = []
EVARS = []
for t in range(0, len(TCASES), 2):
    ### CREATE INPUTS
    var_path_list = TCASES[t]
    TIN.append(var_path_list)
    ### CREATE OUTPUTS
    var_value = TCASES[t + 1]
    TOUT.append(var_value)
    ### CREATE ENV
    var_path_srt = helpers.str_join_no_empty(var_path_list)
    EVARS.append(var_path_srt)


### TESTS
def test_Cfg_default():
    cfg = config.Cfg_default()
    val = cfg.get_value(TIN[0])
    assert val


def test_Cfg_file():
    cfg = config.Cfg_file("./defaults_alt.yml")
    val = cfg.get_value(TIN[0])
    assert val


def test_Cfg_env():
    ### prepare
    for i in range(len(TIN)):
        os.environ[EVARS[i]] = TOUT[i]
    ### test
    cfg = config.Cfg_env()
    for k in cfg.cfg:
        print(cfg.cfg[k])
    for i in range(len(TIN)):
        val = cfg.get_value(TIN[i])
        assert val == TOUT[i]


def test_Cfg_params():
    sys.argv = ["test3.py", "-vv"]
    cfg = config.Cfg_params()
    val = cfg.get_value(["verbose"])
    assert val == 2


def test_CFG() -> None:
    ### prepare
    for i in range(len(TIN)):
        os.environ[EVARS[i]] = str(TOUT[i])
    cfg = config.CFG()

    ### test
    val = cfg.cfg_default.get_value(TIN[0])
    assert val

    ### add sources
    #### param source
    sys.argv = ["test3.py", "--test-par", "-vv"]
    cfgp = config.Cfg_params()

    #### env source
    cfge = config.Cfg_env()

    #### file source
    cfgf = config.Cfg_file("./defaults_alt.yml")

    ### add sources in order of preference
    # cfg.add_sources([cfge,cfgp,cfgf])
    # cfg.add_sources([cfge,cfgp,cfgf])
    cfg.add_sources([cfgf])

    cfg.set_cfg_runtime()
