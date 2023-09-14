import logging
import sys

from rapi import __version__, _client, _helpers
from rapi._config import Config
from rapi._logger import log_stderr as loge
from rapi._logger import log_stdout as logo


def commands(cfg: Config) -> None:
    getvar = cfg.runtime_get

    ### set log level
    vlevel = getvar(["verbose"])
    set_loglevel(vlevel)

    ### test logs
    run = getvar(["test", "logs"])
    test_logs(run)

    ### print version
    print_version(cfg)

    ### debug cfg
    run = getvar(["debug", "cfg"])
    debug_cfg(run, cfg)

    ### subcommands
    subc = getvar(["subcommand"], None)
    if subc is None:
        return
    else:
        logo.info(f"running command: {subc}")

    if "station" == subc:
        croapp = _client.Client(cfg)
        # print(vars(ap))
        # guid = croapp.get_station_guid("11")
        # print(guid)

    if "show" == subc:
        pass


def print_version(cfg: Config) -> None:
    if cfg.runtime_get(["version"]):
        print(__version__)
        sys.exit(0)


def set_loglevel(level: int = 0):
    # NOTE: maybe the loglevel maybe set directly
    if level == 0:
        loglevel = logging.WARN
    if level == 1:
        loglevel = logging.INFO
    if level == 2:
        loglevel = logging.DEBUG
    logo.setLevel(loglevel)
    loge.setLevel(loglevel)


def test_logs(run: bool):
    if run is False:
        return
    logo.debug("this is debug_level message")
    logo.info("this is info_level message")
    logo.warning("this is warning_level message")
    loge.error("this is error_level message")
    sys.exit(0)


def debug_cfg(run: bool, cfg: Config):
    if run is False:
        return
    data = cfg.cfg_runtime
    _helpers.pp(data)
    sys.exit(0)
