import os
from typing import Optional, Union


def is_file_readable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def str_join_no_empty(*args: str) -> str:
    non_empty_strings = [s for s in args if s]
    return "_".join(non_empty_strings)


def dict_get(dictr: dict, sections: list[str]) -> Union[dict, list, str, None]:
    dicw = dictr
    for i in sections:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict
