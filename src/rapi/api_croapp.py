import os
import sys
import time
from dataclasses import asdict, dataclass, make_dataclass
from datetime import datetime, timedelta
from typing import Type, Union

import requests
from dacite import from_dict
from dataclasses_json import dataclass_json
from requests import Session, get

from rapi import config, helpers, station_ids
from rapi.helpers import dict_get_path as DGP
from rapi.logger import log_stderr as loge
from rapi.logger import log_stdout as logo
from rapi.model import Show, Station, StationIDs


class API:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.DB_local = DB_local(cfg)
        self.api_url = cfg.runtime_get(["apis", "croapp", "urls", "api"])
        self.StationIDs = station_ids.StationIDs(cfg)

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

    def get_station_guid(self, station_id: str) -> Union[str, None]:
        sid = StationIDs()
        fkey = self.StationIDs.get_fkey(station_id, sid.croapp_guid)
        return fkey

    # def get_stations(self)->tuple[Station, ...]:
    def get_stations(self, limit: int = 0) -> tuple[Station, ...]:
        jdata = self.DB_local.endp_get_json("stations", limit)
        if jdata is None:
            loge.error("no json downloaded")
            return None
        data = jdata.get("data", None)
        if data is None or len(data) == 0:
            loge.error("no data to extract")
            return None
        paths = helpers.dict_paths_vectors(data[0], list())

        ### select fields from json by position
        fields = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ### creat output list
        out: list = list()
        for d in data:
            st = Station()
            res = helpers.class_assign_attrs_fieldnum(st, d, fields, paths)
            out.append(res)
        return tuple(out)

    def get_station(self, station_id: str) -> Station | None:
        guid = self.get_station_guid(station_id)
        try:
            return tuple(filter(lambda x: x.id == guid, self.get_stations()))[
                0
            ]
        except IndexError:
            raise ValueError(f"The station with id `{id}` does not exist.")

    def get_station_shows(self, station_id: str, limit: int = 0):
        guid = self.get_station_guid(station_id)
        if guid is None:
            loge.error("unknown station id")
            return None
        endp = "stations/" + guid + "/shows"
        jdata = self.DB_local.endp_get_json(endp, limit)
        if jdata is None:
            loge.error("no json downloaded")
            return
        # print(jdata["links"])
        links = jdata.get("links", None)
        if links is not None:
            nlink = links.get("next", None)
            if nlink is not None:
                loge.warning("not all data downloaded")
        data = jdata.get("data", None)
        if data is None or len(data) == 0:
            loge.error("no data to extract")
            return None

        ### select fields
        fields = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
        ### create otput list
        paths = helpers.dict_paths_vectors(data[0], list())
        out: list = list()
        for d in data:
            show = Show()
            res = helpers.class_assign_attrs_fieldnum(show, d, fields, paths)
            out.append(res)
        return tuple(out)

    def get_show_episodes(self, episode_id: str, limit: int = 0):
        pass


class DB_local:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endps = cfg.runtime_get(["apis", "croapp", "endpoints"])
        # path= self.Cfg.runtime_get(["apis", "croapp", "DB_local", "csv_workdir"])
        # path = os.path.join(base_dir, self.__class__.__name__, "db")
        cfgb = ["apis", "croapp", "db_local"]
        path = cfg.runtime_get([*cfgb, "csvs_workdir"])
        helpers.mkdir_parent_panic(path)
        self.cscs_workdir = path
        self.csvs_update = cfg.runtime_get([*cfgb, "csvs_update"])

    def endp_get_link(self, endp: str, limit: int = 0) -> str:
        cfgb = ["apis", "croapp", "response"]
        if limit == 0:
            limit = self.Cfg.runtime_get([*cfgb, "limit"])

        api_url = self.urls.get("api", "")
        if api_url == "":
            loge.error(f"api url not defined")
            sys.exit(1)
        endp_url = "/".join((api_url, endp))

        limstr = self.Cfg.runtime_get([*cfgb, "limit_str"])
        if limit > 0 and limstr is not None:
            endp_url = endp_url + limstr + str(limit)
        return endp_url

    def endp_get_full_json(self, endp: str, limit: int = 0):
        link = self.endp_get_link(endp, limit)
        jdict = helpers.request_url_json(link)
        if jdict is None:
            loge.error(f"no data to save: {endp}")
            return False
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning(f"no data section to parse: {endp}")
            return ""
        # nlink=self.endp_get_next_link(jdata)
        # jdata=self.endp_get_json(endp,limit)

    def endp_get_json(self, endp: str, limit: int = 0) -> Union[dict, None]:
        link = self.endp_get_link(endp, limit)
        jdata = helpers.request_url_json(link)
        return jdata

    def endp_save_json(self, endp: str, limit: int = 0) -> bool:
        jdata = self.endp_get_json(endp, limit)
        if jdata is None:
            loge.error(f"no data to save: {endp}")
            return False
        directory = self.Cfg.runtime_get(["apis", "croapp", "workdir", "dir"])
        filepath = os.path.join(directory, "json")
        ok = helpers.save_json(filepath, endp + ".json", jdata)
        return ok

    def endps_save_json(self, limit: int = 0):
        cfgb = [
            "apis",
            "croapp",
        ]
        eps = self.Cfg.runtime_get([*cfgb, "endpoints"])
        for e in eps:
            ok = self.endp_save_json(e, limit)
            if ok is False:
                loge.error("endpoint json not saved: {e}")

    def endps_csv_update(self, limit: int = 0, follow: bool = False):
        for e in self.endps:
            self.endp_csv_update(e, "", limit, follow)

    def endp_csv_update(
        self, endp: str, nlink: str = "", limit: int = 0, follow: bool = False
    ):
        logo.info(f"updating from: {endp}")
        nlink = self.endp_csv_get_data(endp, limit)
        if follow is False:
            return
        while True:
            logo.info(f"nextlink: {nlink}")
            nlink = self.endp_csv_get_data(endp, 0, nlink)
            if nlink == "":
                break

    def endp_csv_get_data(
        self, endp: str, limit: int = 0, nlink: str = ""
    ) -> str:
        # helpers.mkdir_parent_panic(path)
        # dpaht=os.path.join(self.cscs_workdir, endp)
        fpath = os.path.join(self.cscs_workdir, endp + ".csv")
        dpath = os.path.dirname(fpath)
        helpers.mkdir_parent_panic(dpath)
        fpath_fields = os.path.join(self.cscs_workdir, endp + "_fields.csv")
        if not self.endp_file_needs_update(fpath):
            return ""
        # logo.info(f"updating endp file: {fpath}")

        ### endp files delete (cleanup)
        logo.info(f"before delete: {nlink}")
        if nlink == "":
            link = self.endp_get_link(endp, limit)
            self.endp_file_clear([fpath, fpath_fields])
        else:
            link = nlink
        ### download data
        jdict = helpers.request_url_json(link)
        if jdict is None:
            loge.warning(f"no json to parse: {endp}")
            return ""
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning(f"no data section to parse: {endp}")
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
        return self.endp_get_next_link(jdict)

    def endp_file_needs_update(self, endp_file: str) -> bool:
        update = False
        fpath = endp_file
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

    def endp_file_clear(self, files: list[str]):
        for file in files:
            if os.path.exists(file):
                logo.info(f"deleting endpoint file: {file}")
                os.remove(file)

    def endp_get_next_link(self, respone_json: dict) -> str:
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
