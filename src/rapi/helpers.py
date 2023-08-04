import csv
import json
import os
import pkgutil
from io import StringIO
from typing import Any, Optional, Sequence, Union

from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


def pprint(data: dict):
    data_formated = json.dumps(data, indent=2)
    print(data_formated)


def analyze(obj: Any):
    print(f"value: {obj}")
    print(f"type{type(obj)}")


### files
def read_csv_imported_to_ram(fname: str) -> Union[csv.DictReader, None]:
    dbytes = pkgutil.get_data(__name__, fname)
    if dbytes is not None:
        dtxt = dbytes.decode("utf-8")
        csvdata = StringIO(dtxt)
        csv_reader = csv.DictReader(csvdata, delimiter=";")
        return csv_reader
    return None


def read_csv_path_to_ram(fname: str) -> csv.DictReader:
    path = os.path.abspath(fname)
    logo.info("reading file {path}")
    with open(path, "r") as f:
        fdata = f.read()
    csv_reader = csv.DictReader(fdata, delimiter=";")
    return csv_reader


def read_csv_fspath_or_package_to_ram(
    fspath: str, pkgpath: str
) -> Union[csv.DictReader, None]:
    if fspath is None or fspath == "":
        csvreader = read_csv_imported_to_ram(pkgpath)
    else:
        csvreader = read_csv_path_to_ram(fspath)
    return csvreader


def is_file_readable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def str_join_no_empty(strings: Sequence[str], delim: str = "_") -> str:
    non_empty_strings = [s for s in strings if s]
    return delim.join(non_empty_strings)


### config from env
def env_var_get(key: str) -> Union[str, None]:
    return os.environ.get(key, None)


def get_first_not_none(path: list, cfg_srcs: list) -> Any:
    res = None
    for s in cfg_srcs:
        res = s.get(path)
        if res is not None:
            break
    return res


### dict_get_path: get subset of dictionary giving list of path or keyname
def dict_get_path(
    dictr: dict, sections: list[str]
) -> Union[dict, list, str, bool, int, None]:
    dicw = dictr
    for i in sections:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict


def dict_create_path(dictr: dict, key_path: list, val: str = "kek"):
    n = 0
    for level in key_path:
        n = n + 1
        if level and len(key_path) > n:
            dictr = dictr.setdefault(level, dict())
        else:
            dictr = dictr.setdefault(level, val)


def dict_paths_vectors(
    dictr: dict, p_list: list = [], c_vec: list = []
) -> list:
    for key, val in dictr.items():
        if isinstance(val, dict):
            cv = c_vec.copy()
            cv.append(key)
            p_list = dict_paths_vectors(val, p_list, cv)
        else:
            p_list.append([])
            pi = len(p_list) - 1
            if len(c_vec) > 0:
                p_list[pi] = p_list[pi] + c_vec
            p_list[pi].append(key)
    return p_list


def deep_merge_dicts(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge_dicts(value, node)
        else:
            destination[key] = value
    return destination
