import argparse as AP
import os
import sys
from typing import Dict

from rapi import config, helpers
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo

class HelpAction(AP.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


# def args_read() -> Dict[str, any]:
### TODO: try to eliminate this, parse params from default config
# https://docs.python.org/3/library/argparse.html#action
# 1. short version will be constructed only for atomic word without delim "_" and first letter will be taken. (multiple words with same starting letter?)
# 2. required will be allways False
# 3. type will be taken from defcfg type
# 4. default value will be taken from defcfg value
# 5. action will be always store
# 6. how to treat nargs? (int, '?', '*', or '+')
# 7. help string? maybe from comment above the name in yaml?
# 8. mutually exlusive group?
# 9. choises? from comment above: e.g.:
# verbose: [1:3]
# verbose: [1,2,3]
# 10. explore if code ijections is not possible, otherwise it must be treated.
# 11. count? (from comment above)
# 12. yaml parser which can parse comments or try to parse using reading line by line


def args_read() -> AP.Namespace:
    parser = AP.ArgumentParser()
    parser.add_argument(
        "-V",
        "--version",
        required=False,
        help="version of program",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="logging verbosity (-v for INFO, -vv for DEBUG)",
    )
    parser.add_argument(
        "--cfg-file",
        required=False,
        type=str,
        help="specify config file",
    ),
    parser.add_argument(
        "--test-par",
        required=False,
        action="store_true",
        help="testing parameter",
    ),
    parser.add_argument(
        "--test-logs",
        required=False,
        help="testing logging",
        action="store_true",
    )
    parser.add_argument(
        "--debug-cfg",
        required=False,
        help="debug cfg, print cfg",
        action="store_true",
    )
    # helpers.ptype(parser)
    # parser.add_argument(
    # "--swagger-download",
    # required=False,
    # nargs="?",
    # type=str,
    # help="download swagger openapi definition yaml file",
    # const="https://rapidoc.croapp.cz/apifile/openapi.yaml",
    # )
    # parser.add_argument(
    # "--swagger-parse",
    # required=False,
    # nargs="?",
    # type=str,
    # help="parse swagger openapi definition yaml file",
    # const="./runtime/rapidev_croapp.yml",
    # )
    # parser.add_argument(
    # "--broadcast",
    # required=False,
    # help="request station data",
    # action="store_true",
    # )
    # parser.add_argument(
    # "--apis-croapp-stations",
    # required=False,
    # help="request station data",
    # action="store",
    # )

    ##TODO: DT:2023/07/17_13:37:47, LV:1
    ###SD: Add mutually exclusive command group
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-a', action='store_true')
    params = parser.parse_args()

    print("fuj", dir(params))
    ### no parameter given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    # helpers.pprint(vars(params))
    return params


def parse_all(commands_definition: dict)->AP.Namespace:
    parser = AP.ArgumentParser()
    parse_commands(commands_definition,parser)
    args = parser.parse_args()
    return args

def parse_commands(cmds: dict, parser: AP.ArgumentParser=None):
    if parser is None:
        parser = AP.ArgumentParser()
    subp=parser.add_subparsers(title="subcommands")
    for cmd in cmds:
        cmdp=subp.add_parser(cmd,help="request "+cmd)
        cmdp.add_argument("-f","--filter",type=str)
    return parser

def pars_command(cmdname: str):
    pass

# def parse_defaults(parser: AP.ArgumentParser):
# pass

# def parse_station(parser: AP.ArgumentParser):
# subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
# station_parser = subparsers.add_parser("station", help="request station")
# station_parser.add_argument("-x", type=int, help="First number")
