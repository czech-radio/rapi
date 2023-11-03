"""
Module contains HTTP REST API client.
"""

from datetime import datetime
from typing import ClassVar, Iterator

import requests

import rapi._model as _model
import rapi._services as _services
import rapi._shared as _shared


class Client:
    """
    The REST client to fetch station, show, episodes and participants data.
    """

    api_url: ClassVar[str] = "https://api.mujrozhlas.cz"
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
            _services.StationsProvider()
        )  # FIXME Should be injected in consyructor!

    def __enter__(self):
        """Context manager related method."""
        return NotImplemented

    def __exit__(self) -> None:
        """Context manager related method."""
        return NotImplemented

    def __del__(self):
        """
        Close the the session when the reference is deleted.
        """
        if self._session is not None:
            self._session.close()

    def _get_endpoint_link(
        self,
        endpoint: str,
        limit: int = 0,
    ) -> str:
        """
        Create target URL from the given parameters.

        Example:
        >>> client = Client()
        >>> client._get_endpoint_link("schedule", "10")
        https://api.mujrozhlas.cz/schedule?page[limit]=10
        """
        endpoint_url = "/".join((self.api_url, endpoint))
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
        endpoint_url = "".join(endpoint_parts)
        return endpoint_url

    def _get_endpoint_data(self, endpoint: str, limit: int = 0) -> list[dict]:
        """
        Get all json pages from endpoint.

        :param endpoint: specific part or url which targets specific resource
        returns: json string

        Example:
        >>> client = Client()
        >>> client._get_endpoint_link("stations")
        """
        link = self._get_endpoint_link(endpoint, limit)
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

    def _get_endpoint(self, path: str = "", limit: int = 0) -> list[dict]:
        data = self._get_endpoint_data(path, limit)
        return data

    def get_station(self, station_id: int | str) -> _model.Station | None:
        """
        Get a specified station.

        Examples:
        >>> client = Client()
        >>> client.get_station(11)
        """
        guid = self._station_provider.get_station_guid(str(station_id))
        data = self._get_endpoint_data(f"stations/{guid}", 0)
        result = _shared.class_attrs_by_anotation_dict(data[0], _model.Station)
        return result

    def get_stations(self, limit: int = 100) -> Iterator[_model.Station]:
        """
        Get available stations.

        Examples:
        >>> client = Client()
        >>> result = client.get_stations(limit=10)
        """
        data = self._get_endpoint_data("stations", limit)
        result = _shared.class_attrs_by_anotation_list(data, _model.Station)
        for item in result:
            yield result

    def get_show(self, show_id: str) -> _model.Show | None:
        """
        Get a specified show.

        Examples:
        >>> client = Client()
        >>> client.get_show(uuid.UUID("9f36ee8f-73a7-3ed5-aafb-41210b7fb935"))
        """
        data = self._get_endpoint_data(f"shows/{show_id}", limit=0)
        result = _shared.class_attrs_by_anotation_dict(data[0], _model.Show)
        return result

    def get_shows(self, station_id: int, limit: int = 100) -> Iterator[_model.Show]:
        """
        Get shows for specified station.

        Examples:
        >>> client = Client()
        >>> client.get_station_shows(11)
        """
        guid = self._station_provider.get_station_guid(str(station_id))
        data = self._get_endpoint_data(f"stations/{guid}/shows", limit)
        result = _shared.class_attrs_by_anotation_list(data, _model.Show)
        for item in result:
            yield item

    def get_show_episodes(
        self, show_id: str, limit: int = 100
    ) -> Iterator[_model.Episode]:
        """
        Get episodes of specified show by show UUID.

        >>> client = Client()
        >>> client.get_show_episodes("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        data = self._get_endpoint_data(f"shows/{show_id}/episodes?sort=since", limit)
        episodes = _shared.class_attrs_by_anotation_list(data, _model.Episode)
        for episode in episodes:
            yield episode

    def get_show_episodes_filter(
        self,
        show_id: str,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        station_id: str | None = None,
        limit: int = 0,
    ) -> Iterator[_model.Episode]:
        """
        Get show episodes and filter them by optonal fields.

        >>> Client.shows_episodes_filter(
            "9f36ee8f-73a7-3ed5-aafb-41210b7fb935",
            "2022-09-10",
            "2023-09-11",
            "11",
        )
        """
        tzinfo = _shared.current_timezone()
        eps = self.get_show_episodes(show_id, limit)

        # filter by date
        if date_from is None:
            date_from = datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        if isinstance(date_from, str):
            date_from = _shared.parse_date_optional_fields(date_from)

        if date_to is None:
            date_to = datetime.now(tzinfo)
        if isinstance(date_to, str):
            date_to = _shared.parse_date_optional_fields(date_to)
        # NOTE: In the following lines mypy is disabled cause I don't
        # know how to make proper type hints.
        episodes = filter(
            lambda ep: (ep.since >= date_from) and (ep.till <= date_to),  # type: ignore
            eps,
        )
        for episode in episodes:
            yield episode  # type: ignore

    def get_show_episodes_schedule(
        self, show_id: str, limit: int = 0
    ) -> Iterator[_model.EpisodeSchedule]:
        """
        Get all show episodes schedules.

        >>> Client.get_show_episodes_schedule("9f36ee8f-73a7-3ed5-aafb-41210b7fb935")
        """
        path = f"shows/{show_id}/schedule-episodes?sort=since"
        data = self._get_endpoint_data(path, limit)
        episodes_schedules = _shared.class_attrs_by_anotation_list(
            data, _model.EpisodeSchedule
        )
        for episode_schedule in episodes_schedules:
            yield episode_schedule

    def get_station_schedule_day_flat(
        self,
        day: str,
        station_id: str = "",
        limit: int = 0,
    ) -> Iterator[_model.EpisodeSchedule]:
        """
        Get station schedule without relationships for a given day.

        >>> client = Client()
        >>> client.get_station_schedule_day("2023-10-09")
        >>> client.get_station_schedule_day("2023-10-09", "11")
        """
        path = f"schedule-day-flat?filter[day]={day}"
        data = self._get_endpoint_data(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _model.EpisodeSchedule
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
    ) -> Iterator[_model.EpisodeSchedule]:
        """
        Get station's schedule without relationships for given day."

        >>> client = Client()
        >>> client.get_station_schedule_day("2023-10-09")
        >>> client.get_station_schedule_day("2023-10-09", "11")
        """

        path = f"schedule-day?filter[day]={day}"
        data = self._get_endpoint_data(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _model.EpisodeSchedule
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
    ) -> Iterator[_model.EpisodeSchedule]:
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
        data = self._get_endpoint_data(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _model.EpisodeSchedule
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
        data = self._get_endpoint_data(link, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _model.EpisodeSchedule
        )
        for episode_schedule in epschedules:
            yield episode_schedule

    def get_person(self, person_id: str, limit: int = 0) -> _model.Person | None:
        """
        Get person metadata by person guid.

        >>> Client.get_person("1cb35d9d-fb24-37ee-8993-9f74e57ab2c7")
        """
        path = "persons/" + person_id
        data = self._get_endpoint_data(path, limit)
        out = _shared.class_attrs_by_anotation_dict(data[0], _model.Person)
        if out is not None:
            assert isinstance(out, _model.Person)
        return out

    def get_show_participants_with_roles(
        self,
        show_id: str,
        limit: int = 0,
    ) -> Iterator[_model.Person]:
        """
        Get show participants and their roles in show

        >>> Client.get_show_participants_with_roles("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        # NOTE: relationships.participants.data:
        # [{'type': 'person', 'id': '1cb35d9d-fb24-37ee-8993-9f74e57ab2c7', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': '7b9d1544-8aab-3730-8f0a-4d0b463322be', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'c5b35399-08c6-3057-8145-c6aaaac76d4d', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'fcb6babc-e5f6-3b30-b126-583885584454', 'meta': {'role': 'moderator'}}]

        path = "shows/" + show_id
        data = self._get_endpoint_data(path, limit)
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
    ) -> Iterator[_model.Person]:
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
    ) -> Iterator[_model.Person]:
        """
        Get show participants regardless of their roles. Alternative to get_show_participants_with_roles.

        >>> client.get_show_participants("c7374f41-ae14-3b5c-8c04-385e3241deb4")
        """
        path = "shows/" + show_id + "/participants"
        data = self._get_endpoint_data(path, limit)
        persons = _shared.class_attrs_by_anotation_list(data, _model.Person)
        for person in persons:
            yield person

    def get_show_episodes_last_repetition(
        self, show_id: str, limit: int = 0
    ) -> Iterator[_model.EpisodeSchedule]:
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
        data = self._get_endpoint_data(path, limit)
        epschedules = _shared.class_attrs_by_anotation_list(
            data, _model.EpisodeSchedule
        )

        for episode_schedule in epschedules:
            yield episode_schedule


if __name__ == "__main__":
    import doctest

    doctest.testmod(__name__)
