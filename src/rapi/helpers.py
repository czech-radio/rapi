import os
from typing import Optional, Sequence, Union


def is_file_readable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def str_join_no_empty(strings: Sequence[str], delim: str = "_") -> str:
    non_empty_strings = [s for s in strings if s]
    return delim.join(non_empty_strings)


def dict_get(dictr: dict, sections: list[str]) -> Union[dict, list, str, None]:
    dicw = dictr
    for i in sections:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict
