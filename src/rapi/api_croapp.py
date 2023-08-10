import os
import sys
from datetime import datetime, timedelta
from typing import Union
import time

from rapi import config, helpers
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class Api_croapp:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endpoints = cfg.runtime_get(["apis", "croapp", "endpoints"])
        base_dir = cfg.runtime_get(["workdir", "dir"])
        path = os.path.join(base_dir, self.__class__.__name__, "db")
        helpers.mkdir_parent_panic(path)
        self.DB_work_dir = path
        self.DB_update = cfg.runtime_get(["apis", "croapp", "update_local_db"])

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

    def endpoint_file_clear(self,files:list[str]):
        for file in files:
            if os.path.exists(file):
                logo.info(f"deleting endpoint file: {file}")
                os.remove(file)

    def endpoint_get_next_link(self,respone_json: dict)->str:
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
        self,endp: str,nlink: str="",nlimit: int=100):
        logo.info(f"updating from: {endp}")
        nlink=self.endpoint_link_get_data(endp)
        logo.info(f"nextlink: {nlink}")
        while True:
            # time.sleep(3)
            nlink=self.endpoint_link_get_data(endp,100,nlink)
            logo.info(f"second: {nlink}")
            if nlink == "":
                break

    def endpoint_link_get_data(
            self, endp: str, nlimit: int=100,
            next_link: str = "") -> str:
        fpath = os.path.join(self.DB_work_dir, endp + ".csv")
        fpath_fields = os.path.join(self.DB_work_dir, endp + "_fields.csv")
        if not self.endpoint_file_needs_update(fpath):
            return ""
        # logo.info(f"updating endpoint file: {fpath}")

        ### endpoint files delete (cleanup)
        logo.info(f"before delete: {next_link}")
        if next_link == "":
            link = self.endpoint_get_url(endp)
            self.endpoint_file_clear([fpath,fpath_fields])
        else:
            link=next_link
        ### download data
        jdict = helpers.request_url_json(link)
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning( f"no data section to parse: {endp}")
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

    def update_local_db(self):
        for e in self.endpoints:
            self.endpoint_file_update(e)
