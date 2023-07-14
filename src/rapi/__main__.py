import os, sys
from .logger import log_stdout as logo
from .logger import log_stderr as loge

from . import stations
from . import params
from .__init__ import __version__
from . import swagger

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
        swagger.SwaggerDownload(pars.swagger_download)
        sys.exit(0)
    if pars.swagger_parse:
        logo.info(f"parsing swagger file: {pars.swagger_parse}")
        swagger.SwaggerParse(pars.swagger_parse)
        sys.exit(0)
    if pars.station:
        logo.info(f"requesting stations: {pars.station}")
        st=stations.stations(pars)
        # st.params_debug()
        st.GetStations()
        sys.exit(0)

if __name__ == "__main__":
    main()
