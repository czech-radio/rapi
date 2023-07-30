import configparser
import logging
import os
import pkgutil
from typing import Optional, Union

from rapi import helpers, params

logt = logging.getLogger("log_test")
logt.setLevel(logging.INFO)

__version__ = "0.0.1"



def config_parse(cfg_file: str) -> configparser.ConfigParser:
    cfg_parser = configparser.ConfigParser()
    cfg_parser.read(cfg_file)
    return cfg_parser


def config_default_parse() -> configparser.ConfigParser:
    cfg_parser = configparser.ConfigParser()
    dats = pkgutil.get_data(__name__, "data/defaults.ini")
    assert dats is not None
    dats_txt = dats.decode("utf-8")
    cfg_parser.read_string(dats_txt)
    return cfg_parser


def var_from_env(
    section: str, key: str, default: Optional[str] = None
) -> Union[str, None]:
    sec_key = helpers.str_join_no_empty(section, key)
    return os.environ.get(sec_key, default)


def var_from_cfg(
    section: str, key: str, config: configparser.ConfigParser
) -> Union[str, None]:
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
    section: str, key: str, config: configparser.ConfigParser
) -> Union[str, None]:
    ### ENV
    val = var_from_env(section, key)
    ### CFG
    if val is None or len(val) == 0:
        val = var_from_cfg(section, key, config)
    ### NONE
    if val is None:
        ValueError(f"mandatory variable not defined: {val}")
    return val


