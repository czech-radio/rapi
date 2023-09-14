import os
from datetime import datetime
from typing import Iterator

import requests

from rapi import _helpers, _station_ids
from rapi._config import Config
from rapi._logger import log_stdout as logo
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


class Client:
    def __init__(self, cfg: Config = Config()):
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
        ydata = _helpers.request_url_yaml(url)
        if ydata is None:
            logo.error("data not avaiable")
        return ydata

    def save_swagger(self) -> bool:
        ydata = self.get_swagger()
        if ydata is None:
            return False
        directory = self.Cfg.runtime_get(["apis", "croapp", "workdir", "dir"])
        filepath = os.path.join(directory, "apidef")
        ok = _helpers.save_yaml(filepath, "swagger.yml", ydata)
        return ok

    def get_station_guid(self, station_id: str) -> str:
        sid = StationIDs()
        fkey = self.StationIDs.get_fkey(station_id, sid.croapp_guid)
        if fkey is None:
            raise ValueError(f"Unknown station with id {station_id}")
        return fkey

    def get_station_code(self, station_id: str) -> str:
        sid = StationIDs()
        fkey = self.StationIDs.get_fkey(station_id, sid.croapp_code)
        if fkey is None:
            raise ValueError(f"Unknown station with id {station_id}")
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

    def _get_endpoit_full_json(self, endpoint: str, limit: int = 0):
        link = self._get_endpoint_link(endpoint, limit)
        out: list = list()
        while link:
            logo.debug(f"request url: {link}")
            response = self._session.get(link)
            response.raise_for_status()  # non-2xx status exception
            jdata = response.json()
            # print(jdata)
            data = jdata["data"]
            if not isinstance(data, list):
                data = [data]
            out = out + data
            link = jdata.get("links", {}).get("next")
        return out

    def get_station(self, station_id: str, limit: int = 0) -> Station | None:
        guid = self.get_station_guid(str(station_id))
        endpoint = "stations/" + guid
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_dict(
            data[0],
            Station(),
            station_anotation,
        )
        if out is not None:
            assert isinstance(out, Station)
        return out

    def get_stations(self, limit: int = 0) -> Iterator[Station]:
        data = self._get_endpoit_full_json("stations", limit)
        stations = _helpers.class_attrs_by_anotation_list(
            data,
            Station(),
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
        shows = _helpers.class_attrs_by_anotation_list(
            data,
            Show(),
            show_anotation,
        )
        for show in shows:
            yield show

    def get_show(self, show_id: str, limit: int = 0) -> Show | None:
        endpoint = "shows/" + show_id
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_dict(
            data[0],
            Show(),
            show_anotation,
        )
        if out is not None:
            assert isinstance(out, Show)
        return out

    def get_show_episodes(
        self, episode_id: str, limit: int = 0
    ) -> tuple[Episode, ...]:
        endpoint = "shows/" + episode_id + "/episodes"
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_list(
            data,
            Episode(),
            episode_anotation,
        )
        return tuple(out)

    def show_episodes_filter(
        self,
        episode_id: str,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        station_id: str | None = None,
        limit: int = 0,
    ) -> tuple[Episode, ...]:
        cmdpars = ["commands", "show_ep_filter"]
        getval = self.Cfg.runtime_get
        tzinfo = _helpers.current_timezone()
        eps = self.get_show_episodes(episode_id, limit)

        # filter by date
        if date_from is None:
            date_from = getval(
                [*cmdpars, "date_from"],
                datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzinfo),
            )
        if isinstance(date_from, str):
            date_from = _helpers.parse_date_optional_fields(date_from)

        if date_to is None:
            date_to = getval(
                [*cmdpars, "date_to"],
                datetime.now(tzinfo),
            )
        if isinstance(date_to, str):
            date_to = _helpers.parse_date_optional_fields(date_to)
        assert isinstance(date_to, datetime)
        assert isinstance(date_from, datetime)
        # NOTE: In the following lines mypy is disabled cause
        # I don't know how to make proper type hints.
        out = filter(
            lambda ep: (ep.since >= date_from) and (ep.till <= date_to),  # type: ignore
            eps,
        )

        return tuple(out)  # type: ignore

    def get_show_episodes_schedule(self, show_id: str, limit: int = 0):
        endpoint = "shows/" + show_id + "/schedule-episodes"
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule(),
            episode_schedule_anotation,
        )
        return out

    def get_station_schedule_day_flat(
        self, station_id: str = "", limit: int = 0
    ):
        # https://rapidev.croapp.cz/schedule-day-flat?station=radiozurnal
        ## not valid request when filtering by station
        # code=self.get_station_code(station_id)
        # code=self.get_station_guid(station_id)
        # endpoint = "schedule-day-flat"
        endpoint = "schedule-day-flat"
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_list(
            data,
            Episode_schedule(),
            episode_schedule_anotation,
        )
        if station_id != "":
            code = self.get_station_guid(station_id)
            out = filter(
                lambda ep: (ep.station == code),  # type: ignore
                out,
            )
        return out

    def get_schedule_day(
        self,
        date_from: str,
        date_to: str,
        station_id: str = "",
        limit: int = 0,
    ):
        date_from = _helpers.parse_date_optional_fields(date_from)
        date_from = str(date_from).replace(" ", "T")
        date_to = _helpers.parse_date_optional_fields(date_to)
        date_to = str(date_to).replace(" ", "T")
        uuid = self.get_station_guid(station_id)
        endpoint = "schedule-day?filter[station.id]=" + uuid
        data = self._get_endpoit_full_json(endpoint, -1)

    def get_schedule(self, station_id: str = "", limit: int = 0):
        uuid = self.get_station_guid(station_id)
        endpoint = "schedule?filter[since][ge]=2023-09-12T08:10:00+01:00"
        data = self._get_endpoit_full_json(endpoint, limit)

    def get_show_moderators(
        self, show_id: str, limit: int = 0
    ) -> tuple[Person, ...]:
        endpoint = "shows/" + show_id + "/participants"
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_list(
            data,
            Person(),
            person_anotation,
        )
        # NOTE: All persons, moderators not filtered yet. Seems there are
        # only moderators listed though. To get participation role: it can
        # be extracted from: shows/show_id: relationships.participants.data:
        # [{'type': 'person', 'id': '1cb35d9d-fb24-37ee-8993-9f74e57ab2c7', 'meta': {'role': 'moderator'}}]
        return tuple(out)

    def get_person(self, person_id: str, limit: int = 0) -> Person | None:
        endpoint = "persons/" + person_id
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_dict(
            data[0],
            Person(),
            person_anotation,
        )
        if out is not None:
            assert isinstance(out, Person)
        return out

    def get_show_premieres(self, id: str, limit: int = 0):
        endpoint = (
            "shows/" + id + "/schedule-episodes"
        )  # Note: returns empty data
        data = self._get_endpoit_full_json(endpoint, limit)
        return data

    def get_repetitions(self) -> Iterator[Episode]:
        return NotImplemented
