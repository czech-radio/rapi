import sys

from rapi import __version__
from rapi._client import Client
from rapi.config._config import Config
from rapi.helpers import _logger, helpers

# from rapi.helpers._logger import log_stderr as loge
from rapi.helpers._logger import log_stdout as logo
from rapi._station_ids import StationIDs


def commands(cfg: Config) -> None:
    try:
        commands_list(cfg)
        subcommand_list(cfg)
    except SystemExit as err:
        if err.code == 0:
            return
        else:
            raise err
    except BaseException as err:
        raise err


def commands_list(cfg: Config) -> None:
    cmd_test_logs(cfg)
    cmd_print_version(cfg)
    cmd_debug_cfg(cfg)
    return None


def subcommand_list(cfg: Config) -> None:
    subcommand = cfg.runtime_get(["subcommand"], None)
    if subcommand is None:
        return None
    logo.info(f"running command: {subcommand}")
    # NOTE: this can be simplified to dict or even to a list
    match subcommand:
        case "station_ids":
            subcmd_station_ids(cfg)
        case "station_guid":
            subcmd_station_guid(cfg)
        case "show_episodes":
            subcmd_show_episodes(cfg)
    return None

def subcmd_station_ids(cfg: Config):
    sid=StationIDs()
    print(sid.get_pkey_list())
    pass

def subcmd_show_episodes(cfg: Config):
    croapp = Client(cfg)
    id=cfg.runtime_get(['commands','show_episodes','id'])
    eps = croapp.get_show_episodes(str(id))
    helpers.ppl(list(eps))


def subcmd_station_guid(cfg: Config):
    croapp = Client(cfg)
    id=cfg.runtime_get(['commands','station_guid','id'])
    guid = croapp.get_station_guid(str(id))
    print(guid)


def cmd_print_version(cfg: Config) -> None:
    if cfg.runtime_get(["version"]):
        print(__version__)
        sys.exit(0)


def cmd_test_logs(cfg: Config) -> None:
    if cfg.runtime_get(["test", "logs"]):
        _logger.test_logs()
        sys.exit(0)


def cmd_debug_cfg(cfg: Config):
    if cfg.runtime_get(["debug", "cfg"]):
        data = cfg.cfg_runtime
        helpers.pp(data)
        sys.exit(0)
