import argparse
import json
import logging
import os
import pkgutil
from typing import Any, Union

import requests

from rapi import config, helpers, model, station_ids
from rapi.helpers import analyze as an
from rapi.helpers import ptype as ant
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class Broadcast:
    def __init__(self, cfg: config.CFG) -> None:
        self.Cfg = cfg
        self.StationIDs = station_ids.StationIDs(cfg)
