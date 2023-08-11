import sys
from rapi import params
from rapi import config
from rapi import helpers as hp

cfg=config.Cfg_default()
cmds=cfg.get(["commands"])

def test_parse_commands()->None:
    print()
    sys.argv = ["test3.py","--verbose","station", "-f=hello"] 
    argsp=params.parse_commands(cmds)
    argsp.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="logging verbosity (-v for INFO, -vv for DEBUG)",
    )
    args=argsp.parse_args()
    print(args.__dict__)

def test_parse_all()->None:
    print()
    # sys.argv = ["test3.py","--verbose","station", "-f=hello"] 
    # sys.argv = ["test3.py","station", "-f=hello"]
    sys.argv = ["test3.py","show", "-f=hello"]
    args=params.parse_all(cmds)
    # argsp=params.parse_commands(cmds)
    # argsp.add_argument(
        # "-v",
        # "--verbose",
        # action="count",
        # default=0,
        # help="logging verbosity (-v for INFO, -vv for DEBUG)",
    # )
    print(args.__dict__)
