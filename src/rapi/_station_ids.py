"""
Module contains class which queries table of staion IDs used across
various databases and translate between them.
"""

from typing import Union
from pathlib import Path

from rapi import _helpers as helpers


class StationIDs:
    """
    Class serving to query table. Table contains row for each CRo station.
    One row contains various IDs for one station. `./data/station_ids.csv`
    """

    primary_key_name = "openmedia_id"
    primary_keys_path = "/data/stations_ids.csv"

    def __init__(self) -> None:
        self._storage = self._populate()

    def _populate(self) -> list:
        """
        Load primary keys of stations from CSV file.
        """
        primary_keys = helpers.read_embedded_csv(self.primary_keys_path, __package__)
        if primary_keys is None:
            raise ValueError("Could not load primary keys of stations from CSV file")
        result = helpers.csv_valid_rows(primary_keys)
        return result

    def get_primary_keys(self) -> list:
        """
        Get a primary keys of stations.

        :returns: The list of primary keys.
        """
        out: list = []
        for row in self._storage:
            val = row.get(self.primary_key_name, None)
            if out is not None:
                out.append(val)
        return out

    def get_row_by_primary_key(self, primary_key: str) -> Union[dict, None]:
        """
        FIXME
        """
        for row in self._storage:
            value = row.get(self.primary_key_name, None)
            if value == str(primary_key):
                return row
        return None

    def get_fkey(self, pkey: str, fkey_name: str) -> Union[str, None]:
        """
        FIXME Use better arguments name

        :param pkey: The field value of global primary key used by user.
        :param fkey: The field name of primary key used in particular database.
        """
        row = self.get_row_by_primary_key(pkey)
        if row is not None:
            return row.get(fkey_name, None)
        return None
