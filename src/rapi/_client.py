"""
This module contains REST client class.
"""

from datetime import datetime
from typing import ClassVar, Iterator

import requests

import rapi._domain as _domain
import rapi._service as _service
import rapi._shared as _shared


class Client:
    """
    The REST client to fetch station, show, episodes and participants data.
    """

    __url__: ClassVar[str] = "https://api.mujrozhlas.cz"
    session_connection_timeout: ClassVar[int] = 15
    session_response_timeout: ClassVar[int] = 60
    limit: ClassVar[int] = 500
    # The maximum number of entitites per page.
    limit_page_str: ClassVar[str] = "page[limit]="
    # The part of url address to limit the maximum page length.

    def __init__(self) -> None:
        self._session: requests.Session = requests.Session()
        self._session.headers.update({"User-Agent": __name__})
        self._station_provider = (
            _service.StationsProvider()
        )  # FIXME Should be injected in consyructor!

    def __enter__(self):
        """Context manager related method."""
        return self

    def __exit__(self) -> None:
        """Context manager related method."""
        if self._session is not None:
            self._session.close()

    def _build_route(self, endpoint: str, limit: int = 0) -> list[dict]:
        """
        Get all json pages from endpoint.

        :param endpoint: specific part or url which targets specific resource
        returns: json string

        Example:
        >>> client = Client()
        >>> client._get_endpoint_link("stations")
        """
        endpoint_url = "/".join((self.__url__, endpoint))
        if limit == 0:
            limit = self.limit
        if "?" in endpoint_url:
            opt_delim = "&"
        else:
            opt_delim = "?"
        endpoint_parts = [
            endpoint_url,
            opt_delim,
            self.limit_page_str,
            str(limit),
        ]
        link = "".join(endpoint_parts)
        out = []
        response_ttl = self.session_connection_timeout
        connect_ttl = self.session_response_timeout

        while link:
            request_msg = f"request url: {link}"
            try:
                response = self._session.get(link, timeout=(connect_ttl, response_ttl))
                response.raise_for_status()
            except requests.exceptions.Timeout as ex:
                raise type(ex)(str(ex), request_msg) from None
            except Exception as exf:
                if response is not None:
                    raise type(exf)(str(exf), request_msg, response.text) from None
                else:
                    raise type(exf)(str(exf), request_msg) from None
            jdata = response.json()
            data = jdata["data"]
            if not isinstance(data, list):
                data = [data]
            out = out + data
            link = jdata.get("links", {}).get("next")
        return out

    def get_station(self, station_id: int | str) -> _domain.Station | None:
        """
        Get a specified station.

        Examples:
        >>> client = Client()
        >>> client.get_station(11)
        """
        guid = self._station_provider.get_station_guid(str(station_id))
        data = self._build_route(f"stations/{guid}", 0)
        result = _shared.class_attrs_by_anotation_dict(data[0], _domain.Station)
        return result

    def get_stations(self, limit: int = 100) -> Iterator[_domain.Station]:
        """
        Get available stations.

        Examples:
        >>> client = Client()
        >>> result = client.get_stations(limit=10)
        """
        data = self._build_route("stations", limit)
        result = _shared.class_attrs_by_anotation_list(data, _domain.Station)
        for item in result:
            yield result

    def get_show(self, show_id: str) -> _domain.Show | None:
        """
        Get a specified show.

        Examples:
        >>> client = Client()
        >>> client.get_show(uuid.UUID("9f36ee8f-73a7-3ed5-aafb-41210b7fb935"))
        """
        data = self._build_route(f"shows/{show_id}", limit=0)
        result = _shared.class_attrs_by_anotation_dict(data[0], _domain.Show)
        return result

    def get_shows(self, station_id: int, limit: int = 100) -> Iterator[_domain.Show]:
        """
        Get shows for specified station.

        Examples:
        >>> client = Client()
        >>> client.get_station_shows(11)
        """
        guid = self._station_provider.get_station_guid(str(station_id))
        data = self._build_route(f"stations/{guid}/shows", limit)
        result = _shared.class_attrs_by_anotation_list(data, _domain.Show)
        for item in result:
            yield item

    def get_show_episodes(
        self, show_id: str, limit: int = 100
    ) -> Iterator[_domain.Episode]:
        """
        Get episodes of specified show by show UUID.

        >>> client = Client()
        >>> client.get_show_episodes("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        data = self._build_route(f"shows/{show_id}/episodes?sort=since", limit)
        episodes = _shared.class_attrs_by_anotation_list(data, _domain.Episode)
        for episode in episodes:
            yield episode

    def get_show_episodes_filter(
        self,
        show_id: str,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        station_id: str | None = None,
        limit: int = 0,
    ) -> Iterator[_domain.Episode]:
        """
        Get show episodes and filtered by optional fields.

        >>> Client.shows_episodes_filter(
            "9f36ee8f-73a7-3ed5-aafb-41210b7fb935",
            "2022-09-10",
            "2023-09-11",
            "11",
        )
        """
        tzinfo = _shared.current_timezone()
        eps = self.get_show_episodes(show_id, limit)

        if date_from is None:
            date_from = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        if isinstance(date_from, str):
            date_from = _shared.parse_date_optional_fields(date_from)
        if date_to is None:
            date_to = datetime.now(tzinfo)
        if isinstance(date_to, str):
            date_to = _shared.parse_date_optional_fields(date_to)
        episodes = filter(
            lambda ep: (ep.since >= date_from) and (ep.till <= date_to),  # type: ignore
            eps,
        )
        for episode in episodes:
            yield episode  # type: ignore

    def get_show_episodes_schedule(
        self, show_id: str, limit: int = 0
    ) -> Iterator[_domain.EpisodeSchedule]:
        """
        Get all show episodes schedules.

        >>> Client.get_show_episodes_schedule("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        data = self._build_route(f"shows/{show_id}/schedule-episodes?sort=since", limit)
        result = _shared.class_attrs_by_anotation_list(data, _domain.EpisodeSchedule)
        for item in result:
            yield item

    def get_station_schedule_day_flat(
        self,
        day: str,
        station_id: str = "",
        limit: int = 0,
    ) -> Iterator[_domain.EpisodeSchedule]:
        """
        Get station schedule without relationships.

        >>> client = Client()
        >>> client.get_station_schedule_day("2023-10-09")
        >>> client.get_station_schedule_day("2023-10-09", "11")
        """
        path = f"schedule-day-flat?filter[day]={day}"
        data = self._build_route(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _domain.EpisodeSchedule
        )
        station_uuid = self._station_provider.get_station_guid(station_id)
        result = filter(lambda ep: (ep.station == station_uuid), epschedules)
        for episode in result:
            yield episode

    def get_station_schedule_day(
        self,
        day: str,
        station_id: str = "",
        limit: int = 0,
    ) -> Iterator[_domain.EpisodeSchedule]:
        """
        Get station's schedule without relationships for given day."

        >>> client = Client()
        >>> client.get_station_schedule_day("2023-10-09")
        >>> client.get_station_schedule_day("2023-10-09", "11")
        """

        path = f"schedule-day?filter[day]={day}"
        data = self._build_route(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _domain.EpisodeSchedule
        )
        if station_id != "":
            station_uuid = self._station_provider.get_station_guid(station_id)
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
        since: datetime | str,
        till: datetime | str,
        station_id: str = "",
        limit: int = 0,
    ) -> Iterator[_domain.EpisodeSchedule]:
        """
        Get scheduled shows for the given date range and station.

        :param since: FIXME
        :param till: FIXME
        :param station_id: FIXME
        :returns: All scheduled shows for the given date range and station.

        Examples:
        >>> client = Client()
        >>> client.get_schedule_by_date(since=???, till=???)
        >>> client.get_schedule_by_date(since=???, till=???, "11")
        """
        path = f"schedule?filter[since][ge]={since}&filter[till][le]={till}"
        data = self._build_route(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _domain.EpisodeSchedule
        )
        # NOTE: This station filter does not work!
        # filter[station]={station_uuid}
        if station_id != "":
            station_uuid = self._get_station_guid(station_id)
            epschedules = list(
                filter(
                    lambda ep: (ep.station == station_uuid),  # type: ignore
                    epschedules,
                )
            )
        for episode_schedule in epschedules:
            yield episode_schedule

    def get_schedule_for_station(
        self,
        show_id: str,
        station_id: str,
        since: str,
        till: str,
        limit: int = 100,
    ):
        """
        Get show schedule and filter it by optional parameters.

        >>> client = Client()
        >>> client.get_schedule("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        >>> client.get_schedule("", "11")
        >>> Client.get_schedule("", "", "2021-09-01", "2021-09-02")
        """
        path = "schedule"
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
        link = path + "?" + "&".join(urlfilters) + "&sort=since"
        data = self._build_route(link, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _domain.EpisodeSchedule
        )
        for episode_schedule in epschedules:
            yield episode_schedule

    def get_person(self, person_id: str, limit: int = 0) -> _domain.Person | None:
        """
        Get person metadata by person guid.

        >>> Client.get_person("1cb35d9d-fb24-37ee-8993-9f74e57ab2c7")
        """
        path = "persons/" + person_id
        data = self._build_route(path, limit)
        out = _shared.class_attrs_by_anotation_dict(data[0], _domain.Person)
        if out is not None:
            assert isinstance(out, _domain.Person)
        return out

    def get_show_participants_with_roles(
        self,
        show_id: str,
        limit: int = 0,
    ) -> Iterator[_domain.Person]:
        """
        Get show participants and their roles in show

        >>> Client.get_show_participants_with_roles("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        # NOTE: relationships.participants.data:
        # [{'type': 'person', 'id': '1cb35d9d-fb24-37ee-8993-9f74e57ab2c7', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': '7b9d1544-8aab-3730-8f0a-4d0b463322be', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'c5b35399-08c6-3057-8145-c6aaaac76d4d', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'fcb6babc-e5f6-3b30-b126-583885584454', 'meta': {'role': 'moderator'}}]

        path = "shows/" + show_id
        data = self._build_route(path, limit)
        json_base_path = ["relationships", "participants", "data"]
        persons_meta = _shared.dict_get_path(data[0], [*json_base_path])
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
        limit: int = 0,
    ) -> Iterator[_domain.Person]:
        """
        Get show participants and filter them by role "moderator".

        >>> client.get_show_moderators("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        persons = self.get_show_participants_with_roles(show_id, limit)
        moderators = list(
            filter(
                lambda person: (person.role == "moderator"),  # type: ignore
                persons,
            )
        )
        for moderator in moderators:
            yield moderator

    def get_show_participants(
        self, show_id: str, limit: int = 0
    ) -> Iterator[_domain.Person]:
        """
        Get show participants regardless of their roles. Alternative to get_show_participants_with_roles.

        >>> client.get_show_participants("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        path = "shows/" + show_id + "/participants"
        data = self._build_route(path, limit)
        persons = _shared.class_attrs_by_anotation_list(data, _domain.Person)
        for person in persons:
            yield person

    def get_show_episodes_last_repetition(
        self, show_id: str, limit: int = 0
    ) -> Iterator[_domain.EpisodeSchedule]:
        """
        Get show episodes last repetitions.

        >>> client = Client()
        >>> result = client.get_show_episode_last_repetition("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        >>> result != None
        True
        """
        # NOTE: Acording to Jan Hejzl (see features discussion: file:./docs/build/features_discusion.html) the date of premiere is automaticaly rewritten with the date of episode repetition
        path = "shows/" + show_id + "/schedule-episodes"  # Returns empty
        # endpoint="serials/"
        # endpoint="schedule/"+id
        # endpoint="program/" # very slow
        data = self._build_route(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _domain.EpisodeSchedule
        )

        for episode_schedule in epschedules:
            yield episode_schedule


if __name__ == "__main__":
    import doctest

    doctest.testmod()
