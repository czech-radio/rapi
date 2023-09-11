import sys
from typing import Optional, Tuple, Type, TypeVar, Union

from rapi._logger import log_stderr as loge
from rapi._logger import log_stdout as logo


class DefaultException(Exception):
    err_code = 2

    def __init__(self, message: str):
        super().__init__(message)


class UnknownException(DefaultException):
    err_code = 3


class Err(Exception):
    def __init__(
        self,
        exctype: Union[Type[BaseException], None] = DefaultException,
        message: str = "",
    ):
        super().__init__(message)
        self.message = message
        if exctype is None:
            self.ok = True
            self.exctype = None
            self.err_code = 0
        else:
            self.ok = False
            self.exctype = exctype
            self.err_code = vars(exctype).get("err_code", 1)

    def add_msg(self, msg: str = ""):
        message = " ".join([self.message, msg])
        super().__init__(message)
        self.message = message

    def log(self, stacklevel: int = 2):
        if self.err_code == 0:
            logo.debug(self, stacklevel=stacklevel)
        else:
            loge.error(self, stacklevel=stacklevel)

    def exception_return(self, msg: str = ""):
        if self.exctype is None:
            return
        else:
            msgs = " ".join([self.message, msg])
            self.log(3)
            return self.exctype(msgs)

    def exception_raise(self, msg: str = ""):
        excp = self.exception_return(msg)
        if excp is not None:
            raise excp

    def panic_on_error(self):
        if self.err_code != 0:
            self.log(3)
            sys.exit(self.err_code)

    def exit(self):
        sys.exit(self.err_code)
