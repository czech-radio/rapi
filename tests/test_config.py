import configparser
import json
import os
import sys

import pytest
from ruamel.yaml import YAML

from rapi import _config
from rapi import _helpers as hp


def test_config_yml_default():
    cfg = _config.config_yml_default()
    hp.pp(cfg)
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
    ["test", "par"],
    "env",
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
    var_path_srt = hp.str_join_no_empty(var_path_list)
    EVARS.append(var_path_srt)


### TESTS
def test_Cfg_default() -> None:
    cfg = _config.Cfg_default()
    val = cfg.get(TIN[0])
    assert val


def test_Cfg_file() -> None:
    # cfg = _config.Cfg_file("./defaults_alt.yml")
    cfg = _config.Cfg_file("./tests/data/defaults_alt.yml")
    val = cfg.get(TIN[0])
    assert val


def test_Cfg_env() -> None:
    print()
    ### prepare
    for i in range(len(TIN)):
        os.environ[EVARS[i]] = str(TOUT[i])
    ### test
    cfg = _config.Cfg_env()
    print(cfg.cfg)


def test_Cfg_params() -> None:
    print()
    sys.argv = ["test3.py", "-vv", "--test-par=par", "-di=10"]
    # sys.argv = ["test3.py", "-vv"]
    cfg = _config.Cfg_params()
    val = cfg.get(["verbose"])
    assert val == 2
    val = cfg.get(["test", "par"])
    assert val == "par"


def test_Config_defaults() -> None:
    print()
    # sys.argv = ["test3.py", "-vv", "--test-par=par", "-di=10"]
    sys.argv = ["test3.py"]
    Cfg = _config.Config()
    Cfg.cfg_runtime_set_defaults()


def test_Config() -> None:
    print()
    ### prepare
    for i in range(len(EVARS)):
        os.environ[EVARS[i]] = str(TOUT[i])
    Cfg = _config.Config()

    ### test
    val = Cfg.cfg_default.get(TIN[0])
    assert val

    ### add sources
    #### param source
    sys.argv = ["test3.py", "--test-par=par", "-vv"]
    cfgp = _config.Cfg_params()
    # print(cfgp.cfg)

    #### env source
    cfge = _config.Cfg_env()
    # print(cfge.cfg)

    #### file source
    cfgf = _config.Cfg_file("./tests/data/defaults_alt.yml")

    ### add sources in order of preference
    # Cfg.add_sources([cfge])
    Cfg.add_sources([cfgf])
    # Cfg.add_sources([cfge, cfgf])
    # Cfg.add_sources([cfgp, cfge, cfgf])

    Cfg.cfg_runtime_set()
    # hp.pp(Cfg.cfg_runtime)
