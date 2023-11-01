"""
This module contains package praivate helper functions.
"""

import csv
import dataclasses as dc
import datetime
from pathlib import Path
import os
import pkgutil
from io import StringIO
from typing import Any, Sequence, Union
from dateutil import parser
from rapi._model import Anotated


def current_timezone():
    """Get current timezone from host system."""
    return datetime.datetime.now().astimezone().tzinfo


def datenow_with_timezone():
    """
    Get current datetime with current timezone from host system.
    """


def parse_date_optional_fields(date_string: str):
    try:
        """
        Parses date string with optional date time precision.

        param: date string with optional increasing datetime precision defined in string e.g: 2023, 2023-09, 2023-09-10
        """
        pdate = parser.parse(date_string)
        if pdate.tzinfo is None:
            return pdate.astimezone()
        return pdate
    except Exception as e:
        raise ValueError(f"date not parsed. invalid date format: {e}")


def read_csv(file_name: str) -> csv.DictReader:
    path = os.path.abspath(file_name)
    with open(path, "r") as f:
        csv_reader = csv.DictReader(f.read(), delimiter=";")
    return csv_reader


def read_embedded_csv(file_path: Path, pakage_name: str) -> Union[csv.DictReader, None]:
    dbytes = pkgutil.get_data(pakage_name, str(file_path))
    if dbytes is not None:
        dtxt = dbytes.decode("utf-8")
        csvdata = StringIO(dtxt)
        csv_reader = csv.DictReader(csvdata, delimiter=";")
        return csv_reader
    return None


def csv_is_row_valid(row: dict) -> bool:
    """
    Check if csw row has all cells defined. i.e. no cell in row can be empty/undefined.
    """
    for _, cval in row.items():
        if cval == "":
            return False
    return True


def csv_valid_rows(csv: csv.DictReader) -> list:
    """Get valid csv rows."""
    out: list = []
    for row in csv:
        if csv_is_row_valid(row):
            out.append(row)
    return out


def str_join_no_empty(strings: Sequence[str], delim: str = "_") -> str:
    """
    Join the list of strings, omit empty strings.
    """
    non_empty_strings = [s for s in strings if s]
    return delim.join(non_empty_strings)


def dict_get_path(general_dictionary: dict, json_path: list[str]) -> Any:
    """
    Get path value in json-like object.
    Get subset of dictionary giving list of path or keyname
    """
    gd = general_dictionary
    for path in json_path:
        result = gd.get(path, None)
        if result is not None:
            gd = result
        else:
            return None
    return result


def json_value_parse(
    field_type: object,
    json_value: Any,
) -> Any:
    """
    Json fields parsers list.
    Parse json value according to ist type.
    """
    match field_type:
        case datetime.datetime:
            value = parse_date_optional_fields(json_value)
        case _:
            value = json_value
    return value


def class_attrs_by_anotation_dict(data: dict, entity: Anotated) -> object:
    """
    Parse JSON data fields specified in anotation to dataclass instance.

    :param data: FIXME
    :param entity: The model represented with dataclass.
    :returns: FIXME
    """
    fields = {field.name: field.type for field in dc.fields(entity)}  # type: ignore
    values: list = list()

    for field in fields:
        path = dict_get_path(entity.anotation, [field, "json"])
        if path is not None:
            json_value = dict_get_path(data, path.split("."))
            value = json_value_parse(fields[field], json_value)
        else:
            value = None
        values.append(value)

    return entity(*values)  # type: ignore


def class_attrs_by_anotation_list(data: list[dict], entity: Anotated) -> list[Any]:
    """
    Parse JSON data fields specified in anotation to list of dataclasses instances.

    :param data: FIXME
    :param entity: The model represented with dataclass.
    :returns: FIXME
    """
    result: list[Any] = []

    for item in data:
        result = result + [class_attrs_by_anotation_dict(item, entity)]

    return result
