import csv
import errno
import json
import os
import pkgutil
import sys
from io import StringIO
from typing import Any, Optional, Sequence, Tuple, Type, Union

import numpy as np
import requests
import yaml

from rapi.logger import log_stdout as loge
from rapi.logger import log_stdout as logo


### printers
def pl(data: Any):
    logo.info(data)


def pp(data: Any):
    data_formated = json.dumps(data, indent=2)
    print(data_formated)


def pt(obj: Any):
    print(f"type{type(obj)}")


def pdict(obj: Any):
    pp(obj.__dict__)


def pdir(obj: Any):
    pp(dir(obj))


def an(obj: Any):
    print(f"value: {obj}")
    print(f"type{type(obj)}")


def type_by_name(type_name):
    type_map = {
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
    }

    if type_name in type_map:
        return type_map[type_name]
    else:
        raise NameError(f"{type_name} not implemented")


### csv files
def read_csv_imported_to_ram(fname: str) -> Union[csv.DictReader, None]:
    dbytes = pkgutil.get_data(__name__, fname)
    if dbytes is not None:
        dtxt = dbytes.decode("utf-8")
        csvdata = StringIO(dtxt)
        # reader = csv.reader(f)
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


def csv_is_row_valid(row: dict) -> bool:
    for ckey, cval in row.items():
        if cval == "":
            return False
    return True


def csv_valid_rows(csv: csv.DictReader) -> list:
    out: list = []
    for row in csv:
        if csv_is_row_valid(row):
            out.append(row)
    return out


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


### dict helpers
#### dict_get_path: get subset of dictionary giving list of path or keyname
def dict_get_path(
    dictr: dict,
    sections: list[str]
    # ) -> Union[dict, list, str, bool, int, None]:
) -> Any:
    dicw = dictr
    for i in sections:
        resdict = dicw.get(i, None)
        if resdict is None:
            return resdict
        else:
            dicw = resdict
    return resdict


def class_assign_attrs_fieldnum(
    cls: Any, data: dict, fields: list[int], paths: list[list[str]]
):
    j = 0
    for i in cls.__dict__:
        path = paths[fields[j]]
        cls.__dict__[i] = dict_get_path(data, path)
        j = j + 1
    return cls


def class_assign_attrs_fieldname(
    cls: Any, data: dict, fields: list[int], paths: list[str]
):
    pass


def dict_create_path(dictr: dict, key_path: list, val: str = "kek"):
    n = 0
    for level in key_path:
        n = n + 1
        if level and len(key_path) > n:
            dictr = dictr.setdefault(level, dict())
        else:
            dictr = dictr.setdefault(level, val)


def dict_paths_vectors(dictr: dict, p_list: list, c_vec: list = []) -> list:
    plist = p_list
    for key, val in dictr.items():
        if isinstance(val, dict):
            cv = c_vec.copy()
            cv.append(key)
            p_list = dict_paths_vectors(val, plist, cv)
        else:
            p_list.append([])
            pi = len(plist) - 1
            if len(c_vec) > 0:
                plist[pi] = plist[pi] + c_vec
            plist[pi].append(key)
    return plist


def dict_paths_to_strings(lst: list) -> list:
    out: list = []
    for p in lst:
        stro = ".".join(p)
        out.append(stro)
    return out


