import argparse
import json
import logging
import os
import sys
import time
from typing import Type

from rapi import api_croapp, config, helpers, swagger
from rapi.broadcast import Broadcast
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


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


def debug_cfg(run: bool, cfg: config.CFG):
    if run is False:
        return
    data = cfg.cfg_runtime
    helpers.pp(data)
    sys.exit(0)


def command(Cfg: config.CFG) -> None:
    getv = Cfg.runtime_get
    ###
    vlevel = getv(["verbose"])
    set_loglevel(vlevel)
    ###
    run = getv(["test", "logs"])
    test_logs(run)
    ###
    run = getv(["debug", "cfg"])
    debug_cfg(run, Cfg)

    ### broadcast
    if getv(["broadcast"]):
        bc = Broadcast(Cfg)

    ### croapp
    cmd = getv(["apis", "croapp", "stations"])
    if cmd:
        pass

        # print(cmd)
        # croapp = api_croapp.API(Cfg)
        # st=croapp.get_station("11")
        # print(st)
        # logo.info(f"requesting stations: {args.broadcast}")
        # bcdata=Cfg.runtime_get(["apis","croapp"])
        # helpers.pprint(bcdata)


# def filter_cmd(cmd: str)->Type:
