import argparse
import json
import logging
import os
import pkgutil
from typing import Any, Union

import requests

from rapi import config, helpers, model
from rapi.helpers import analyze as an
from rapi.helpers import ptype as ant
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class StationIDs:
    def __init__(self, cfg: config.CFG) -> None:
        self.Cfg = cfg
        self.DBpath = self.Cfg.runtime_get(["broadcast", "station_ids", "csv"])
        self.DB_global_id = self.Cfg.runtime_get(
            ["broadcast", "station_ids", "pkey"]
        )
        self.DB = self.db_csv_init(self.DBpath)

    def db_csv_init(self, fspath: str = "default") -> list:
        if fspath == "default":
            pkgpath = "data/stations_ids.csv"
            fspath = ""
        csvr = helpers.read_csv_fspath_or_package_to_ram(
            fspath,
            pkgpath,
        )
        if csvr is None:
            loge.error("cannot parse station_ids_csv")
            raise ValueError
        return helpers.csv_valid_rows(csvr)

    def get_pkey_list(self) -> list:
        pkey = self.DB_global_id
        out: list = []
        for row in self.DB:
            val = row.get(pkey, None)
            if out is not None:
                out.append(val)
        return out

    def get_table(self) -> list:
        out = []
        for row in self.DB:
            out.append(row)
        return out

    def get_row_by_pkey(self, pkey: str) -> Union[dict, None]:
        pkey_name = self.DB_global_id
        for row in self.DB:
            val = row.get(pkey_name, None)
            if val == str(pkey):
                return row
        return None

    def get_fkey(self, pkey: str, fkey_name: str) -> Union[str, None]:
        row = self.get_row_by_pkey(pkey)
        if row is not None:
            return row.get(fkey_name, None)
        return None
