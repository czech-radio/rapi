
import os
from typing import Optional, Sequence, Union

from rapi import helpers

def env_vars_cfg_union(cfg_in: dict, section: str = "") -> dict:
    cfg = cfg_in
    for k in cfg:
        ### is atom -> get value
        if isinstance(cfg[k], (str, int, bool)):
            keyname = helpers.str_join_no_empty([section, k])
            env_val = env_var_get(keyname)
            if env_val is not None:
                logo.debug(f"taking var from env: {k}, value: {env_val}")
                cfg[k] = env_val
        ### is dict -> recurse
        elif isinstance(cfg[k], dict):
            keyname = helpers.str_join_no_empty([section, k])
            logo.debug(f"recursive call for keyname!: {keyname}")
            scfg = cfg[k]
            modscfg = env_vars_cfg_union(scfg, keyname)
            cfg[k] = modscfg
        ### not implemented for other types
        else:
            raise TypeError(f"cannot parse type: {type(cfg[k])}")
    return cfg
