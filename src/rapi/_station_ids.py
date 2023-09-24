from typing import Union

from rapi.config._config import Config
from rapi.helpers import helpers
from rapi.helpers._logger import log_stdout as loge


class StationIDs:
    def __init__(
        self,
        cfg: Config = Config(__package__),
    ) -> None:
        if cfg.cfg_sources is None:
            cfg.cfg_runtime_set_defaults()
        if cfg.cfg_runtime is None:
            cfg.cfg_runtime_set()

        self.Cfg = cfg
        bpath = ["apis", "common"]
        self.DBpath = self.Cfg.runtime_get(bpath + ["csv"])
        self.DB_pkey = self.Cfg.runtime_get(bpath + ["pkey"])
        self.DB = self.db_csv_init(self.DBpath)

    def db_csv_init(self, fspath: str = "default") -> list:
        # parse default or user specified table
        if fspath == "default":
            csvr = helpers.read_embeded_csv_to_ram(
                "data/stations_ids.csv", __package__
            )
        else:
            csvr = helpers.read_csv_path_to_ram(self.DBpath)
        if csvr is None:
            loge.error("cannot parse station_ids_csv")
            raise ValueError
        return helpers.csv_valid_rows(csvr)

    def get_pkey_list(self) -> list:
        pkey = self.DB_pkey
        out: list = []
        for row in self.DB:
            val = row.get(pkey, None)
            if out is not None:
                out.append(val)
        return out

    def get_table(self) -> list:
        out = []
        for row in self.DB:
            out.append(row)
        return out

    def get_row_by_pkey(self, pkey: str) -> Union[dict, None]:
        pkey_name = self.DB_pkey
        for row in self.DB:
            val = row.get(pkey_name, None)
            if val == str(pkey):
                return row
        return None

    def get_fkey(self, pkey: str, fkey_name: str) -> Union[str, None]:
        # pkey: field value of global primary key used by user
        # fkey: fieldname of primary key used in particular database
        row = self.get_row_by_pkey(pkey)
        if row is not None:
            return row.get(fkey_name, None)
        return None
