from typing import Union
import os
import sys
from datetime import datetime, timedelta
from rapi import config, helpers
from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


class Api_croapp:
    def __init__(self, cfg: config.CFG):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endpoints = cfg.runtime_get(["apis", "croapp", "endpoints"])
        base_dir=cfg.runtime_get(["workdir", "dir"])
        path=os.path.join(
                base_dir,self.__class__.__name__,"db")
        helpers.mkdir_parent_panic(path)
        self.DB_work_dir=path
        self.DB_update=cfg.runtime_get(["apis", "croapp", "update_local_db"])

    def endpoint_get_url(self,endpoint: str)-> str:
        api_url = self.urls.get("api", "")
        if api_url == "":
            loge.error(f"api url not defined")
            sys.exit(1)
        endp_url = "/".join((api_url, endpoint))
        return endp_url

    # def endpoint_get_json(self, endpoint: str) -> Union[dict, None]:
        # api_url = self.urls.get("api", "")
        # if api_url == "":
            # loge.error(f"api url not defined")
            # return None
        # endp_url = "/".join((api_url, endpoint))
        # jdict = helpers.request_url_json(endp_url)
        # return jdict

    def endpoint_file_needs_update(self,endpoint_file: str)->bool:
        update=False
        fpath=endpoint_file
        try:
            mtime=os.path.getmtime(fpath)
            if self.DB_update == True:
                update=True
            if self.DB_update == "daily":
                mdate_time=datetime.fromtimestamp(mtime)
                td=timedelta(days=1)
                ### check if file is older than one day
                if datetime.now() > mdate_time + td:
                    update = True
        except FileNotFoundError:
            update=True
        return update

    def endpoint_update(self,endp: str,endp_url: str=""):
        fpath=os.path.join(self.DB_work_dir,endp+".csv")
        fpath_fields=os.path.join(self.DB_work_dir,endp+"_fields"+".csv")
        if not self.endpoint_file_needs_update(fpath):
            return
        logo.info(f"updating endpoint file: {fpath}")
        logo.info(f"updating endpoint: {endp}")

        if endp_url == "":
            endp_url = self.endpoint_get_url(endp)
            if os.path.exists(fpath):
                logo.info(f"deleting endpoint file: {fpath}")
                os.remove(fpath)
            if os.path.exists(fpath_fields):
                os.remove(fpath_fields)

        ### download first batch
        jdict = helpers.request_url_json(endp_url)
        data=jdict.get("data",None)
        if data is None:
            loge.warn(f"cannot extract data section from json: {endp}, {endp_url}")
            return
        rows, header = helpers.dict_list_to_rows(data)
        helpers.save_rows_to_csv(fpath, rows, header)
        if not os.path.exists(fpath_fields):
            tdata = helpers.rows_transpose([header])
            helpers.save_rows_to_csv(fpath_fields, tdata)

        ### download next batch
        links=jdict.get("links",None)
        if links is None:
            return
        next_link=links.get("next",None)
        if next_link is None:
            return
        logo.info(f"trying next link: {next_link}")
        self.endpoint_update(endp,next_link)

    def update_local_db(self):
        for e in self.endpoints:
            self.endpoint_update(e)
