import os
import sys
import argparse as AP

import pytest

from rapi.config import _conf_vars as cv
from rapi.config import _conf_pars as cp
from rapi.helpers import helpers as hp
from rapi.config import _conf as cf


@pytest.mark.config
def test_conf_pars()->None:
    sys.argv = ["test3.py", "-vv","--debug-cfg","-tp=10"]
    args=cp.parse_config_dict(cv.configure_dict)
    pars_namespace=args.parse_args()
    print(vars(pars_namespace))

@pytest.mark.config
def test_conf()->None:
    # pass
    sys.argv = ["test3.py", "-vv","--debug-cfg","-tp=10"]
    cfg=cf.Cfg_default()
    val=cfg.get(['test-par'])
    print(val)

@pytest.mark.current
def test_conf_Config()->None:
    sys.argv = ["rapi", "-vv","--debug_cfg","-tp=10"]
    cfg=cf.Config()
    cfg.runtime_set_defaults()
    var=cfg.runtime_get(['test_par'])
    # print(cfg.cfg_runtime)
    print("kek",var)
    var=cfg.runtime_get(['test_env'])
    print("jek",var)
    # apr=AP.ArgumentParser()
    # pn=apr.parse_args()
    # print(vars(pn))

