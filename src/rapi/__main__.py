import os, sys
import logging
logo=logging.getLogger("log_stdout")
loge=logging.getLogger("log_stderr")

from . import broadcast
from . import params
from .__init__ import __version__
from . import swagger

def main():
    pars = params.args_read()
    if pars.version:
        print(__version__)
        sys.exit(0)
    if pars.verbose==0:
        loglevel=logging.WARN
    if pars.verbose == 1:
        loglevel=logging.INFO
    if pars.verbose == 2:
        loglevel=logging.DEBUG
    logo.setLevel(loglevel)
    loge.setLevel(loglevel)
    if pars.test_logs:
        print("log_out level",logo.level)
        print("log_err level",loge.level)
        logo.debug("debug_level")    
        logo.info("info_level")    
        logo.warn("warn_level")    
        loge.error("error_level")
        sys.exit(0)
    if pars.swagger_download:
        logo.info(f"downloading file: {pars.swagger_download}")
        swagger.SwaggerDownload(pars.swagger_download)
        sys.exit(0)
    if pars.swagger_parse:
        logo.info(f"parsing swagger file: {pars.swagger_parse}")
        swagger.SwaggerParse(pars.swagger_parse)
        sys.exit(0)
    if pars.broadcast:
        logo.info(f"requesting stations: {pars.broadcast}")
        st=broadcast.broadcast(pars)
        print(st.fields)
        sys.exit(0)

if __name__ == "__main__":
    main()
