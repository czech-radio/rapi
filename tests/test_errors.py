import logging
import sys
from string import Template
from typing import Optional, Tuple, Type, TypeVar, Union

from rapi import _errors as err
from rapi import _helpers
from rapi._logger import log_stderr as loge
from rapi._logger import log_stdout as logo

loglevel = logging.DEBUG
logo.setLevel(loglevel)


def HelloErr(value: int) -> tuple[int, err.Err]:
    if value == 0:
        return 0 + 1, err.Err(None)
    else:
        return 0, err.Err(ValueError, "I can take only zero")


def test_HelloErr():
    val, err = HelloErr(1)
    print(val, err)
    if err.ok:
        logo.debug("everything ok")
    else:
        raise err.exception_return()


def test_Err_None():
    print()
    er = err.Err(None, "Everything went better than expected")
    er.exception_raise()
    er.panic_on_error()
    # er.exit()


def test_Err():
    er = err.Err(TypeError, "your type is invalid:")
    er.add_msg("blau")
    er.log()
    raise er.exception_return()
    # er.panic_on_error()
    # er.exit()
