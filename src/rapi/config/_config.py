import copy
import pkgutil
import sys
from typing import Any
from typing import Union

import yaml as yaml

from rapi.config import _params
from rapi.helpers import _logger
from rapi.helpers import helpers as helpers
from rapi.helpers._logger import log_stderr as loge

# from mergedeep import merge

__all__ = ["Config", "Cfg_default"]


# dict_get_path: get subset of dictionary giving list of path or keyname
def dict_get_path(
    dictr: dict, path: list[str]
) -> Union[dict, list, str, None]:
    dicw = dictr
    for i in path:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict


def config_yaml_defaults(pkg_name: str = __package__) -> dict:
    dats = pkgutil.get_data(pkg_name, "data/defaults.yml")
    if dats is None:
        raise LookupError("cannot read default config")
        # cfg=yaml.load(dats,Loader=yaml.FullLoader)
    config_dict = yaml.load(dats, Loader=yaml.SafeLoader)
    if config_dict is None:
        raise LookupError("cannot parse default config")
    return config_dict


class Cfg_default:
    def __init__(self, pkg_name: str = __package__):
        self.cfg = config_yaml_defaults(pkg_name)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


# config from user provided file
def config_yaml_file(file: str) -> dict:
    try:
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            return data
    except Exception:
        loge.debug("user config file not read")
        return {}


class Cfg_file:
    def __init__(self, file: str):
        self.cfg = config_yaml_file(file)
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


#### Try to find env var predefined in input dictionary. The env var name is constructed from joined dictionary path
def env_vars_dict_intersec(dcfg: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg, list())
    dictr: dict = {}
    for p in paths:
        val = helpers.env_var_get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr


class Cfg_env:
    # NOTE: maybe use alt method when using runtime_cfg_set:
    # traverse the default config constructing path vectors along the way, then try using the vector and concatenated vector to get value i.e. Cfg_?.get_path_value(vec,cvec) if not None skip trying the remaining Cfg_? sources. Then construct the particular cfg dict from path or incorporate the value to default cfg.
    # (This would eliminate traversing default cfg each time.)
    # or maybe use dict.update(odict)
    # maybe crreate package config/env.py, config/file.py, cofig/cfg.py
    def __init__(self, pkg_name: str = __package__):
        cfg = config_yaml_defaults(pkg_name)
        if cfg is not None:
            self.cfg = env_vars_dict_intersec(cfg)
        else:
            self.cfg = {}
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


def params_vars_cfg_intersec(dcfg: dict, pars: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg, list())
    dictr: dict = {}
    for p in paths:
        val = pars.get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr


# ArgumentParser(prog='pytest', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)
class Cfg_params:
    def __init__(self, pkg_name: str = __package__):
        argpars = _params.params_yml_config(pkg_name)
        launcher = helpers.filepath_to_vector(sys.argv[0])[-1]
        sysargbak = sys.argv
        match launcher:
            case "rapi":
                pass
            case _:
                # e.g. "ipykernel_launcher.py"
                sys.argv = ["rapi"]
            # NOTE: calling from playbook sys.argv is set to some bullshit ['/home/user/rapi/.venv/lib/python3.11/site-packages/ipykernel_launcher.py', '-f', '/home/user/.local/share/jupyter/runtime/kernel-d916e01b-a4eb-42eb-998a-ec7eeb156cff.json'] so commandline args cannot be properly defined/parsed
        try:
            params_namespace = argpars.parse_args()
        except BaseException as e:
            raise ValueError(
                f"__name__={__name__}, __package__={__package__}, sys.argv={sys.argv}, launcher={launcher}, err: {e}"
            )
        sys.argv = sysargbak
        self.params = vars(params_namespace)
        self.cfg = params_vars_cfg_intersec(
            config_yaml_defaults(pkg_name),
            self.params,
        )
        self.get = lambda path, dictr=self.cfg: dict_get_path(dictr, path)


class Config:
    def __init__(self, pkg_name: str = __package__) -> None:
        self.pkg_name = pkg_name
        self.cfg_default = Cfg_default(pkg_name)
        self.cfg_sources: list | None = None
        self.cfg_runtime: dict | None = None

    def cfg_runtime_set_defaults(self):
        cfgp = Cfg_params(self.pkg_name)
        cfge = Cfg_env(self.pkg_name)
        path = ["cfg", "file"]
        cfgd = Cfg_default(self.pkg_name)
        cfg_fname = helpers.get_first_not_none(path, [cfgp, cfge, cfgd])
        cfgf = None
        if cfg_fname is not None:
            cfgf = Cfg_file(cfg_fname)
        self.add_sources([cfgp, cfge, cfgf])
        self.cfg_runtime_set()
        # set log level
        _logger.set_level(self.runtime_get(["verbose"]))

    def add_sources(self, cfg_sources: list[Any]) -> None:
        # NOTE: maybe add check if type implements interface method get or has dict
        # sources:list=[]
        if self.cfg_sources is None:
            self.cfg_sources = list()
        for s in cfg_sources:
            if s is not None:
                self.cfg_sources.append(s)

    def cfg_runtime_set(self) -> None:
        srcs = self.cfg_sources
        res: dict = {}
        # merge in all sources in order of increasing priority
        if srcs is None or len(srcs) == 0:
            self.cfg_runtime = self.cfg_default.cfg
        else:
            for s in reversed(srcs):
                tmps = copy.deepcopy(s.cfg)
                res = helpers.deep_merge_dicts(tmps, res)
        # finaly merge with defaults.yml which should contain full set of variables
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
