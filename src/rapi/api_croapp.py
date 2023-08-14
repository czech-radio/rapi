import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Type, Union

from dataclasses_json import dataclass_json
from requests import Session, get

from rapi import config, helpers, model, station_ids
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class API:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.api_url = cfg.runtime_get(["apis", "croapp", "urls", "api"])
        self.StationIDs = station_ids.StationIDs(cfg)

    def get_station_guid(self, station_id: str) -> Union[str, None]:
        sid = model.Station_ids()
        # helpers.pp(sid.__dict__)
        fkey = self.StationIDs.get_fkey(station_id, sid.croapp_guid)
        return fkey

    def get_station(self, station_id: str):
        guid = self.get_station_guid(station_id)
        url = f"{self.api_url}/stations"
        data = get(url).json()["data"]
        return data
        # for d in data:
        # ms=model.Station_data()
        # for i in ms.__dict__:
        # print(i)
        # print(ms.__dict__)
        # print(ms)
        # helpers.pprint(data)
        # res=tuple()
        # for item in data:
        # row=[]
        # res
        # res
        # helpers.pprint(item)
        # res=tuple(
        # [
        # model.Station_data()
        # for item in data
        # ]
        # )
        # helpers.pprint(res)


class DB_local_csv:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endpoints = cfg.runtime_get(["apis", "croapp", "endpoints"])
        base_dir = cfg.runtime_get(["workdir", "dir"])
        path = os.path.join(base_dir, self.__class__.__name__, "db")
        helpers.mkdir_parent_panic(path)
        self.DB_work_dir = path
        self.DB_update = cfg.runtime_get(["apis", "croapp", "update_db"])

    def endpoint_get_url(self, endpoint: str) -> str:
        api_url = self.urls.get("api", "")
        if api_url == "":
            loge.error(f"api url not defined")
            sys.exit(1)
        endp_url = "/".join((api_url, endpoint))
        return endp_url

    def endpoint_file_needs_update(self, endpoint_file: str) -> bool:
        update = False
        fpath = endpoint_file
        try:
            mtime = os.path.getmtime(fpath)
            if self.DB_update == True:
                update = True
            if self.DB_update == "daily":
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
        next_link = links.get("next", None)
        if next_link is None:
            return ""
        if next_link == "":
            return ""
        logo.info(f"trying next link: {next_link}")
        return next_link

    def endpoint_file_update(
        self, endp: str, nlink: str = "", nlimit: int = 100
    ):
        logo.info(f"updating from: {endp}")
        nlink = self.endpoint_link_get_data(endp)
        logo.info(f"nextlink: {nlink}")
        while True:
            # time.sleep(3)
            nlink = self.endpoint_link_get_data(endp, 100, nlink)
            logo.info(f"second: {nlink}")
            if nlink == "":
                break

    def endpoint_link_get_data(
        self, endp: str, nlimit: int = 100, next_link: str = ""
    ) -> str:
        fpath = os.path.join(self.DB_work_dir, endp + ".csv")
        fpath_fields = os.path.join(self.DB_work_dir, endp + "_fields.csv")
        if not self.endpoint_file_needs_update(fpath):
            return ""
        # logo.info(f"updating endpoint file: {fpath}")

        ### endpoint files delete (cleanup)
        logo.info(f"before delete: {next_link}")
        if next_link == "":
            link = self.endpoint_get_url(endp)
            self.endpoint_file_clear([fpath, fpath_fields])
        else:
            link = next_link
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

    def update_db(self):
        for e in self.endpoints:
            self.endpoint_file_update(e)
