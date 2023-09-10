import os
import sys
import time
from dataclasses import (asdict, dataclass, is_dataclass, make_dataclass,
                         replace)
from datetime import datetime, timedelta
from typing import (Any, Callable, Generator, Iterable, List, Type, TypeVar,
                    Union)

import requests
from dacite import from_dict
from dataclasses_json import dataclass_json
from requests import Session, get

from rapi import _config
from rapi import _helpers
from rapi import _helpers as helpers
from rapi import _station_ids
from rapi._config import CFG
from rapi._helpers import dict_get_path as DGP
from rapi._logger import log_stderr as loge
from rapi._logger import log_stdout as logo
from rapi._model import (Episode, Show, Station, StationIDs, episode_anotation,
                         show_anotation, station_anotation)


class Client:
    def __init__(self, cfg: CFG = CFG()):
        cfg.cfg_runtime_set_defaults()
        self.Cfg = cfg
        self.DB_local = DB_local(cfg)
        self.api_url = cfg.runtime_get(["apis", "croapp", "urls", "api"])
        self.StationIDs = _station_ids.StationIDs(cfg)
        session = requests.Session()
        headers = {"User-Agent": __name__}
        session.headers.update(headers)
        self._session = session

    def __del__(self):
        if self._session:
            self._session.close()

    def get_swagger(self) -> Union[dict, None]:
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
            endpoint_url = endpoint_url + limstr + str(limit)
        return endpoint_url

    ### add return value
    def _get_endpoit_full_json(self, endpoint: str, limit: int = 0):
        link = self._get_endpoint_link(endpoint, limit)
        out: list = list()
        while link:
            logo.debug(f"request url: {link}")
            response = self._session.get(link)
            response.raise_for_status()  # non-2xx status exception
            jdata = response.json()
            data = jdata["data"]
            if not isinstance(data, list):
                data = [data]
            out = out + data
            link = jdata.get("links", {}).get("next")
        return out

    def assign_fields(
        self, data: list[dict], fields: list[int], dclass=Type[dataclass]
    ) -> list[Any]:
        """
        Assign fields from list of json dicts to list of arbitrary dataclass.
        """
        out: list = list()
        paths: list = list()
        for d in data:
            dcc = replace(dclass)
            if len(paths) == 0:
                paths = helpers.dict_paths_vectors(d, list())
            res = helpers.class_assign_attrs_fieldnum(dcc, d, fields, paths)
            out.append(res)
        return out

    def get_station(self, station_id: str, limit: int = 0) -> Station | None:
        guid = self.get_station_guid(station_id)
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

    def get_stations(self, limit: int = 0) -> tuple[Station, ...]:
        endpoint = "stations"
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_list(
            data,
            Station(),
            station_anotation,
        )
        return tuple(out)

    def get_station_shows(
        self, station_id: str, limit: int = 0
    ) -> tuple[Show, ...]:
        guid = self.get_station_guid(station_id)
        endpoint = "stations/" + guid + "/shows"
        data = self._get_endpoit_full_json(endpoint, limit)
        out = _helpers.class_attrs_by_anotation_list(
            data,
            Show(),
            show_anotation,
        )
        return tuple(out)

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
        tzinfo = _helpers.current_pytz_timezone()
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
        # NOTE: in following lines mypy is disable cause I don't know how to make proper typehints
        out = filter(
            lambda ep: (ep.since >= date_from) and (ep.till <= date_to),  # type: ignore
            eps,
        )

        return tuple(out)  # type: ignore


