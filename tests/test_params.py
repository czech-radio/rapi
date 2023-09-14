import argparse as AP
import sys

from rapi import _helpers as hp
from rapi.config import _config, _params

cfg = _config.Cfg_default()
cmds = cfg.get(["commands"])


def test_params_yml_config() -> None:
    sys.argv = ["test3.py", "-vv"]
    argp = _params.params_yml_config()
    pars = argp.parse_args()
