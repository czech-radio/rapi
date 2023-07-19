import argparse
import logging
import os
import sys
import time

from .__init__ import __version__
from .broadcast import Broadcast
from .logger import log_stdout as loge
from .logger import log_stdout as logo


def command(args: argparse.Namespace):
    ### version
    if args.version:
        print(__version__)
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
    ### swagger parser
    if args.swagger_download:
        logo.info(f"downloading file: {args.swagger_download}")
        swagger.SwaggerDownload(args.swagger_download)
        return
    if args.swagger_parse:
        logo.info(f"parsing swagger file: {args.swagger_parse}")
        swagger.swagger_parse(args.swagger_parse)
        return
    ### broacast class
    if args.broadcast:
        logo.info(f"requesting stations: {args.broadcast}")
        st = Broadcast(args)
        st.station_ids_parse()
        # for i in st.Entities:
        # print(st.Entities[i])
        return
