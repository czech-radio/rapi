"""
FIXME
"""

from datetime import datetime
from typing import ClassVar, Iterator

import requests

from rapi import _helpers as helpers
from rapi import _station_ids
from rapi._logger import log_stdout as logo
from rapi._model import (
    Episode,
    Episode_schedule,
    Person,
    Show,
    Station,
    StationIDs,
)


class Client:
    """
    The REST client to fetch station, show, episodes and participants data.
    """

    api_url: ClassVar[str] = "https://api.mujrozhlas.cz"
    session_connection_timeout: ClassVar[int] = 15
    session_response_timeout: ClassVar[int] = 60
    limit_page_length: ClassVar[int] = 500
    # The maximum number of entitites per page.
    limit_page_str: ClassVar[str] = "page[limit]="
    # The part of url address to limit the maximum page length.

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": __name__})
        self._station_ids = _station_ids.StationIDs()

    def __del__(self):
        """
        Close the the session when all reference to it are deleted.

        TODO: Use context manager.

        """
        if self._session:
            self._session.close()

    def get_station_guid(self, station_id: str) -> str:
        """
        Get station guid: (globally unique identificator)

        :param station_id:
            The station serial identifier (ID) stored in `./data/stations_ids.csv`.
        :returns: The station unique identifier (UUID) as string.

        Example:
            >>> client = Client()
            >>> client.get_station_guid("11")
            4082f63f-30e8-375d-a326-b32cf7d86e02
        """
        sid = StationIDs()
        fkey = self._station_ids.get_fkey(station_id, sid.croapp_guid)
        if fkey is None:
            raise ValueError(f"guid not found for station_id: {station_id}")
        return fkey

    def get_station_code(self, station_id: str) -> str:
        """
        Get the station code i.e. id from croap_code column inside ./data/stations_ids.csv

        :param station_id: from openmedia_id column inside ./data/stations_ids.csv

        Examples:
            >>> client = Client()
            >>> client.get_station_code("11")
            radiouzurnal

        """
        sid = StationIDs()
        fkey = self._station_ids.get_fkey(station_id, sid.croapp_code)
        if fkey is None:
            raise ValueError(f"code not found for station_id: {station_id}")
        return fkey

    def _get_endpoint_link(
        self,
        endpoint: str,
        limit_page_length: int = 0,
    ) -> str:
        """
        Create API URL from the given parameters.

        Example:
            >>> client = Client()
            >>> client.get_endpoint_link("schedule", "10")
            https://api.mujrozhlas.cz/schedule?page[limit]=10

        """
        endpoint_url = "/".join((self.api_url, endpoint))
        if limit_page_length == 0:
            limit_page_length = self.limit_page_length
        if "?" in endpoint_url:
            opt_delim = "&"
        else:
            opt_delim = "?"
        endpoint_parts = [
            endpoint_url,
            opt_delim,
            self.limit_page_str,
            str(limit_page_length),
        ]
        endpoint_url = "".join(endpoint_parts)
        return endpoint_url

    def _get_endpoint_full_json(
        self, endpoint: str, limit_page_length: int = 0
    ) -> list[dict]:
        link = self._get_endpoint_link(
            endpoint,
            limit_page_length,
        )
        """
        get all json pages from endpoint
        """
        out: list = list()
        response_ttl = self.session_connection_timeout
        connect_ttl = self.session_response_timeout

        while link:
            request_msg = f"request url: {link}"
            logo.debug(request_msg)
            try:
                response = self._session.get(
                    link,
                    timeout=(
                        connect_ttl,
                        response_ttl,
                    ),
                )
                response.raise_for_status()
            except requests.exceptions.Timeout as ex:
                raise type(ex)(str(ex), request_msg) from None
            except Exception as exf:
                if response is not None:
                    raise type(exf)(
                        str(exf), request_msg, response.text
                    ) from None
                else:
                    raise type(exf)(str(exf), request_msg) from None
            jdata = response.json()
            data = jdata["data"]
            if not isinstance(data, list):
                data = [data]
            out = out + data
            link = jdata.get("links", {}).get("next")
        return out

    def _get_endpoint(
        self, endpoint: str = "", limit_page_length: int = 0
    ) -> list[dict]:
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        return data

    def get_station(
        self, station_id: str, limit_page_length: int = 0
    ) -> Station | None:
        """
        Get the station metadata.

        Example:
            >>> Client.get_station("11")
        """
        guid = self.get_station_guid(str(station_id))
        endpoint = "stations/" + guid
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        out = helpers.class_attrs_by_anotation_dict(
            data[0],
            Station,
        )
        if out is not None:
            assert isinstance(out, Station)
        return out

    def get_stations(self, limit_page_length: int = 0) -> Iterator[Station]:
        """
        Get all broadcast stations metadata.

        Example:
            >>> Client.get_stations()
        """
        data = self._get_endpoint_full_json("stations", limit_page_length)
        stations = helpers.class_attrs_by_anotation_list(data, Station)
        for station in stations:
            yield station

    def get_station_shows(
        self, station_id: str, limit_page_length: int = 0
    ) -> Iterator[Show]:
        """
        Get shows aired on specified station

        Examples:
            >>> Client.get_station_shows("11")
        """
        guid = self.get_station_guid(station_id)
        endpoint = "stations/" + guid + "/shows"
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        shows = helpers.class_attrs_by_anotation_list(data, Show)
        for show in shows:
            yield show

    def get_show(
        self, show_id: str, limit_page_length: int = 0
    ) -> Show | None:
        """
        Get metada for given show specified by show guid

        Example:
            >>> Client.get_show("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        endpoint = "shows/" + show_id
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        out = helpers.class_attrs_by_anotation_dict(data[0], Show)
        return out  # type: ignore

    def get_show_episodes(
        self, show_id: str, limit_page_length: int = 0
    ) -> Iterator[Episode]:
        """
        Get episodes of specified show by show UUID.

        >>> Clien.get_show_episodes("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        endpoint = "shows/" + show_id + "/episodes"
        endpoint = endpoint + "?sort=since"
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        episodes = helpers.class_attrs_by_anotation_list(
            data,
            Episode,
        )
        for episode in episodes:
            yield episode

    def show_episodes_filter(
        self,
        show_id: str,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        station_id: str | None = None,
        limit_page_length: int = 0,
    ) -> Iterator[Episode]:
        """
        Get show episodes and filter them by optonal fields.

        >>> Client.shows_episodes_filter(
            "9f36ee8f-73a7-3ed5-aafb-41210b7fb935",
            "2022-09-10",
            "2023-09-11",
            "11",
        )
        """
        tzinfo = helpers.current_timezone()
        eps = self.get_show_episodes(show_id, limit_page_length)

        # filter by date
        if date_from is None:
            date_from = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        if isinstance(date_from, str):
            date_from = helpers.parse_date_optional_fields(date_from)

        if date_to is None:
            date_to = datetime.now(tzinfo)
        if isinstance(date_to, str):
            date_to = helpers.parse_date_optional_fields(date_to)
        # NOTE: In the following lines mypy is disabled cause I don't
        # know how to make proper type hints.
        episodes = filter(
            lambda ep: (ep.since >= date_from) and (ep.till <= date_to),  # type: ignore
            eps,
        )
        for episode in episodes:
            yield episode  # type: ignore

    def get_show_episodes_schedule(
        self, show_id: str, limit_page_length: int = 0
    ) -> Iterator[Episode_schedule]:
        """
        Get all show episodes schedules.

        >>> Client.get_show_episodes_schedule("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        endpoint = "shows/" + show_id + "/schedule-episodes?sort=since"
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        episodes_schedules = helpers.class_attrs_by_anotation_list(
            data, Episode_schedule
        )
        for episode_schedule in episodes_schedules:
            yield episode_schedule

    def get_station_schedule_day_flat(
        self,
        day: str,
        station_id: str = "",
        limit_page_length: int = 0,
    ) -> Iterator[Episode_schedule]:
        """
        Get station schedule without relationships for given day by datetime string"

        >>> Client.get_station_schedule_day("2023-10-09")
        >>> Client.get_station_schedule_day("2023-10-09","11")
        """
        # NOTE:
        # https://rapidev.croapp.cz/schedule-day-flat?station=radiozurnal
        # not valid request when filtering by station
        # endpoint = "schedule-day?filter[station.id]=" + uuid # NOT WORKING
        endpoint = f"schedule-day-flat?filter[day]={day}"
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        epschedules = helpers.class_attrs_by_anotation_list(
            data, Episode_schedule
        )
        if station_id != "":
            station_uuid = self.get_station_guid(station_id)
            epschedules = list(
                filter(
                    lambda ep: (ep.station == station_uuid),  # type: ignore
                    epschedules,
                )
            )

        for episode_schedule in epschedules:
            yield episode_schedule

    def get_station_schedule_day(
        self,
        day: str,
        station_id: str = "",
        limit_page_length: int = 0,
    ) -> Iterator[Episode_schedule]:
        """
        Get station schedule without relationships for given day by datetime string"

        >>> Client.get_station_schedule_day("2023-10-09")
        >>> Client.get_station_schedule_day("2023-10-09","11")
        """

        endpoint = f"schedule-day?filter[day]={day}"
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        epschedules = helpers.class_attrs_by_anotation_list(
            data, Episode_schedule
        )
        if station_id != "":
            station_uuid = self.get_station_guid(station_id)
            epschedules = list(
                filter(
                    lambda ep: (ep.station == station_uuid),  # type: ignore
                    epschedules,
                )
            )
        for episode_schedule in epschedules:
            yield episode_schedule

    def get_schedule(
        self,
        show_id: str = "",
        station_id: str = "",
        since: str = "",
        till: str = "",
        limit_page_length: int = 0,
    ):
        """
        Get show schedule and filter it by optional parameters.

        >>> client = Client()
        >>> client.get_schedule("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        >>> client.get_schedule("","11")
        >>> Client.get_schedule("","","2021-09-01","2021-09-02")
        """
        endpoint = "schedule"
        urlfilters: list = list()
        if show_id != "":
            urlfilter = f"filter[show.id]={show_id}"
            urlfilters.append(urlfilter)
        if station_id != "":
            urlfilter = f"filter[stations.id]={station_id}"
            urlfilters.append(urlfilter)
        if since != "":
            urlfilter = f"filter[since][ge]={since}"
            urlfilters.append(urlfilter)
        if till != "":
            urlfilter = f"filter[till][le]={till}"
            urlfilters.append(urlfilter)
        link = endpoint + "?" + "&".join(urlfilters) + "&sort=since"
        data = self._get_endpoint_full_json(link, limit_page_length)
        epschedules = helpers.class_attrs_by_anotation_list(
            data, Episode_schedule
        )
        for episode_schedule in epschedules:
            yield episode_schedule

    def get_schedule_by_date(
        self,
        date_from: datetime | str,
        date_to: datetime | str,
        station_id: str = "",
        limit_page_length: int = 0,
    ) -> Iterator[Episode_schedule]:
        """
        Get show schedule and filter it by datetime given by datetime object or datetime string. The string is parsed as date. Optionaly filter by station_id.


        >>> Client.get_schedule_by_date(datefrom, dateto)
        >>> Client.get_schedule_by_date(datefrom, dateto, "11")
        """
        # e.g.: https://rapidev.croapp.cz/schedule?filter[title][eq]=Zpr%C3%A1vy
        if not isinstance(date_from, str):
            date_from = str(date_from)
        if not isinstance(date_from, str):
            date_to = str(date_to)
        endpoint = "schedule"
        from_filter = f"filter[since][ge]={date_from}"
        to_filter = f"filter[till][le]={date_to}"
        link = f"{endpoint}?{from_filter}&{to_filter}"
        data = self._get_endpoint_full_json(
            link,
            limit_page_length,
        )
        epschedules = helpers.class_attrs_by_anotation_list(
            data, Episode_schedule
        )
        # NOTE: This station filter does not work!
        # endpoint=f"{endpoint}&filter[station]={station_uuid}"
        if station_id != "":
            station_uuid = self.get_station_guid(station_id)
            epschedules = list(
                filter(
                    lambda ep: (ep.station == station_uuid),  # type: ignore
                    epschedules,
                )
            )
        for episode_schedule in epschedules:
            yield episode_schedule

    def get_person(
        self, person_id: str, limit_page_length: int = 0
    ) -> Person | None:
        """
        Get person metadata by person guid.

        >>> Client.get_person("1cb35d9d-fb24-37ee-8993-9f74e57ab2c7")
        """
        endpoint = "persons/" + person_id
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        out = helpers.class_attrs_by_anotation_dict(data[0], Person)
        if out is not None:
            assert isinstance(out, Person)
        return out

    def get_show_participants_with_roles(
        self,
        show_id: str,
        limit_page_length: int = 0,
    ) -> Iterator[Person]:
        """
        Get show participants and their roles in show

        >>> Client.get_show_participants_with_roles("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        # NOTE: relationships.participants.data:
        # [{'type': 'person', 'id': '1cb35d9d-fb24-37ee-8993-9f74e57ab2c7', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': '7b9d1544-8aab-3730-8f0a-4d0b463322be', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'c5b35399-08c6-3057-8145-c6aaaac76d4d', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'fcb6babc-e5f6-3b30-b126-583885584454', 'meta': {'role': 'moderator'}}]

        endpoint = "shows/" + show_id
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        json_base_path = ["relationships", "participants", "data"]
        persons_meta = helpers.dict_get_path(data[0], [*json_base_path])
        for p in persons_meta:
            puuid = p["id"]
            prole = p["meta"]["role"]
            person = self.get_person(puuid)
            if person is not None:
                person.role = prole
                yield person

    def get_show_moderators(
        self,
        show_id: str,
        limit_page_length: int = 0,
    ) -> Iterator[Person]:
        """
        Get show participants and filter them by role "moderator"

        >>> client.get_show_moderators("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        persons = self.get_show_participants_with_roles(
            show_id, limit_page_length
        )
        moderators = list(
            filter(
                lambda person: (person.role == "moderator"),  # type: ignore
                persons,
            )
        )
        for moderator in moderators:
            yield moderator

    def get_show_participants(
        self, show_id: str, limit_page_length: int = 0
    ) -> Iterator[Person]:
        """
        Get show participants regardless of their roles. Alternative to get_show_participants_with_roles

        >>> client.get_show_participants("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        endpoint = "shows/" + show_id + "/participants"
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        persons = helpers.class_attrs_by_anotation_list(data, Person)
        for person in persons:
            yield person

    def get_show_episodes_last_repetition(
        self, show_id: str, limit_page_length: int = 0
    ) -> Iterator[Episode_schedule]:
        """
        Get show episodes last repetitions.

        >>> client.get_show_episode_last_repetition("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        # NOTE: Acording to Jan Hejzl (see features discussion: file:./docs/build/features_discusion.html) the date of premiere is automaticaly rewritten with the date of episode repetition
        endpoint = "shows/" + show_id + "/schedule-episodes"  # Returns empty
        # endpoint="serials/"
        # endpoint="schedule/"+id
        # endpoint="program/" # very slow
        data = self._get_endpoint_full_json(endpoint, limit_page_length)
        epschedules = helpers.class_attrs_by_anotation_list(
            data, Episode_schedule
        )

        for episode_schedule in epschedules:
            yield episode_schedule

    def get_show_episodes_premieres(self) -> Iterator[Episode]:
        return NotImplemented

    def get_show_episodes_repetitions(self) -> Iterator[Episode]:
        return NotImplemented
