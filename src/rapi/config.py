import configparser
import logging
import os
from typing import Union, Optional

from . import helpers

logt = logging.getLogger("log_test")
logt.setLevel(logging.INFO)

__version__ = "0.0.1"


def config_parse(cfg_file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(cfg_file)
    return config


# def var_from_env(section: str, key: str) -> str:
# var = helpers.str_join_no_empty(section, key)
# return os.environ.get(var, default="")
# env_key = f"{section.upper()}_{key.upper()}"


def var_from_env(
        section: str, key: str,
        default: Optional[str] = None
        ) -> Union[str, None]:
    sec_key = helpers.str_join_no_empty(section, key)
    return os.environ.get(sec_key, default)


def var_from_cfg(
        section: str, key: str,
        config: configparser.ConfigParser
        ) -> Union[str,None]:
    if section == "":
        return None
    return os.environ.get(key, config.get(section, key))

### from:
#### 1. argparser
#### 2. envparser
#### 3. configparser.ConfigParser
#### 4. default value
#### 5. Empty or panicfail

def get_var(
        section: str, key: str,
        config: configparser.ConfigParser
        ) -> Union[str,None]:
    ### ENV 
    val = var_from_env(section, key)
    ### CFG
    if val is None or len(val) == 0:
        val=var_from_cfg(section,key,config)
    ### NONE
    if val is None:
        ValueError(f"mandatory variable not defined: {val}")
    return val


# def get_cfg_vars(cfg_file: str) -> dict:
# config = configparser.ConfigParser()
# config.read(cfg_file)
# for var, section, default in cfg_vars:
# print(var)
# print(section, default)
# return {}
