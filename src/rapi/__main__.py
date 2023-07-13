import os
import sys
from .logger import log_stdout as logo
from .logger import log_stderr as loge

from . import station
from . import params
from .__init__ import __version__
from . import swagger_parse as swp

def main():
    pars = params.args_read()
    if pars.version:
        print(__version__)
        sys.exit(0)
    if pars.test_logs:
        logo.info("kek")    
        loge.error("jek")
        sys.exit(0)
    if pars.swagger_download:
        logo.info(f"downloading file: {pars.swagger_download}")
        swp.DownloadApiDefinition()
        sys.exit(0)
    if pars.swagger_parse:



if __name__ == "__main__":
    main()
