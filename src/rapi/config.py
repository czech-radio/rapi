import configparser
import logging
import os

logt = logging.getLogger("log_test")
logt.setLevel(logging.INFO)

__version__ = "0.0.1"

cfg_vars = [
    ("apiurl_mock", "api_urls", ""),
    ("apiurl_doc", "api_urls", ""),
]


def is_file_readable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def load_from_cfg(config, section, key) -> str:
    env_key = f"{section.upper()}_{key.upper()}"
    return os.environ.get(env_key, config.get(section, key))


# def get_env_var(env_var: str, cfg_file: str, default: str) -> str:
#     ### 1. from env if exists and no-empty
#     value = os.environ.get(env_var)
#     ### 2. from cfg file if exists
#     if value is None:
#         if is_file_readable(cfg_file):
#             value = load_from_cfg(cfg_file, env_var)
#     ### 3. defalt value or fail
#     if value is None:
#         if default == "fail":
#             raise ValueError(f"mandatory variable not defined {env_var}")
#     return value


def get_cfg_vars(cfg_file: str) -> dict:
    config = configparser.ConfigParser()
    config.read(cfg_file)
    for var, section, default in cfg_vars:
        print(var, section, default)
    return {}
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
