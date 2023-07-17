import os, sys
import logging
from .logger import log_stdout as logo
from .logger import log_stdout as loge

from . import params
from . import command

def main():
    pars = params.args_read()
    command.command(pars)

if __name__ == "__main__":
    main()
