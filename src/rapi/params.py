import argparse as AP
import builtins
import os
import pkgutil
import re
import sys
from typing import Any, Dict, Union

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.tokens import CommentToken

from rapi import helpers
from rapi import helpers as hp
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class HelpAction(AP.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


### NOTE: try to eliminate this, parse params from default config
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


def params_yml_config() -> AP.ArgumentParser:
    dats = pkgutil.get_data(__name__, "data/defaults.yml")
    argpars = AP.ArgumentParser()
    # y = YAML(typ='safe')
    # y = YAML(typ='rt')
    # print("hex",getattr(builtins,"int"))
    yl = YAML()
    cfg = yl.load(dats)
    params_yml_comments(cfg, argpars, "")
    return argpars


def params_add_argument(
    ap: AP.ArgumentParser,
    cvec: list,
    key: str,
    keyval: Any,
):
    ap.add_argument(
        cvec[0],
        ### long version
        key,
        required=False,
        default=keyval,
        action=cvec[2],
        help=cvec[3]
        ### type converts param value to type or with callable function
        ### choices
    )
    return ap


def params_join_keys(pkey, key):
    if pkey != "":
        akey = pkey + "-" + key
    else:
        akey = "--" + key
    return akey


def debug_unparsed_comment(cmv):
    assert len(cmv) == 4
    for i in [0, 1, 3]:
        if cmv[i] is not None:
            logo.info(f"{i}: {cmv[i]}")


def params_yml_comments(cm: CommentedMap, ap: AP.ArgumentParser, pkey: str):
    for key in cm.ca.items:
        ### NOTE: sometimes in ca.items[n] n is 3
        ### precise meaning of returned list unknown
        ### 1. not parsed: lone comment on line is n=1
        ### 2. parsed: normalinline comment
        ### with following lines if any
        ### 3. noparse: complex key without inline comment
        ### if comment follows on next line the comment is n=3
        # debug_unparsed_comment(cm.ca.items[key])
        comment = cm.ca.items[key][2]
        if key == "commands":
            # ### TODO: parse subcommand flags from comment?
            parse_commands(cm[key], ap)
            continue
        if comment is not None:
            ### check type of input againts specified in config
            cvec = parse_comment(comment)
            if len(cvec) > 3:
                akey = params_join_keys(pkey, key)
                params_add_argument(ap, cvec, akey, cm[key])

        if type(cm[key]) is CommentedMap:
            akey = params_join_keys(pkey, key)
            params_yml_comments(cm[key], ap, akey)


def parse_commands(cmds: dict, parser: AP.ArgumentParser):
    subp = parser.add_subparsers(dest='subcommand',title="subcommands")
    for cmd in cmds:
        cmdp = subp.add_parser(cmd, help="request " + cmd)
        cmdp.add_argument("-f", "--filter", type=str)


def parse_command(argp: AP.ArgumentParser, cmdname: str):
    subp = argp.add_subparsers(title="subcommands")
    subp.add_parser(cmdname, help="request " + cmdname)
