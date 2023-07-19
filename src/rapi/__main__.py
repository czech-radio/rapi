import logging
import os
import sys

from . import command, params
from .logger import log_stdout as loge
from .logger import log_stdout as logo


def main():
    pars = params.args_read()
    command.command(pars)


if __name__ == "__main__":
    main()
