import configparser
import copy
import pkgutil
import sys
from typing import Any, Union

import yaml as yaml

from rapi import __version__, _client, _helpers
from rapi import _helpers as helpers
from rapi._logger import log_stderr as loge
from rapi.config import _params


__all__ = "Config"


# dict_get_path: get subset of dictionary giving list of path or keyname
def dict_get_path(
    dictr: dict, path: list[str]
) -> Union[dict, list, str, None]:
    dicw = dictr
    for i in path:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict


def config_ini_default() -> configparser.ConfigParser:
    cfg_parser = configparser.ConfigParser()
    dats = pkgutil.get_data(__name__, "data/defaults.ini")
    assert dats is not None
    dats_txt = dats.decode("utf-8")
    cfg_parser.read_string(dats_txt)
    return cfg_parser


def parse_yaml_comments():
    dats = pkgutil.get_data(__name__, "data/defaults.yml")
    return dats
    # y = YAML(typ='rt')  # Use 'safe' type to preserve comments
    # assert dats is not None
    # cfg = y.load(dats)
    # return cfg


# default config
def config_yml_default() -> dict:
    dats = pkgutil.get_data(__name__, "data/defaults.yml")
    assert dats is not None
    # cfg=yaml.load(dats,Loader=yaml.FullLoader)
    cfg = yaml.load(dats, Loader=yaml.SafeLoader)
    return cfg


class Cfg_default:
    def __init__(self):
        self.cfg = config_yml_default()
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


# config from user provided file
def config_yml_file(file: str) -> dict:
    try:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        loge.debug("user config file not read")
        return {}


class Cfg_file:
    def __init__(self, file: str):
        self.cfg = config_yml_file(file)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


#### Try to find env var predefined in input dictionary. The env var name is constructed from joined dictionary path
def env_vars_dict_intersec(dcfg: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg, list())
    dictr: dict = {}
    for p in paths:
        val = helpers.env_var_get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr


class Cfg_env:
    # NOTE: maybe use alt method when using runtime_cfg_set:
    # traverse the default config constructing path vectors along the way, then try using the vector and concatenated vector to get value i.e. Cfg_?.get_path_value(vec,cvec) if not None skip trying the remaining Cfg_? sources. Then construct the particular cfg dict from path or incorporate the value to default cfg.
    # (This would eliminate traversing default cfg each time.)
    # or maybe use dict.update(odict)
    # maybe crreate package config/env.py, config/file.py, cofig/cfg.py
    def __init__(self):
        self.cfg = env_vars_dict_intersec(config_yml_default())
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


def params_vars_cfg_intersec(dcfg: dict, pars: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg, list())
    dictr: dict = {}
    for p in paths:
        val = pars.get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr


# ArgumentParser(prog='pytest', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)
class Cfg_params:
    def __init__(self):
        argpars = _params.params_yml_config()
        launcher = helpers.filepath_to_vector(sys.argv[0])[-1]
        sysargbak = sys.argv
        match launcher:
            case "rapi":
                pass
            case _:
                # e.g. "ipykernel_launcher.py"
                sys.argv = ["rapi"]
            # NOTE: calling from playbook sys.argv is set to some bullshit ['/home/user/rapi/.venv/lib/python3.11/site-packages/ipykernel_launcher.py', '-f', '/home/user/.local/share/jupyter/runtime/kernel-d916e01b-a4eb-42eb-998a-ec7eeb156cff.json'] so commandline args cannot be properly defined/parsed
        try:
            pars = argpars.parse_args()
        except BaseException as e:
            raise ValueError(
                f"__name__={__name__}, __package__={__package__}, sys.argv={sys.argv}, launcher={launcher}, err: {e}"
            )
        sys.argv = sysargbak
        self.pars = pars
        pars = vars(pars)
        self.cfg = params_vars_cfg_intersec(config_yml_default(), pars)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)
        # print("fuck")


class Config:
    def __init__(self) -> None:
        self.cfg_default = Cfg_default()
        self.cfg_sources: list = []
        self.cfg_runtime: dict = {}

    def cfg_runtime_set_defaults(self):
        cfgp = Cfg_params()
        cfge = Cfg_env()
        path = ["cfg", "file"]
        cfgd = Cfg_default()
        cfg_fname = helpers.get_first_not_none(path, [cfgp, cfge, cfgd])
        cfgf = None
        if cfg_fname is not None:
            cfgf = Cfg_file(cfg_fname)
        self.add_sources([cfgp, cfge, cfgf])
        self.cfg_runtime_set()

    def add_sources(self, cfg_sources: list[Any]) -> None:
        # NOTE: maybe add check if type implements interface method get or has dict
        for s in cfg_sources:
            if s is not None:
                self.cfg_sources.append(s)

    def cfg_runtime_set(self) -> None:
        srcs = self.cfg_sources
        res: dict = {}
        # merge in all sources in order of increasing priority
        if srcs is None or len(srcs) == 0:
            sys.argv = ["rapi", "-v"]
            self.cfg_runtime = self.cfg_default.cfg
        else:
            for s in reversed(srcs):
                tmps = copy.deepcopy(s.cfg)
                res = helpers.deep_merge_dicts(tmps, res)
        # finaly merge with defaults.yml which should contain full set of variables
        res = helpers.deep_merge_dicts(res, self.cfg_default.cfg)
        self.cfg_runtime = res

    def runtime_get(self, path: list, dvalue: Any = ValueError) -> Any:
        val = helpers.dict_get_path(self.cfg_runtime, path)
        if val is None:
            try:
                isexcp = isinstance(dvalue(), Exception)
            except Exception:
                return dvalue
            if isexcp:
                raise dvalue(f"cannot get path: {path}")
            else:
                return dvalue
        return val


def commands(cfg: Config) -> None:
    getvar = cfg.runtime_get

    ### set log level
    vlevel = getvar(["verbose"])
    set_loglevel(vlevel)

    ### test logs
    run = getvar(["test", "logs"])
    test_logs(run)

    ### print version
    print_version(cfg)

    ### debug cfg
    run = getvar(["debug", "cfg"])
    debug_cfg(run, cfg)

    ### subcommands
    subc = getvar(["subcommand"], None)
    if subc is None:
        return
    else:
        logo.info(f"running command: {subc}")

    if "station" == subc:
        croapp = _client.Client(cfg)
        # print(vars(ap))
        # guid = croapp.get_station_guid("11")
        # print(guid)

    if "show" == subc:
        pass


def print_version(cfg: Config) -> None:
    if cfg.runtime_get(["version"]):
        print(__version__)
        sys.exit(0)


def set_loglevel(level: int = 0):
    if level == 0:
        loglevel = logging.WARN
    if level == 1:
        loglevel = logging.INFO
    if level == 2:
        loglevel = logging.DEBUG
    logo.setLevel(loglevel)
    loge.setLevel(loglevel)


def test_logs(run: bool):
    if run is False:
        return
    logo.debug("this is debug_level message")
    logo.info("this is info_level message")
    logo.warning("this is warning_level message")
    loge.error("this is error_level message")
    sys.exit(0)


def debug_cfg(run: bool, cfg: Config):
    if run is False:
        return
    data = cfg.cfg_runtime
    _helpers.pp(data)
    sys.exit(0)


import argparse as AP
import pkgutil
import re
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.tokens import CommentToken

from rapi._logger import log_stdout as logo


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
        ### NOTE: default value is given in defaults.yml. If default is set in here, there is problem when merging with env or with values from alt file. If params given on commanline has higest prioriy in config sources, the default values will overwrite even though they are not explicitly given on commandline.
        # default=keyval,
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


def parse_commands(cmds: dict, ap: AP.ArgumentParser):
    subp = ap.add_subparsers(dest="subcommand", title="subcommands")
    for cmd in cmds:
        cmdp = subp.add_parser(cmd, help="request " + cmd)
        cmdp.add_argument("-f", "--filter", type=str)
        cmp = cmds.get(cmd, None)
        # cmp: <class 'ruamel.yaml.comments.CommentedMap'>
        if cmp is not None:
            # print(type(cmp))
            # print(cmd, cmp.ca)
            # params_yml_comments(cmp, cmdp, "--"+cmd)
            params_yml_comments(cmp, cmdp, "--commands-" + cmd)


def parse_subcommand_flag(cm: CommentedMap):
    for key in cm.ca.items:
        print(key)
        print(cm.ca.items[key][2])
