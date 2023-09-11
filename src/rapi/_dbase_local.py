import os
import sys
from datetime import datetime, timedelta
from typing import Union

from rapi import _helpers
from rapi._config import CFG
from rapi._logger import log_stderr as loge
from rapi._logger import log_stdout as logo


class DB_local:
    def __init__(self, cfg: CFG = CFG()):
        self.Cfg = cfg
        self.urls = cfg.runtime_get(["apis", "croapp", "urls"])
        self.endpoints = cfg.runtime_get(["apis", "croapp", "endpoints"])
        # path = os.path.join(base_dir, self.__class__.__name__, "db")
        cfgb = ["apis", "croapp", "db_local"]
        path = cfg.runtime_get([*cfgb, "csvs_workdir"])
        # _helpers.mkdir_parent_panic(path)
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
        jdict = _helpers.request_url_json(link)
        if jdict is None:
            loge.error(f"no data to save: {endpoint}")
            return None
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning(f"no data section to parse: {endpoint}")
            return None

        nlink = self.endpoint_get_next_link(jdict)
        while nlink != "":
            jdict = _helpers.request_url_json(nlink)
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
        jdata = _helpers.request_url_json(link)
        return jdata

    def endpoint_save_json(self, endpoint: str, limit: int = 0) -> bool:
        jdata = self.endpoint_get_json(endpoint, limit)
        if jdata is None:
            loge.error(f"no data to save: {endpoint}")
            return False
        directory = self.Cfg.runtime_get(["apis", "croapp", "workdir", "dir"])
        filepath = os.path.join(directory, "json")
        ok = _helpers.save_json(filepath, endpoint + ".json", jdata)
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
        # _helpers.mkdir_parent_panic(path)
        # dpaht=os.path.join(self.cscs_workdir, endpoint)
        fpath = os.path.join(self.cscs_workdir, endpoint + ".csv")
        dpath = os.path.dirname(fpath)
        _helpers.mkdir_parent_panic(dpath)
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
        jdict = _helpers.request_url_json(link)
        if jdict is None:
            loge.warning(f"no json to parse: {endpoint}")
            return ""
        data = jdict.get("data", None)
        if data is None or len(data) == 0:
            loge.warning(f"no data section to parse: {endpoint}")
            return ""
        ### save data to csv
        rows, header = _helpers.dict_list_to_rows(data)
        if not os.path.exists(fpath):
            _helpers.save_rows_to_csv(fpath, rows, header)
        else:
            _helpers.save_rows_to_csv(fpath, rows)
        if not os.path.exists(fpath_fields):
            tdata = _helpers.rows_transpose([header])
            _helpers.save_rows_to_csv(fpath_fields, tdata)
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
