import configparser
import logging
import os

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


# def var_from_env(key: str, default: str="") -> str:
def var_from_env(
        section: str, key: str,
        default: str | None = None
        ) -> str:
    sec_key = helpers.str_join_no_empty(section, key)
    return os.environ.get(sec_key, default)


def var_from_cfg(section: str, key: str, config: configparser.ConfigParser) -> str:
    return os.environ.get(key, config.get(section, key))


def get_var(section: str, key: str, config: configparser.ConfigParser) -> str:
    # key="mekt"
    value = var_from_env(section, key)
    return value
    # if len(kak) == 0:
    # print("kek")
    # return value
    # if value


# def get_cfg_vars(cfg_file: str) -> dict:
# config = configparser.ConfigParser()
# config.read(cfg_file)
# for var, section, default in cfg_vars:
# print(var)
# print(section, default)
# return {}


# def get_env_var(env_var: str, cfg_file: str, default: str) -> str:
#     ### 1. from env if exists and no-empty
#     value = os.environ.get(env_var)
#     ### 2. from cfg file if exists
#     if value is None:
#         if helpers.is_file_readable(cfg_file):
#             value = load_from_cfg(cfg_file, env_var)
#     ### 3. defalt value or fail
#     if value is None:
#         if default == "fail":
#             raise ValueError(f"mandatory variable not defined {env_var}")
#     return value


# load_from_cfg(config)


# def get_env_var(env_var, default):
# value = os.environ.get(env_var)
# return value if value else default

# username = load_config_from_env(config, 'Credentials', 'username')

# class Env
# def __init_(self):
### api urls
# apiurl_mock = "https://mockservice.croapp.cz/mock"
# apiurl_doc = "https://rapidoc.croapp.cz"
# apiurl_api = "https://rapidev.croapp.cz"
