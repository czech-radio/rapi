import os
from typing import Optional, Sequence, Union


def is_file_readable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def str_join_no_empty(strings: Sequence[str], delim: str = "_") -> str:
    non_empty_strings = [s for s in strings if s]
    return delim.join(non_empty_strings)


### config from env
def env_var_get(key: str) -> Union[str, None]:
    return os.environ.get(key, None)


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
