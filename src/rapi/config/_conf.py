from rapi.config._conf_vars import configure_dict
from rapi.config._conf_pars import Cfg_params
from rapi.helpers import helpers
from rapi.helpers import _logger
from typing import Any
import copy
from rapi.helpers._logger import log_stderr as loge

# dict_get_path: get subset of dictionary giving list of path or keyname
def dict_get_path(
    dictr: dict, path: list[str]
) -> Any:
    dicw = dictr
    for i in path:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict

#### Try to find env var predefined in input dictionary. The env var name is constructed from joined dictionary path
def env_vars_dict_intersec(dcfg: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg, list())
    dictr: dict = {}
    for p in paths:
        val = helpers.env_var_get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr

class Cfg_default:
    def __init__(self,config_dict: dict=configure_dict):
        self.cfg = config_dict
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)

class Cfg_env:
    def __init__(self,config_dict: dict=configure_dict):
        if config_dict is not None:
            self.cfg = env_vars_dict_intersec(config_dict)
        else:
            self.cfg = {}
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)

class Config:
    def __init__(self, config_dict: dict=configure_dict) -> None:
        self.config_dict=config_dict
        self.cfg_default = Cfg_default()
        self.cfg_sources: list | None = None
        self.cfg_runtime: dict | None = None

    def add_sources(self, cfg_sources: list[Any]) -> None:
        if self.cfg_sources is None:
            self.cfg_sources = list()
        for s in cfg_sources:
            if s is not None:
                self.cfg_sources.append(s)

    def runtime_set_defaults(self):
        cfgd = Cfg_default(self.config_dict)
        cfge = Cfg_env(self.config_dict)
        cfgp = Cfg_params(self.config_dict)
        # path = ["cfg", "file"]
        # cfg_fname = helpers.get_first_not_none(path, [cfgp, cfge, cfgd])
        # cfgf = None
        # if cfg_fname is not None:
            # cfgf = Cfg_file(cfg_fname)
        # self.add_sources([cfgp, cfge, cfgf])
        self.add_sources([cfgp, cfge])
        self.runtime_set_vars()
        # set log level
        _logger.set_level(self.runtime_get(["verbose"]))
        loge.debug("user config file not read")

    def runtime_set_vars(self) -> None:
        srcs = self.cfg_sources
        res: dict = {}
        # merge in all sources in order of increasing priority
        if srcs is None or len(srcs) == 0:
            self.cfg_runtime = self.cfg_default.cfg
        else:
            for s in reversed(srcs):
                tmps = copy.deepcopy(s.cfg)
                res = helpers.deep_merge_dicts(tmps, res)
        # finaly merge with default config which should contain full set of variables
        res = helpers.deep_merge_dicts(res, self.cfg_default.cfg)
        self.cfg_runtime = res
        # set log level
        _logger.set_level(self.runtime_get(["verbose"]))

    def runtime_get(self, path: list, dvalue: Any = ValueError) -> Any:
        if self.cfg_runtime is None:
            raise LookupError("runtime config is not set")
        val = helpers.dict_get_path(self.cfg_runtime, path)
        if val is None:
            try:
                isexcp = isinstance(dvalue(), Exception)
            except Exception:
                return dvalue
            if isexcp:
                raise dvalue(f"cannot get path: {path}")
            else:
                return dvalue
        return val
