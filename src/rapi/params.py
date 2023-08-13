import argparse as AP
import os
import pkgutil
import re
import sys
from typing import Dict, Union

from ruamel.yaml import YAML
from ruamel.yaml.tokens import CommentToken

from rapi import config
from rapi import helpers
from rapi import helpers as hp
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo
import builtins


class HelpAction(AP.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


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

    ### no parameter given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    # helpers.pprint(vars(params))
    return params


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
### print yaml file
# 8. mutually exlusive group?
### solved partialy by commands
# 9. choises? from comment above: e.g.:
# verbose: [1:3]
# verbose: [1,2,3]
# 10. explore if code ijections is not possible, otherwise it must be treated.
# 11. count? (from comment above)
# 12. yaml parser which can parse comments or try to parse using reading line by line
### maybe use inline comment and split the string


def parse_all(cfg: dict) -> AP.Namespace:
    parser = AP.ArgumentParser()

    parse_flags(cfg, parser)
    cmds = cfg.get("commands", None)
    if cmds is not None:
        parse_commands(cmds, parser)

    args = parser.parse_args()
    return args


def parse_flags(
    config: dict, parser: Union[AP.ArgumentParser, None] = None
) -> AP.ArgumentParser:
    if parser is None:
        parser = AP.ArgumentParser()
    pvs = helpers.dict_paths_vectors(config, list())
    for pvec in pvs:
        basep = pvec[0]
        if basep != "commands":
            # pathstr="--"+"-".join(pvec)
            default = (helpers.dict_get_path(config, pvec),)
            # print(pvec,str(default[0]))
            hp.pt(default[0])
            # parser.add_argument(
            # pathstr,
            # "-v",
            # action="count",
            # default=helpers.dict_get_path(config,pvec),
            # required=False,
            # help="logging verbosity (-v for INFO, -vv for DEBUG)",
            # )

    #  break
    # parser.add_argument(p[0],action="store_true")
    return parser


def parse_commands(
    cmds: dict, parser: Union[AP.ArgumentParser, None] = None
) -> AP.ArgumentParser:
    if parser is None:
        parser = AP.ArgumentParser()
    subp = parser.add_subparsers(title="subcommands")
    for cmd in cmds:
        cmdp = subp.add_parser(cmd, help="request " + cmd)
        cmdp.add_argument("-f", "--filter", type=str)
    return parser


def parse_comment(comm: CommentToken):
    cline = comm.value
    strip_leading = r"^#\s*"
    sline = re.sub(strip_leading, "", cline)
    cvec = sline.split(";")
    form1 = r"^\s*"
    form2 = r"\n\s*#"
    form3 = r"\n"
    for i in range(len(cvec)):
        sc = re.sub(form1, "", cvec[i])
        sc = re.sub(form2, "", sc)
        sc = re.sub(form3, "", sc)
        cvec[i] = sc
    return cvec

def param_specs(commvec: list,key: str):
    # pass
    res=list()
    if len(commvec)==4:
        ### short version
        res.append("-"+commvec[0])
        ### long version
        # res.append("--"+key)
    return res

def params_add_argument(ap: AP.ArgumentParser,commvec: list,key: str):
    # ap.add_argument(
            # )
    return ap

def params_yml_config():
    dats = pkgutil.get_data(__name__, "data/defaults.yml")
    argpars = AP.ArgumentParser()
    # y = YAML(typ='safe')
    # y = YAML(typ='rt')
    yl = YAML()
    cfg = yl.load(dats)
    # print("hex",getattr(builtins,"int"))
    for i in cfg.ca.items:
        comment = cfg.ca.items[i][2]
        if comment is not None:
            # print(i, cfg[i])
            ### check type of input againts specified in config
            c = parse_comment(comment)
            if len(c) > 3:
                print(c)
                argpars.add_argument(
                    ### short version
                    c[0],
                    ### long version
                    "--" + i,
                    required=False,
                    default=cfg[i],
                    action=c[2],
                    help=c[3]
### type converts param value to type or with callable function
                    ### choices
                )
    return argpars