class DB_local:
    def __init__(self, cfg: CFG):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endpoints = cfg.runtime_get(["apis", "croapp", "endpoints"])
        # path = os.path.join(base_dir, self.__class__.__name__, "db")
        cfgb = ["apis", "croapp", "db_local"]
        path = cfg.runtime_get([*cfgb, "csvs_workdir"])
        # helpers.mkdir_parent_panic(path)
        self.cscs_workdir = path
        self.csvs_update = cfg.runtime_get([*cfgb, "csvs_update"])

    def endpoint_get_link(self, endpoint: str, limit: int = 0) -> str:
        cfgb = ["apis", "croapp", "response"]
        if limit == 0:
            limit = self.Cfg.runtime_get([*cfgb, "limit"])

        api_url = self.urls.get("api", "")
        if api_url == "":
            loge.error(f"api url not defined")
            sys.exit(1)
        endpoint_url = "/".join((api_url, endpoint))

        limstr = self.Cfg.runtime_get([*cfgb, "limit_str"])
        if limit > 0 and limstr is not None:
            endpoint_url = endpoint_url + limstr + str(limit)
        return endpoint_url

    def endpoint_get_full_json(self, endpoint: str, limit: int = 0):
        link = self.endpoint_get_link(endpoint, limit)
        jdict = helpers.request_url_json(link)
        if jdict is None:
            loge.error(f"no data to save: {endpoint}")
            return None
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning(f"no data section to parse: {endpoint}")
            return None

        nlink = self.endpoint_get_next_link(jdict)
        while nlink != "":
            jdict = helpers.request_url_json(nlink)
            if jdict is not None:
                jdata = jdict.get("data", None)
                if jdata is not None:
                    data = data + jdata
                nlink = self.endpoint_get_next_link(jdict)
        return data

    def endpoint_get_json(
        self, endpoint: str, limit: int = 0
    ) -> Union[dict, None]:
        link = self.endpoint_get_link(endpoint, limit)
        jdata = helpers.request_url_json(link)
        return jdata

    def endpoint_save_json(self, endpoint: str, limit: int = 0) -> bool:
        jdata = self.endpoint_get_json(endpoint, limit)
        if jdata is None:
            loge.error(f"no data to save: {endpoint}")
            return False
        directory = self.Cfg.runtime_get(["apis", "croapp", "workdir", "dir"])
        filepath = os.path.join(directory, "json")
        ok = helpers.save_json(filepath, endpoint + ".json", jdata)
        return ok

    def endpoints_save_json(self, limit: int = 0):
        cfgb = [
            "apis",
            "croapp",
        ]
        eps = self.Cfg.runtime_get([*cfgb, "endpoints"])
        for e in eps:
            ok = self.endpoint_save_json(e, limit)
            if ok is False:
                loge.error("endpoint json not saved: {e}")

    def endpoints_csv_update(self, limit: int = 0, follow: bool = False):
        for e in self.endpoints:
            self.endpoint_csv_update(e, "", limit, follow)

    def endpoint_csv_update(
        self,
        endpoint: str,
        nlink: str = "",
        limit: int = 0,
        follow: bool = False,
    ):
        logo.info(f"updating from: {endpoint}")
        nlink = self.endpoint_csv_get_data(endpoint, limit)
        if follow is False:
            return
        while True:
            logo.info(f"nextlink: {nlink}")
            nlink = self.endpoint_csv_get_data(endpoint, 0, nlink)
            if nlink == "":
                break

    def endpoint_csv_get_data(
        self, endpoint: str, limit: int = 0, nlink: str = ""
    ) -> str:
        # helpers.mkdir_parent_panic(path)
        # dpaht=os.path.join(self.cscs_workdir, endpoint)
        fpath = os.path.join(self.cscs_workdir, endpoint + ".csv")
        dpath = os.path.dirname(fpath)
        helpers.mkdir_parent_panic(dpath)
        fpath_fields = os.path.join(
            self.cscs_workdir, endpoint + "_fields.csv"
        )
        if not self.endpoint_file_needs_update(fpath):
            return ""
        # logo.info(f"updating endpoint file: {fpath}")

        ### endpoint files delete (cleanup)
        logo.info(f"before delete: {nlink}")
        if nlink == "":
            link = self.endpoint_get_link(endpoint, limit)
            self.endpoint_file_clear([fpath, fpath_fields])
        else:
            link = nlink
        ### download data
        jdict = helpers.request_url_json(link)
        if jdict is None:
            loge.warning(f"no json to parse: {endpoint}")
            return ""
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning(f"no data section to parse: {endpoint}")
            return ""
        ### save data to csv
        rows, header = helpers.dict_list_to_rows(data)
        if not os.path.exists(fpath):
            helpers.save_rows_to_csv(fpath, rows, header)
        else:
            helpers.save_rows_to_csv(fpath, rows)
        if not os.path.exists(fpath_fields):
            tdata = helpers.rows_transpose([header])
            helpers.save_rows_to_csv(fpath_fields, tdata)
        ### return next link if any
        return self.endpoint_get_next_link(jdict)

    def endpoint_file_needs_update(self, endpoint_file: str) -> bool:
        update = False
        fpath = endpoint_file
        try:
            mtime = os.path.getmtime(fpath)
            if self.csvs_update == True:
                update = True
            if self.csvs_update == "daily":
                mdate_time = datetime.fromtimestamp(mtime)
                td = timedelta(days=1)
                ### check if file is older than one day
                if datetime.now() > mdate_time + td:
                    update = True
        except FileNotFoundError:
            update = True
        return update

    def endpoint_file_clear(self, files: list[str]):
        for file in files:
            if os.path.exists(file):
                logo.info(f"deleting endpointoint file: {file}")
                os.remove(file)

    def endpoint_get_next_link(self, respone_json: dict) -> str:
        links = respone_json.get("links", None)
        if links is None:
            return ""
        nlink = links.get("next", None)
        if nlink is None:
            return ""
        if nlink == "":
            return ""
        logo.info(f"trying next link: {nlink}")
        return nlink
