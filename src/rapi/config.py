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

# from mergedeep import merge


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

### env_vars_paths:
#### Try to find env var predefined in input dictionary. The env var name is constructed from joined dictionary path
def env_vars_paths(dcfg: dict, pathlists: list = [], pathidx: int=0,cnames: list=[]) -> list:
    ps=pathlists
    pi=pathidx
    for key,val in dcfg.items():
        if pi+1 > len(ps):
            ps.append([])
        if isinstance(val, (str, int, bool)):
            envname=helpers.str_join_no_empty([*cnames,key])
            env_val=env_var(envname)
            if env_val is not None :
                if len(cnames) > 1:
                    ps[pi]=ps[pi]+cnames
                ps[pi].append(key)
                pi=pi+1
        if isinstance(val, dict):
            cn=cnames.copy()
            cn.append(key)
            ps=env_vars_paths(val,ps,pi,cn)
    return ps

def dict_add_path(dictr: dict,path: list,val: str="kek"):
    n=0
    for level in path:
        n=n+1
        if level and len(path)>n:
            dictr=dictr.setdefault(level, dict())
        else: 
            dictr=dictr.setdefault(level, val)

def env_vars(dcfg: dict)->dict:
    paths=env_vars_paths(dcfg)
    dictr={}
    for p in paths:
        envval=env_var("_".join(p))
        dict_add_path(dictr,p,envval)
    return dictr


def env_vars2(cfg_in, section: str = "") -> dict:
    cfg = cfg_in
    for k in cfg:
        ### is atom -> get value
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            env_val = env_var(keyname)
            if env_val is not None:
                logo.debug(f"taking var from env: {k}, value: {env_val}")
                cfg[k] = env_val
        ### is dict -> recurse
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            logo.debug(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = env_vars2(scfg, keyname)
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
                logo.debug(f"taking var from par: {k}, value: {val}")
                cfg[k] = val
        ### is dict
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            logo.debug(f"recursive call for keyname!: {keyname}")
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

    def set_cfg_runtime(self):
        # print()
        # print(self.cfg_runtime.cfg)
        cfgin = self.cfg_runtime.cfg
        for s in reversed(self.cfg_sources):
            mekt = helpers.deep_merge_dicts(cfgin, s.cfg)
            # print(mekt)
