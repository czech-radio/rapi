import argparse
import configparser
import copy
import logging
import os
import pkgutil
import types
from typing import Any, Optional, Union
import sys

import yaml
from ruamel.yaml import YAML

from rapi import helpers, params
from rapi.logger import log_stderr as loge
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


def parse_yaml_comments():
    dats = pkgutil.get_data(__name__, "data/defaults.yml")
    return dats
    # y = YAML(typ='safe')  # Use 'safe' type to preserve comments
    # y = YAML(typ='rt')  # Use 'safe' type to preserve comments
    # assert dats is not None
    # cfg = y.load(dats)
    # return cfg


### default config
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


### config from user provided file
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
    # TODO: maybe use alt method when using runtime_cfg_set:
    # traverse the default config constructing path vectors along the way, then try using the vector and concatenated vector to get value i.e. Cfg_?.get_path_value(vec,cvec) if not None skip trying the remaining Cfg_? sources. Then construct the particular cfg dict from path or incorporate the value to default cfg.
    # (This would eliminate traversing default cfg each time.)
    # or maybe use dict.update(odict)
    # maybe crreate package config/env.py, config/file.py, cofig/cfg.py
    def __init__(self):
        self.cfg = env_vars_dict_intersec(config_yml_default())
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)
        # helpers.pp(self.cfg)


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
        argpars = params.params_yml_config()
        pars = argpars.parse_args()
        self.pars = pars
        pars = vars(pars)
        self.cfg = params_vars_cfg_intersec(config_yml_default(), pars)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)
        # helpers.pp(self.cfg)


class CFG:
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
        ### merge in all sources in order of increasing priority
        if srcs is None or len(srcs) == 0:
            self.cfg_runtime = self.cfg_default.cfg
        else:
            for s in reversed(srcs):
                tmps = copy.deepcopy(s.cfg)
                res = helpers.deep_merge_dicts(tmps, res)
        ### finaly merge with defaults.yml which should contain full set of variables
        res = helpers.deep_merge_dicts(res, self.cfg_default.cfg)
        self.cfg_runtime = res

    def runtime_get(self, path: list):
        val = helpers.dict_get_path(self.cfg_runtime, path)
        return val
