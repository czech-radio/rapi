import configparser
import logging
import os
import pkgutil
import types
from typing import Optional, Union

import yaml

from rapi import helpers, params
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo

__version__ = "0.0.1"


### dict_get: get subset of dictionary giving list of sections or keyname
def dict_get(dictr: dict, sections: list[str]) -> Union[dict, list, str, None]:
    dicw = dictr
    for i in sections:
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
        self.get_value = lambda sections, dictr=self.cfg: dict_get(
            dictr, sections
        )


### config from user provided file
def config_yml_file(file: str) -> dict:
    with open(file, "r") as f:
        data = yaml.safe_load(f)
        return data


class Cfg_file:
    def __init__(self, file: str):
        self.cfg = config_yml_file(file)
        self.get_value = lambda sections, dictr=self.cfg: dict_get(
            dictr, sections
        )


### config from env
def env_var(key: str) -> Union[str, None]:
    return os.environ.get(key, None)


def env_vars(cfg_in, section: str = "") -> dict:
    print(cfg_in)
    cfg = cfg_in
    for k in cfg:
        ### is atom -> get value
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            env_val = env_var(keyname)
            if env_val is not None:
                logo.info(f"taking var from env: {k}, value: {env_val}")
                cfg[k] = env_val
        ### is dict -> recurse
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            logo.info(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = env_vars(scfg, keyname)
            cfg[k] = modscfg
        ### not implemented for other types
        else:
            raise TypeError(f"cannot parse type: {type(cfg[k])}")
    return cfg


class Cfg_env:
    def __init__(self):
        self.cfg = env_vars(config_yml_default())
        self.get_value = lambda sections, dictr=self.cfg: dict_get(
            dictr, sections
        )


### config from commandline params (flags)
def params_vars(cfg_in: dict, pars: dict, section: str = ""):
    cfg = cfg_in
    for k in cfg:
        ### simple string
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            val = pars.get(keyname, None)
            if val is not None:
                logo.info(f"taking var from par: {k}, value: {val}")
                cfg[k] = val
        ### is dict
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            logo.info(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = params_vars(scfg, pars, keyname)
            cfg[k] = modscfg
        ### not implemented for other types
        else:
            raise TypeError(f"cannot parse type: {type(cfg[k])}")
    return cfg


class Cfg_params:
    def __init__(self):
        pars = vars(params.args_read())
        self.cfg = params_vars(config_yml_default(), pars, "")
        self.get_value = lambda sections, dictr=self.cfg: dict_get(
            dictr, sections
        )


class CFG:
    # def __init__(self, cfg_sources: Union[list[dict[str,any]], None] = None):
    def __init__(self):
        self.cfg_default = Cfg_default()
        self.cfg_runtime = self.cfg_default
        self.cfg_sources = Union[list[dict], None]

    def add_sources(self, cfg_sources):
        self.cfg_sources = cfg_sources

    # def set_cfg_runtime(self):
    # for i in self.cfg_sources:
    # print(i)
