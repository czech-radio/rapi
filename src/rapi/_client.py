import os
from datetime import datetime
from typing import Iterator

import requests

from rapi import _station_ids
from rapi._model import (
    Episode,
    Episode_schedule,
    Person,
    Show,
    Station,
    StationIDs,
    episode_anotation,
    episode_schedule_anotation,
    person_anotation,
    show_anotation,
    station_anotation,
)
from rapi.config._config import Config
from rapi.helpers import helpers
from rapi.helpers._logger import log_stdout as logo


class Client:
    def __init__(
        self,
        cfg: Config = Config(__package__),
    ):
        cfg.cfg_runtime_set_defaults()
        self.Cfg = cfg
        self.api_url = cfg.runtime_get(
            [
                "apis",
                "croapp",
                "urls",
                "api",
            ]
        )
        self.StationIDs = _station_ids.StationIDs(cfg)
        session = requests.Session()
        headers = {"User-Agent": __name__}
        session.headers.update(headers)
        self._session = session

    def __del__(self):
        if self._session:
            self._session.close()

    def get_swagger(self) -> dict | None:
        url = self.Cfg.runtime_get(["apis", "croapp", "urls", "swagger"])
        ydata = helpers.request_url_yaml(url)
        if ydata is None:
            logo.error("data not avaiable")
        return ydata

    def save_swagger(self) -> bool:
        ydata = self.get_swagger()
        if ydata is None:
            return False
        directory = self.Cfg.runtime_get(["apis", "croapp", "workdir", "dir"])
        filepath = os.path.join(directory, "apidef")
        ok = helpers.save_yaml(filepath, "swagger.yml", ydata)
        return ok

    def get_station_guid(self, station_id: str) -> str:
        sid = StationIDs()
        fkey = self.StationIDs.get_fkey(station_id, sid.croapp_guid)
        if fkey is None:
            raise ValueError(f"guid not found for station_id: {station_id}")
        return fkey

    def get_station_code(self, station_id: str) -> str:
        sid = StationIDs()
        fkey = self.StationIDs.get_fkey(station_id, sid.croapp_code)
        if fkey is None:
            raise ValueError(f"code not found for station_id: {station_id}")
        return fkey

    def _get_endpoint_link(self, endpoint: str, limit: int = 0) -> str:
        cfgb = ["apis", "croapp", "response"]
        if limit == 0:
            limit = self.Cfg.runtime_get([*cfgb, "limit"])
        cfgu = ["apis", "croapp", "urls", "api"]
        api_url = self.Cfg.runtime_get(cfgu)
        if api_url is None:
            raise ValueError(f"{cfgu} not defined")
        endpoint_url = "/".join((api_url, endpoint))
        limstr = self.Cfg.runtime_get([*cfgb, "limit_str"])
        if limit > 0 and limstr is not None:
            if "?" in endpoint_url:
                opt_delim = "&"
            else:
                opt_delim = "?"
            endpoint_url = endpoint_url + opt_delim + limstr + str(limit)
        return endpoint_url

    def _get_endpoit_full_json(
        self, endpoint: str, limit: int = 0
    ) -> list[dict]:
        link = self._get_endpoint_link(endpoint, limit)
        out: list = list()
        while link:
            logo.debug(f"request url: {link}")
            try:
                response = self._session.get(link)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise requests.exceptions.RequestException(e, response.text)
            except Exception as e:
                raise Exception("frequest url: {link}", e)
            jdata = response.json()
            data = jdata["data"]
            if not isinstance(data, list):
                data = [data]
            out = out + data
            link = jdata.get("links", {}).get("next")
        return out

    def _get_endpoint(self, endpoint: str = "", limit: int = 0) -> list[dict]:
        data = self._get_endpoit_full_json(endpoint, limit)
        return data

    def get_station(self, station_id: str, limit: int = 0) -> Station | None:
        guid = self.get_station_guid(str(station_id))
        endpoint = "stations/" + guid
        data = self._get_endpoit_full_json(endpoint, limit)
        out = helpers.class_attrs_by_anotation_dict(
            data[0],
            Station,
            station_anotation,
        )
        if out is not None:
            assert isinstance(out, Station)
        return out

    def get_stations(self, limit: int = 0) -> Iterator[Station]:
        data = self._get_endpoit_full_json("stations", limit)
        stations = helpers.class_attrs_by_anotation_list(
            data,
            Station,
            station_anotation,
        )
        for station in stations:
            yield station

    def get_station_shows(
        self, station_id: str, limit: int = 0
    ) -> Iterator[Show]:
        guid = self.get_station_guid(station_id)
        endpoint = "stations/" + guid + "/shows"
        data = self._get_endpoit_full_json(endpoint, limit)
        shows = helpers.class_attrs_by_anotation_list(
            data,
            Show,
            show_anotation,
        )
        for show in shows:
            yield show

    def get_show(self, show_id: str, limit: int = 0) -> Show | None:
        endpoint = "shows/" + show_id
        data = self._get_endpoit_full_json(endpoint, limit)
        out = helpers.class_attrs_by_anotation_dict(
            data[0],
            Show,
            show_anotation,
        )
        return out  # type: ignore

    def get_show_episodes(
        self, episode_id: str, limit: int = 0
    ) -> Iterator[Episode]:
        endpoint = "shows/" + episode_id + "/episodes"
        data = self._get_endpoit_full_json(endpoint, limit)
        episodes = helpers.class_attrs_by_anotation_list(
            data,
            Episode,
            episode_anotation,
        )
        for episode in episodes:
            yield episode

    def show_episodes_filter(
        self,
        episode_id: str,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        station_id: str | None = None,
        limit: int = 0,
    ) -> Iterator[Episode]:
        cmdpars = ["commands", "show_ep_filter"]
        getval = self.Cfg.runtime_get
        tzinfo = helpers.current_timezone()
        eps = self.get_show_episodes(episode_id, limit)

        # filter by date
        if date_from is None:
            date_from = getval(
                [*cmdpars, "date_from"],
                datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzinfo),
            )
        if isinstance(date_from, str):
            date_from = helpers.parse_date_optional_fields(date_from)

        if date_to is None:
            date_to = getval(
                [*cmdpars, "date_to"],
                datetime.now(tzinfo),
            )
        if isinstance(date_to, str):
            date_to = helpers.parse_date_optional_fields(date_to)
        # NOTE: In the following lines mypy is disabled cause
        # I don't know how to make proper type hints.
        episodes = filter(
            lambda ep: (ep.since >= date_from) and (ep.till <= date_to),  # type: ignore
            eps,
        )
        for episode in episodes:
            yield episode  # type: ignore

    def get_show_episodes_schedule(
        self, show_id: str, limit: int = 0
    ) -> Iterator[Episode_schedule]:
        endpoint = "shows/" + show_id + "/schedule-episodes"
        data = self._get_endpoit_full_json(endpoint, limit)
        episodes_schedules = helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule,
            episode_schedule_anotation,
        )
        for episode_schedule in episodes_schedules:
            yield episode_schedule

    def get_station_schedule_day_flat(
        self,
        day: str,
        station_id: str = "",
        limit: int = 0,
    ) -> Iterator[Episode_schedule]:
        # NOTE:
        ## https://rapidev.croapp.cz/schedule-day-flat?station=radiozurnal
        ## not valid request when filtering by station
        ## endpoint = "schedule-day?filter[station.id]=" + uuid # NOT WORKING
        endpoint = f"schedule-day-flat?filter[day]={day}"
        data = self._get_endpoit_full_json(endpoint, limit)
        epschedules = helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule,
            episode_schedule_anotation,
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
        limit: int = 0,
    ) -> Iterator[Episode_schedule]:
        endpoint = f"schedule-day?filter[day]={day}"
        data = self._get_endpoit_full_json(endpoint, limit)
        epschedules = helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule,
            episode_schedule_anotation,
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
        date_from: datetime | str,
        date_to: datetime | str,
        station_id: str = "",
        limit: int = 0,
    ) -> Iterator[Episode_schedule]:
        # e.g.: https://rapidev.croapp.cz/schedule?filter[title][eq]=Zpr%C3%A1vy
        if not isinstance(date_from, str):
            date_from = str(date_from)
        if not isinstance(date_from, str):
            date_to = str(date_to)

        from_filter = f"filter[since][ge]={date_from}"
        to_filter = f"filter[till][le]={date_to}"
        endpoint = f"schedule?{from_filter}&{to_filter}"
        data = self._get_endpoit_full_json(endpoint, limit)
        epschedules = helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule,
            episode_schedule_anotation,
        )
        # endpoint=f"{endpoint}&filter[station]={station_uuid}" # NOT WORKING STATION FILTER
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

    def get_person(self, person_id: str, limit: int = 0) -> Person | None:
        endpoint = "persons/" + person_id
        data = self._get_endpoit_full_json(endpoint, limit)
        out = helpers.class_attrs_by_anotation_dict(
            data[0],
            Person,
            person_anotation,
        )
        if out is not None:
            assert isinstance(out, Person)
        return out

    def get_show_participants_with_roles(
        self,
        show_id: str,
        limit: int = 0,
    ) -> Iterator[Person]:
        # NOTE: relationships.participants.data:
        # [{'type': 'person', 'id': '1cb35d9d-fb24-37ee-8993-9f74e57ab2c7', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': '7b9d1544-8aab-3730-8f0a-4d0b463322be', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'c5b35399-08c6-3057-8145-c6aaaac76d4d', 'meta': {'role': 'moderator'}}, {'type': 'person', 'id': 'fcb6babc-e5f6-3b30-b126-583885584454', 'meta': {'role': 'moderator'}}]

        endpoint = "shows/" + show_id
        data = self._get_endpoit_full_json(endpoint, limit)
        base_path = ["relationships", "participants", "data"]
        persons_meta = helpers.dict_get_path(data[0], [*base_path])
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
    ) -> Iterator[Person]:
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
    ) -> Iterator[Person]:
        endpoint = "shows/" + show_id + "/participants"
        data = self._get_endpoit_full_json(endpoint, limit)
        persons = helpers.class_attrs_by_anotation_list(
            data,
            Person,
            person_anotation,
        )
        for person in persons:
            yield person

    def get_show_premieres(
        self, id: str, limit: int = 0
    ) -> Iterator[Episode_schedule]:
        # endpoint = "shows/" + show_id + "/participants"
        endpoint = "shows/" + id + "/schedule-episodes"  # Returns empty
        # endpoint="serials/"
        # endpoint="schedule/"+id
        # endpoint="program/" # very slow
        data = self._get_endpoit_full_json(endpoint, limit)
        epschedules = helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule,
            episode_schedule_anotation,
        )

        for episode_schedule in epschedules:
            yield episode_schedule

    def get_repetitions(self) -> Iterator[Episode]:
        return NotImplemented
