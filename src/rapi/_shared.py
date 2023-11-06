"""
This module contains package various private functions or classes shared accross package.
"""

import csv
import dataclasses as dc
import datetime
import logging
import pkgutil
import sys
from io import StringIO
from pathlib import Path
from typing import Any, Sequence, Mapping

from dateutil import parser

from rapi._domain import Anotated


def parse_date_optional_fields(date_string: str):
    """
    Parses a date string with optional date time precision.

    param date_string: The input date string e.g: '2023', '2023-09', '2023-09-10'.
    """
    parsed = parser.parse(date_string)
    result = parsed.astimezone() if parsed.tzinfo is None else parsed
    return result


def read_package_csv(file_path: Path, package_name: str) -> csv.DictReader:
    """
    :raises: ValueError: FIXME
    :raises: DecodingError: FIXME
    """
    data = pkgutil.get_data(package_name, str(file_path))
    if data is None:
        ValueError(f"Could open specified file {file_path}")
    reader = csv.DictReader(
        StringIO(data.decode("utf-8")),
        delimiter=";",
        quoting=csv.QUOTE_NONE,
    )
    return reader


def str_join_no_empty(strings: Sequence[str], delim: str = "_") -> str:
    """
    Join the list of strings, omit the empty strings.
    """
    non_empty_strings = [s for s in strings if s]
    return delim.join(non_empty_strings)


def json_value_parse(field_type: object, field_value: Any) -> Any:
    """
    Json fields parsers list.
    Parse json value according to ist type.
    """
    match field_type:
        case datetime.datetime:
            value = parse_date_optional_fields(field_value)
        case _:
            value = field_value
    return value


def deep_get(data: Mapping[Any, Any], *keys: str, default=None) -> Any:
    """
    Get the value from nested dictionaries.
    """
    assert len(keys) > 0  # debugging
    for key in keys:
        data = data.get(key, None)
        if data is None:
            break
    return data or default


# FIXME Rename, remove or move to dataclass itself.
def class_attrs_by_anotation_dict(data: dict, entity: Anotated) -> object:
    """
    Parse JSON data fields specified in anotation to dataclass instance.

    :param data: FIXME
    :param entity: The model represented with dataclass.
    :returns: FIXME
    """
    fields = {field.name: field.type for field in dc.fields(entity)}  # type: ignore
    values: list = []

    for field in fields:
        path = deep_get(entity.anotation, field, "json")
        if path is not None:
            json_value = deep_get(data, *path.split("."))
            value = json_value_parse(fields[field], json_value)
        else:
            value = None
        values.append(value)

    return entity(*values)  # type: ignore


# ######################################################################### #
#                                 LOGGING                                   #
# ########################################################################  #

DEFAULT_FORMAT = "%(asctime)s [%(levelname)1s] %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s"


class ShortenedLevelFormatter(logging.Formatter):
    """Shorten the log level to one letter."""

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