def deep_merge_dicts(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge_dicts(value, node)
        else:
            destination[key] = value
    return destination


### http request
def request_url(url: str) -> Union[requests.models.Response, None]:
    # headers = {}
    # params = {}
    # response = requests.get(url, headers=headers, params=params)
    try:
        ### download url data
        logo.info(f"requesting url: {url}")
        response = requests.get(url)
    except requests.exceptions.HTTPError as errh:
        loge.error(errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        loge.error(f"Connection Error: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        loge.error(f"Timeout Error:{errt}")
        return None
    except requests.exceptions.RequestException as err:
        loge.error(f"unknow exception:{err}")
        return None
    response.raise_for_status()
    return response


def request_url_json(url: str) -> Union[dict, None]:
    response = request_url(url)
    # json_data = json.loads(response.text)
    if response is None:
        return None
    if response.content is None:
        return None
    jdata = response.json()
    if jdata is None:
        loge.warning(f"no json data to parse: {url}")
        return None
    if len(jdata) == 0:
        logo.info("no data to parse: {endp}")
    return jdata


def request_url_yaml(url: str) -> Union[dict, None]:
    response = request_url(url)
    if response is None:
        return None
    if response.content is None:
        return None
    ydata = yaml.safe_load(response.content)
    if ydata is None:
        loge.warning(f"no yml data to parse: {url}")
        return None
    if len(ydata) == 0:
        logo.info("no data to parse: {url}")
    return ydata


def dict_to_dataclass(dictr: dict, model: Type):
    pass


def dict_to_row(dictr: dict, sections: list) -> list:
    row: list = []
    for s in sections:
        row.append(dict_get_path(dictr, s))
    return row


# Convert list of dictionaries to a NumPy array
# array_data = np.array([(d['name'], d['age'], d['city']) for d in data], dtype=[('name', 'U10'), ('age', int), ('city', 'U20')])


def dict_list_to_rows(
    lstarr: list[dict], check_type: Union[Any, None] = None
) -> Tuple[list, list]:
    logo.info("converting")
    paths = dict_paths_vectors(lstarr[0], list())
    header = dict_paths_to_strings(paths)
    rows: list = []
    for l in lstarr:
        row = dict_to_row(l, paths)
        rows.append(row)
    return rows, header


def rows_transpose(rows: list, header: list = []) -> list:
    if len(header) > 0:
        data = [header] + rows
    else:
        data = rows
    cols: list = []
    for c in range(len(data[0])):
        row = list()
        for i in range(len(data)):
            row.append(data[i][c])
        cols.append(row)
    return cols


def mkdir_parent_panic(path: str):
    if os.path.exists(path):
        if os.path.isdir(path):
            return
        else:
            loge.error(
                f"path already exists and it is not a directory: '{path}'"
            )
            sys.exit(1)
    try:
        os.makedirs(path, exist_ok=True)
        logo.info(f"Created '{path}'")
    except OSError as e:
        loge.error(f"Error creating directory '{path}': {e}")
        sys.exit(1)


def save_yaml(path: str, filename: str, data: dict) -> bool:
    try:
        file_path = os.path.join(path, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf8") as file:
            yaml.dump(data, file)
    except OSError as e:
        if e.errno != errno.EEXIST:
            loge.error("error saving the file: {file_path}", e)
            return False
        print("file exits")
    except IOError as e:
        loge.error("error saving the file: {file_path}, ", e)
        return False

    except Exception as e:
        loge.error("error saving the file: {file_path}, ", e)
        return False
    finally:
        logo.info(f"data saved to: {file_path}")
        return True


def save_json(path: str, filename: str, data: dict) -> bool:
    try:
        file_path = os.path.join(path, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf8") as file:
            yaml.dump(data, file)
    except OSError as e:
        if e.errno != errno.EEXIST:
            loge.error("error saving the file: {file_path}", e)
            return False
        print("file exits")
    except IOError as e:
        loge.error("error saving the file: {file_path}, ", e)
        return False

    except Exception as e:
        loge.error("error saving the file: {file_path}, ", e)
        return False
    finally:
        logo.info(f"data saved to: {file_path}")
        return True


def save_txt_data(file_path: str, data: str):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf8") as file:
            file.write(data)
        logo.info("data saved to:", file_path)

    except OSError as e:
        if e.errno != errno.EEXIST:
            loge.error("error saving the file:", e)

    except IOError as e:
        loge.error("error saving the file:", e)

    except Exception as e:
        loge.error("unknown error", e)


# ystr=yaml.dump(data,allow_unicode=True)


def save_rows_to_csv(fname: str, rows: list, header: list = []):
    # with open(fname, "w", newline="") as file:
    with open(fname, mode="a", newline="") as file:
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer = csv.writer(file)
        if len(header) > 0:
            writer.writerow(header)  # Writing header
        writer.writerows(rows)
