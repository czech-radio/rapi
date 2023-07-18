import requests, json
import os
import csv
import logging
from .logger import log_stdout as logo
from .logger import log_stdout as loge
from . import model

class Broadcast:
    def __init__(self, pars):
        self.params = pars
        self.url_mock="https://mockservice.croapp.cz/mock"
        self.url_apidoc="https://rapidoc.croapp.cz"
        self.url_api="https://rapidev.croapp.cz"
        self.station_ids_file="data/stations_ids_table.csv"
        self.raw_data=self.request_data()
        self.Entities=self.entities_parse_fields()
        logo.info("broadcast class initialized")
    def params_debug(self):
        print(json.dumps(self.params.__dict__))
    def request_data(self):
        url=self.url_api+'/stations-all'
        logo.info("requesitng url: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            loge.error("cannot get data from: {url}")
            return None
    def entities_parse_fields(self):
        stations={}
        data=self.raw_data["data"]
        for k in data:
            attr=k["attributes"] 
            stdat=model.station_data(
                    id=k["id"],
                    code=attr["code"],
                    title=attr["title"],
                    stitle=attr["shortTitle"],
                    priority=attr["priority"],
                    type=attr["stationType"],
                    )
            stations[attr["code"]]=stdat
        return stations
    def station_ids_parse(self):
        path = os.path.abspath(self.station_ids_file)
        logo.info("reading file {path}")
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
    def get_station_by_code(self,station_code: str):
        return self.Entities[station_code]
