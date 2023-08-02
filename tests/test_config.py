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
    val = test["cfg_prio"]
    assert val
    print(val)


### TESTS PREPARE
TCASES = [
    ["test", "cfg_prio"],
    "env",
    ["test", "env"],
    "env",
    ["nomek"],
    "fenv",
    ["only_in_env"],
    "fenv",
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
    val = cfg.get(TIN[0])
    assert val


def test_Cfg_file():
    # cfg = config.Cfg_file("./defaults_alt.yml")
    cfg = config.Cfg_file("./tests/defaults_alt.yml")
    val = cfg.get(TIN[0])
    assert val


def test_Cfg_env():
    print()
    ### prepare
    for i in range(len(TIN)):
        os.environ[EVARS[i]] = TOUT[i]
    ### test
    cfg = config.Cfg_env()
    print(cfg.cfg)


def test_Cfg_params():
    print()
    sys.argv = ["test3.py", "-vv", "--test-par"]
    cfg = config.Cfg_params()
    val = cfg.get(["verbose"])
    assert val == 2
    val = cfg.get(["test", "par"])
    assert val is True


def test_CFG() -> None:
    print()
    ### prepare
    for i in range(len(EVARS)):
        os.environ[EVARS[i]] = str(TOUT[i])
    Cfg = config.CFG()

    ### test
    val = Cfg.cfg_default.get(TIN[0])
    assert val

    ### add sources
    #### param source
    sys.argv = ["test3.py", "--test-par", "-vv"]
    cfgp = config.Cfg_params()
    # print(cfgp.cfg)

    #### env source
    cfge = config.Cfg_env()
    # print(cfge.cfg)

    #### file source
    cfgf = config.Cfg_file("./tests/defaults_alt.yml")

    ### add sources in order of preference
    Cfg.add_sources([cfge, cfgp, cfgf])
    # Cfg.add_sources([cfge, cfgf])
    # Cfg.add_sources([cfgf])

    Cfg.cfg_runtime_set()
    print(Cfg.cfg_runtime)
