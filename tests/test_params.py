import argparse as AP
import sys

from rapi import _config
from rapi import _helpers as hp
from rapi import _params

cfg = _config.Cfg_default()
cmds = cfg.get(["commands"])


def test_params_yml_config() -> None:
    print()
    # sys.argv = ["test3.py", "--dbool"]
    # sys.argv = ["test3.py", "-vv"]
    # sys.argv = ["test3.py", "-vv","--dbool", "--dint=hello"]
    # sys.argv = ["test3.py", "--dint"]
    # sys.argv = ["test3.py", "-vv","--test-par"]
    # sys.argv = ["test3.py", "-vv", "--dbool"]
    sys.argv = ["test3.py", "-vv"]
    # sys.argv = ["test3.py", "-vv","station","--id"]
    argp = _params.params_yml_config()
    pars = argp.parse_args()
    # print(pars)
    # print(vars(pars))
    # dats=_config.parse_yaml_comments()
    # hp.pl(cfg["debug"].ca)
