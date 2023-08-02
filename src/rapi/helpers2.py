import os
from typing import Optional, Sequence, Union

from rapi import helpers


def env_vars_cfg_union(cfg_in: dict, section: str = "") -> dict:
    cfg = cfg_in
    for k in cfg:
        ### is atom -> get value
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            env_val = helpers.env_var_get(keyname)
            if env_val is not None:
                # logo.debug(f"taking var from env: {k}, value: {env_val}")
                cfg[k] = env_val
        ### is dict -> recurse
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            # logo.debug(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = env_vars_cfg_union(scfg, keyname)
            cfg[k] = modscfg
        ### not implemented for other types
        else:
            raise TypeError(f"cannot parse type: {type(cfg[k])}")
    return cfg


def env_vars_cfg_paths2(
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
            ps = env_vars_cfg_paths2(val, ps, pi, cn)
    return ps


def env_vars_dict_intersec2(dcfg: dict) -> dict:
    paths = env_vars_cfg_paths2(dcfg)
    dictr: dict = {}
    for p in paths:
        envval = helpers.env_var_get("_".join(p))
        if envval is not None:
            helpers.dict_create_path(dictr, p, envval)
    return dictr


### config from commandline params (flags) union with default config
def params_vars_cfg_union(cfg_in: dict, pars: dict, section: str = ""):
    cfg = cfg_in
    for k in cfg:
        ### simple string
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            val = pars.get(keyname, None)
            if val is not None:
                # logo.debug(f"taking var from par: {k}, value: {val}")
                cfg[k] = val
        ### is dict
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            # logo.debug(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = params_vars_cfg_union(scfg, pars, keyname)
            cfg[k] = modscfg
        ### not implemented for other types
        else:
            raise TypeError(f"cannot parse type: {type(cfg[k])}")
    return cfg
