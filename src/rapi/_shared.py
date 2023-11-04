"""
This module contains package various private functions or classes shared accross package.
"""

import csv
import dataclasses as dc
import datetime
import logging
import os
import pkgutil
import sys
from io import StringIO
from pathlib import Path
from typing import Any, Sequence

from dateutil import parser

from rapi._domain import Anotated

DEFAULT_FORMAT = "%(asctime)s [%(levelname)1s] %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s"


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
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file.read(), delimiter=";")
    return reader


def read_package_csv(file_path: Path, package_name: str) -> csv.DictReader:
    """
    :raises: ValueError: FIXME
    :raises: DecodingError: FIXME
    """
    data = pkgutil.get_data(package_name, str(file_path))
    if data is None:
        ValueError(f"Could open specified file {file_path}")
    reader = csv.DictReader(StringIO(data.decode("utf-8")), delimiter=";")
    return reader


def str_join_no_empty(strings: Sequence[str], delim: str = "_") -> str:
    """
    Join the list of strings, omit the empty strings.
    """
    non_empty_strings = [s for s in strings if s]
    return delim.join(non_empty_strings)


def extract_fields(data: dict, keys: list[str]) -> Any:
    """
    Get subset of dictionary  keys.
    """
    data: dict = data.copy()
    for key in keys:
        if result := data.get(key, None):
            data = result
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


class ShortenedLevelFormatter(logging.Formatter):
    """Shorten level name to one letter."""

    def format(self, record):
        if record.levelname:
            record.levelname = record.levelname[0]
        return super().format(record)


# Standard Output Logger Configuration
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.INFO)
info_handler = logging.StreamHandler(sys.stdout)
info_formatter = logging.Formatter(DEFAULT_FORMAT)
info_handler.setFormatter(info_formatter)
log_stdout.addHandler(info_handler)

# Standard Error Logger Configuration
log_stderr = logging.getLogger("log_stderr")
log_stderr.setLevel(logging.ERROR)
error_handler = logging.StreamHandler()
error_formatter = logging.Formatter(DEFAULT_FORMAT)
error_handler.setFormatter(error_formatter)
log_stderr.addHandler(error_handler)


def set_level(verbose_level: int = 0) -> None:
    # NOTE: The log level can be set also as:
    # log = logging.getLogger("log_stdout")
    # log.setLevel(logging.DEBUG)
    levels = [
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    level = levels[min(verbose_level, len(levels) - 1)]
    log_stderr.setLevel(level)
    log_stdout.setLevel(level)


def current_timezone():
    """Get current timezone from host system."""
    return datetime.datetime.now().astimezone().tzinfo


if __name__ == "__main__":
    log_stdout.debug("test debug")
    log_stdout.info("test info")
    log_stdout.warning("test warning")
    log_stderr.error("test error")
