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
        self._storage: list[dict] = list(
            _shared.read_package_csv(self._DATA_PATH, __package__)
        )
        # FIXME This should be dict with key == primary_key not a list of dicts!

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

    def _find_station_field(self, station_id: str, field_name: str) -> str | None:
        """Find the value of attribute of the specified station.

        :param station_id: FIXME
        :param field_name: FIXME
        :returns: FIXME
        """
        found = None
        for item in self._storage:
            if str(station_id) == item.get("openmedia_id", None):
                found = item.get(field_name, None)
        return found

    def find_station_uuid(self, station_id: int) -> uuid.UUID | None:
        """Get the station's UUID.

        :param station_id: The station serial identifier.
        :returns: The station's UUID or `None`.

        Examples:
        >>> client = Client()
        >>> client._get_station_guid(11)
        UUID('4082f63f-30e8-375d-a326-b32cf7d86e02')
        """
        found = self._find_station_field(station_id, "croapp_id")
        if found is not None:
            found = uuid.UUID(found)
        return found

    def find_station_code(self, station_id: int) -> str | None:
        """Get the station's code (name).

        :param station_id: The station serial identifier.
        :returns: The station's code or `None`.

        Examples:
        >>> client = Client()
        >>> client._get_station_code(11)
        radiouzurnal
        """
        found = self._find_station_field(station_id, "croapp_code")
        return found
