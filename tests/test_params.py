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
    sys.argv = ["test3.py", "-vv","--dbool"]
    # sys.argv = ["test3.py", "-vv"]
    argp = params.params_yml_config()
    pars = argp.parse_args()
    # print(pars)
    # print(vars(pars))
    # dats=config.parse_yaml_comments()
    # hp.pl(cfg["debug"].ca)


def test_parse_commands() -> None:
    print()
    sys.argv = ["test3.py", "--verbose", "station", "-f=hello"]
    argsp = params.parse_commands(cmds)
    argsp.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="logging verbosity (-v for INFO, -vv for DEBUG)",
    )
    args = argsp.parse_args()
    print(args.__dict__)


def test_parse_all() -> None:
    print()
    # sys.argv = ["test3.py","--verbose","station", "-f=hello"]
    # sys.argv = ["test3.py","station", "-f=hello"]
    # sys.argv = ["test3.py","--verbose", "show", "-f=hello"]
    # sys.argv = ["test3.py","--verbose","show"]
    # sys.argv = ["test3.py","--verbose","station","-f"]
    # sys.argv = ["test3.py","--verbose","station","-f=kfda"]
    sys.argv = ["test3.py"]
    args = params.parse_all(cfg.cfg)
    # argsp=params.parse_commands(cmds)
    # argsp.add_argument(
    # "-v",
    # "--verbose",
    # action="count",
    # default=0,
    # help="logging verbosity (-v for INFO, -vv for DEBUG)",
    # )
    print(args.__dict__)
