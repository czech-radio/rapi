# import configparser
import os

__version__ = "0.0.1"


def load_from_cfg(config, section, key):
    env_key = f"{section.upper()}_{key.upper()}"
    return os.environ.get(env_key, config.get(section, key))


def get_env_var_or_default(env_var, default):
    value = os.environ.get(env_var)
    return value if value else default

    # username = load_config_from_env(config, 'Credentials', 'username')


### api urls
# apiurl_mock = "https://mockservice.croapp.cz/mock"
# apiurl_doc = "https://rapidoc.croapp.cz"
# apiurl_api = "https://rapidev.croapp.cz"
