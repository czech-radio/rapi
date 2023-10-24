"""
FIXME
"""

from typing import Union

from rapi import _helpers as helpers
from rapi._logger import log_stdout as loge


class StationIDs:
    station_ids_pkey = "openmedia_id"
    station_ids_embeded_path = "/data/stations_ids.csv"

    def __init__(self) -> None:
        self.DB = self.db_csv_init()

    def db_csv_init(self) -> list:
        """
        parse default station ids table
        """
        csvr = helpers.read_embeded_csv_to_ram(
            self.station_ids_embeded_path, __package__
        )
        if csvr is None:
            loge.error("cannot parse station_ids_csv")
            raise ValueError
        return helpers.csv_valid_rows(csvr)

    def get_pkey_list(self) -> list:
        out: list = []
        for row in self.DB:
            val = row.get(self.station_ids_pkey, None)
            if out is not None:
                out.append(val)
        return out

    def get_table(self) -> list:
        """get whole staion ids table"""
        out = []
        for row in self.DB:
            out.append(row)
        return out

    def get_row_by_pkey(self, pkey: str) -> Union[dict, None]:
        pkey_name = self.station_ids_pkey
        for row in self.DB:
            val = row.get(pkey_name, None)
            if val == str(pkey):
                return row
        return None

    def get_fkey(self, pkey: str, fkey_name: str) -> Union[str, None]:
        """
        pkey: field value of global primary key used by user
        fkey: fieldname of primary key used in particular database
        """
        row = self.get_row_by_pkey(pkey)
        if row is not None:
            return row.get(fkey_name, None)
        return None
