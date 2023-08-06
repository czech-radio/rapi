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


# class Broadcast2:
# self.raw_data = self.request_data()
# self.Entities = self.entities_parse_fields()

# def entities_parse_fields(self) -> dict:
# stations = {}
# data = self.raw_data["data"]
# for k in data:
# attr = k["attributes"]
# stdat = model.station_data(
# id=k["id"],
# code=attr["code"],
# title=attr["title"],
# stitle=attr["shortTitle"],
# priority=attr["priority"],
# type=attr["stationType"],
# )
# stations[attr["code"]] = stdat
# return stations
