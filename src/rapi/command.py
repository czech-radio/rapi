import argparse
import json
import logging
import os
import sys
import time

from rapi import config, swagger
from rapi.broadcast import Broadcast
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


def set_loglevel(level: int = 0):
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
    data_formated = json.dumps(data, indent=4)
    print(data_formated)
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


def command2(args: argparse.Namespace) -> None:
    ### version
    if args.version:
        print(config.__version__)
        return
    ### logs settings
    if args.verbose == 0:
        loglevel = logging.WARN
    if args.verbose == 1:
        loglevel = logging.INFO
    if args.verbose == 2:
        loglevel = logging.DEBUG
    logo.setLevel(loglevel)
    loge.setLevel(loglevel)
    if args.test_logs:
        logo.debug("this is debug_level message")
        logo.info("this is info_level message")
        logo.warning("this is warning_level message")
        loge.error("this is error_level message")
        return

    if args.cfg_file is None:
        pass
        # cfgfile = config.get_env_var("RAPI_CFG_FILE", ".config.ini")

    ### dummy parser
    if args.dummy:
        # print(cfgfile)
        return

    ### swagger parser
    if args.swagger_download:
        logo.info(f"downloading file: {args.swagger_download}")
        swagger.swagger_download(args.swagger_download)
        return
    if args.swagger_parse:
        logo.info(f"parsing swagger file: {args.swagger_parse}")
        # swagger.swagger_parse(args.swagger_parse)
        return

    ### broacast class
    if args.broadcast:
        logo.info(f"requesting stations: {args.broadcast}")
        st = Broadcast(args)
        st.station_ids_parse()
        # for i in st.Entities:
        # print(st.Entities[i])
        return
