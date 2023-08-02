import configparser
import logging
import os
import pkgutil
import types
from typing import Any, Optional, Union

import yaml

from rapi import helpers, params
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo

# from mergedeep import merge


__version__ = "0.0.1"


### dict_get_path: get subset of dictionary giving list of path or keyname
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


### default config
def config_yml_default():
    dats = pkgutil.get_data(__name__, "data/defaults.yml")
    assert dats is not None
    # cfg=yaml.load(dats,Loader=yaml.FullLoader)
    cfg = yaml.load(dats, Loader=yaml.SafeLoader)
    return cfg


class Cfg_default:
    def __init__(self):
        self.cfg = config_yml_default()
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


### config from user provided file
def config_yml_file(file: str) -> dict:
    with open(file, "r") as f:
        data = yaml.safe_load(f)
        return data


class Cfg_file:
    def __init__(self, file: str):
        self.cfg = config_yml_file(file)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


#### Try to find env var predefined in input dictionary. The env var name is constructed from joined dictionary path
def env_vars_cfg_paths(
    dcfg: dict, pathlists: list = [], pathidx: int = 0, cnames: list = []
) -> list:
    ps = pathlists
    pi = pathidx
    for key, val in dcfg.items():
        if pi + 1 > len(ps):
            ps.append([])
        if isinstance(val, (str, int, bool)):
            envname = helpers.str_join_no_empty([*cnames, key])
            env_val = helpers.env_var_get(envname)
            if env_val is not None:
                if len(cnames) > 0:
                    ps[pi] = ps[pi] + cnames
                ps[pi].append(key)
                pi = pi + 1
        elif isinstance(val, dict):
            cn = cnames.copy()
            cn.append(key)
            ps = env_vars_cfg_paths(val, ps, pi, cn)
    return ps


def env_vars_intersection(dcfg: dict) -> dict:
    paths = env_vars_cfg_paths(dcfg)
    dictr: dict = {}
    for p in paths:
        envval = helpers.env_var_get("_".join(p))
        if envval is not None:
            helpers.dict_create_path(dictr, p, envval)
    return dictr


class Cfg_env:
    def __init__(self):
        self.cfg = env_vars_intersection(config_yml_default())
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


# def params_vars_cfg_intersection():


### config from commandline params (flags) union with default config
def params_vars_cfg_union(cfg_in: dict, pars: dict, section: str = ""):
    cfg = cfg_in
    for k in cfg:
        ### simple string
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            val = pars.get(keyname, None)
            if val is not None:
                logo.debug(f"taking var from par: {k}, value: {val}")
                cfg[k] = val
        ### is dict
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            logo.debug(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = params_vars_cfg_union(scfg, pars, keyname)
            cfg[k] = modscfg
        ### not implemented for other types
        else:
            raise TypeError(f"cannot parse type: {type(cfg[k])}")
    return cfg


class Cfg_params:
    def __init__(self):
        pars = vars(params.args_read())
        self.cfg = params_vars_cfg_union(config_yml_default(), pars, "")
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


class CFG:
    # def __init__(self, cfg_sources: Union[list[dict[str,any]], None] = None):
    def __init__(self) -> None:
        self.cfg_default = Cfg_default()
        self.cfg_sources: list = []
        self.cfg_runtime: dict = {}

    def add_sources(self, cfg_sources: list[Any]) -> None:
        # NOTE: mayebe add check if type implements interface method get or has dict
        for s in cfg_sources:
            if s is not None:
                self.cfg_sources.append(s)

    def cfg_runtime_set(self) -> None:
        srcs = self.cfg_sources
        res: dict = {}
        ### merge all sources
        if srcs is None or len(srcs) == 0:
            self.cfg_runtime = self.cfg_default.cfg
        else:
            if self.cfg_default.cfg is not None:
                srcs.append(self.cfg_default)
            for s in reversed(srcs):
                res = helpers.deep_merge_dicts(s.cfg, res)
        self.cfg_runtime = res
