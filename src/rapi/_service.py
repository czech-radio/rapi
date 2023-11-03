"""
This module contains services to store or retrieve data. Services are classes or functions.
which implements input/output operations, e.g., reading from disk, network, etc.
"""

import enum as _enum
import uuid
from typing import Iterator

import rapi._shared as _shared


class StationDataField(_enum.Enum):
    OPENMEDIA_ID: str = "openmedia_id"
    OPENMEDIA_STATION: str = "openmedia_station"
    CROAPP_SHORT_TITLE: str = "croapp_shortTitle"


class StationsProvider:
    """
    Retrieve informations about Czech Radio stations.

    NOTE: These are stored in package data directory.
    """

    _DATA_PATH: str = "data/stations.csv"
    # The file patch of CSV file relative to the package directory.

    def __init__(self) -> None:
        # Load and store station data from CSV file.
        self._storage = _shared.read_package_csv(self._DATA_PATH, __package__)

    @property
    def items(self) -> list:
        return [x for x in self._storage]

    @property
    def station_primary_keys(self) -> Iterator[str]:
        """
        Get a primary keys of stations if present.

        :returns: The list of primary keys of stations.
        """
        for item in self.items:
            primary_key = item.get("openmedia_id", None)
            if primary_key is not None:
                yield primary_key

    def find(self, primary_key: str, field_name: str) -> str | None:
        """FIXME

        :param primary_key: FIXME
        :param field_name: FIXME
        :returns: FIXME
        """
        result = None
        for row in self._storage:
            value = row.get("openmedia_id", None)
            if value == primary_key:
                result = row
        return result or row.get(field_name, None)

        # FIXME This should be in StationProvider service.

    def get_station_guid(self, station_id: int) -> str | uuid.UUID:
        """
        Get the station's UUID.

        :param station_id:
            The station serial identifier stored in `./data/stations.csv`.
        :returns: The station unique identifier or string.

        Example:
        >>> client = Client()
        >>> client._get_station_guid("11")
        4082f63f-30e8-375d-a326-b32cf7d86e02
        """
        fkey = self.find(station_id, "croapp_id")
        if fkey is None:
            raise ValueError(f"Could not find UUID for station with ID {station_id}")
        return fkey  # TODO We should prefer UUID.

    def get_station_code(self, station_id: str) -> str:
        """
        Get the station code i.e. id from croap_code column inside ./data/stations_ids.csv

        :param station_id: from openmedia_id column inside ./data/stations_ids.csv

        Example:
        >>> client = Client()
        >>> client._get_station_code("11")
        radiouzurnal
        """
        fkey = self._station_provider.find(station_id, "croapp_code")
        if fkey is None:
            raise ValueError(f"code not found for station_id: {station_id}")
        return fkey
