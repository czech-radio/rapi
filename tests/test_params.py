import argparse as AP
import sys

from rapi import config
from rapi import helpers as hp
from rapi import params

cfg = config.Cfg_default()
cmds = cfg.get(["commands"])


def test_params_yml_config() -> None:
    print()
    # sys.argv = ["test3.py", "--dbool"]
    # sys.argv = ["test3.py", "-vv"]
    # sys.argv = ["test3.py", "-vv","--dbool", "--dint=hello"]
    # sys.argv = ["test3.py", "--dint"]
    # sys.argv = ["test3.py", "-vv","--test-par"]
    sys.argv = ["test3.py", "-vv", "--dbool"]
    # sys.argv = ["test3.py", "-vv"]
    argp = params.params_yml_config()
    pars = argp.parse_args()
    # print(pars)
    # print(vars(pars))
    # dats=config.parse_yaml_comments()
    # hp.pl(cfg["debug"].ca)