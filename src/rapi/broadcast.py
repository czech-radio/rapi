import argparse
import csv
import json
import logging
import os

import requests

from rapi import config, model
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class Broadcast:
    def __init__(self, pars: argparse.Namespace) -> None:
        self.params = pars
        self.url_mock = "https://mockservice.croapp.cz/mock"
        self.url_apidoc = "https://rapidoc.croapp.cz"
        self.url_api = "https://rapidev.croapp.cz"
        self.station_ids_file = "data/stations_ids_table.csv"
        self.raw_data = self.request_data()
        self.Entities = self.entities_parse_fields()
        logo.info("broadcast class initialized")

    def params_debug(self) -> None:
        print(json.dumps(self.params.__dict__))

    def request_data(self) -> dict:
        url = self.url_api + "/stations-all"
        logo.info("requesitng url: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            loge.error("cannot get data from: {url}")
            return {}

    def entities_parse_fields(self) -> dict:
        stations = {}
        data = self.raw_data["data"]
        for k in data:
            attr = k["attributes"]
            stdat = model.station_data(
                id=k["id"],
                code=attr["code"],
                title=attr["title"],
                stitle=attr["shortTitle"],
                priority=attr["priority"],
                type=attr["stationType"],
            )
            stations[attr["code"]] = stdat
        return stations

    def station_ids_parse(self) -> None:
        path = os.path.abspath(self.station_ids_file)
        logo.info("reading file {path}")
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    def get_station_by_code(self, station_code: str) -> model.station_data:
        return self.Entities[station_code]
