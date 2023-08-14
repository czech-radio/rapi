import os
import sys
import time
from dataclasses import asdict, dataclass, fields, make_dataclass
from datetime import datetime, timedelta
from typing import Type, Union
from dacite import from_dict

import requests
from dataclasses_json import dataclass_json
from requests import Session, get

from rapi import config, helpers, station_ids
from rapi.helpers import dict_get_path as DGP
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo
from rapi.model import Station, StationIDs, Show


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
    def get_stations(self, limit: int = 0):
        jdata = self.DB_local.endpoint_get_json("stations", limit)
        if jdata is None:
            loge.error("no json downloaded")
            return
        data = jdata.get("data", None)
        if data is None or len(data) == 0:
            loge.error("no data to extract")
            return None
        paths = helpers.dict_paths_vectors(data[0], list())
        ### select fields from json by position
        fields = [item for item in range(1, 9)]
        out: list = list()
        ### creat output list
        for e in data:
            j = 0
            st = Station()
            for i in st.__dict__:
                path = paths[fields[j]]
                st.__dict__[i] = DGP(e, path)
                j = j + 1
            out.append(st)
        return tuple(out)

    def get_station(self, station_id: str)-> Station | None:
        guid = self.get_station_guid(station_id)
        try:
            return tuple(filter(lambda x: x.id == guid, self.get_stations()))[0]
        except IndexError:
            raise ValueError(f"The station with id `{id}` does not exist.")

    def get_station_shows(self,station_id: str,limit: int=0):
        guid = self.get_station_guid(station_id)
        endp="stations/"+guid+"/shows"
        jdata=self.DB_local.endpoint_get_json(endp,limit)
        if jdata is None:
            loge.error("no json downloaded")
            return
        # print(jdata["links"])
        links=jdata.get("links",None)
        if links is not None:
            nlink=links.get("next",None)
            if nlink is not None:
                loge.warning("not all data downloaded")
        data = jdata.get("data", None)
        if data is None or len(data) == 0:
            loge.error("no data to extract")
            return None
        fields=[1,2,3,4,5,6,7,8,9,11,12]
        paths = helpers.dict_paths_vectors(data[0], list())
        out: list=list()
        for d in data:
            show=Show()
            res=helpers.class_assign_attrs_fieldnum(show,d,fields,paths)
            out.append(res)
        return tuple(out)


class DB_local:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endpoints = cfg.runtime_get(["apis", "croapp", "endpoints"])
        # path= self.Cfg.runtime_get(["apis", "croapp", "DB_local", "csv_workdir"])
        # path = os.path.join(base_dir, self.__class__.__name__, "db")
        cfgb = ["apis", "croapp", "DB_local"]
        path = cfg.runtime_get([*cfgb, "csvs_workdir"])
        helpers.mkdir_parent_panic(path)
        self.cscs_workdir = path
        self.csvs_update = cfg.runtime_get([*cfgb, "csvs_update"])

    def endpoint_get_link(self, endp: str, limit: int = 0) -> str:
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
        self, endp: str, nlink: str = "", limit: int = 0, follow: bool = False
    ):
        logo.info(f"updating from: {endp}")
        nlink = self.endpoint_csv_get_data(endp, limit)
        if follow is False:
            return
        while True:
            logo.info(f"nextlink: {nlink}")
            nlink = self.endpoint_csv_get_data(endp, 0, nlink)
            if nlink == "":
                break

    def endpoint_csv_get_data(
        self, endp: str, limit: int = 0, nlink: str = ""
    ) -> str:
        # helpers.mkdir_parent_panic(path)
        # dpaht=os.path.join(self.cscs_workdir, endp)
        fpath = os.path.join(self.cscs_workdir, endp + ".csv")
        dpath=os.path.dirname(fpath)
        helpers.mkdir_parent_panic(dpath)
        fpath_fields = os.path.join(self.cscs_workdir, endp + "_fields.csv")
        if not self.endpoint_file_needs_update(fpath):
            return ""
        # logo.info(f"updating endpoint file: {fpath}")

        ### endpoint files delete (cleanup)
        logo.info(f"before delete: {nlink}")
        if nlink == "":
            link = self.endpoint_get_link(endp, limit)
            self.endpoint_file_clear([fpath, fpath_fields])
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
                logo.info(f"deleting endpoint file: {file}")
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
