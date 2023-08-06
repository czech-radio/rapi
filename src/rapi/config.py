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
def env_vars_dict_intersec(dcfg: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg)
    dictr: dict = {}
    for p in paths:
        val = helpers.env_var_get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr


class Cfg_env:
    # TODO: maybe use alt method when using runtime_cfg_set:
    # traverse the default config constructing path vectors along the way, then try using the vector and concatenated vector to get value i.e. Cfg_?.get_path_value(vec,cvec) if not None skip trying the remaining Cfg_? sources. Then construct the particular cfg dict from path or incorporate the value to default cfg.
    # (This would eliminate traversing default cfg each time.)
    # or maybe use dict.update(odict)
    # maybe crreate package config/env.py, config/file.py, cofig/cfg.py
    def __init__(self):
        self.cfg = env_vars_dict_intersec(config_yml_default())
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


def params_vars_cfg_intersec(dcfg: dict, pars: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg)
    dictr: dict = {}
    for p in paths:
        val = pars.get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr


class Cfg_params:
    def __init__(self):
        pars = vars(params.args_read())
        self.cfg = params_vars_cfg_intersec(config_yml_default(), pars)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


class CFG:
    def __init__(self) -> None:
        self.cfg_default = Cfg_default()
        self.cfg_sources: list = []
        self.cfg_runtime: dict = {}

    def add_sources(self, cfg_sources: list[Any]) -> None:
        # NOTE: maybe add check if type implements interface method get or has dict
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

    def runtime_get(self, path: list):
        val = helpers.dict_get_path(self.cfg_runtime, path)
        return val
