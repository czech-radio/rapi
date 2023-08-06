import argparse
import json
import logging
import os
import pkgutil
from typing import Any, Union

import requests

from rapi import config, helpers, model, station_ids
from rapi.helpers import analyze as an
from rapi.helpers import analyze_type as ant
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class Broadcast:
    def __init__(self, cfg: config.CFG) -> None:
        self.Cfg = cfg
        self.StationIDs = station_ids.StationIDs(cfg)


# class Broadcast2:
# def __init__(self, pars: argparse.Namespace) -> None:
# self.raw_data = self.request_data()
# self.Entities = self.entities_parse_fields()

# def request_data(self) -> dict:
# url = self.url_api + "/stations-all"
# logo.info("requesitng url: {url}")
# response = requests.get(url)
# if response.status_code == 200:
# json_data = json.loads(response.text)
# return json_data
# else:
# loge.error("cannot get data from: {url}")
# return {}

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

# def station_ids_parse(self) -> None:
# path = os.path.abspath(self.station_ids_file)
# logo.info("reading file {path}")
# with open(path, "r") as f:
# reader = csv.reader(f)
# for row in reader:
# print(row)

# def get_station_by_code(self, station_code: str) -> model.station_data:
# return self.Entities[station_code]
