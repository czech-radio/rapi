import argparse as AP
import sys

from rapi.config._config import Config, _params

cfg = Config()
cfg.cfg_runtime_set_defaults()
cmds = cfg.runtime_get(["commands"])


def test_params_yml_config() -> None:
    sys.argv = ["test3.py", "-vv"]
    argp = _params.params_yml_config()
    pars = argp.parse_args()
