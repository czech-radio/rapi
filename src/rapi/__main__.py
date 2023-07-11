import os
import sys
from .__init__ import __version__
from .logger import log_stdout as logo
from .logger import log_stderr as loge

def main():
    logo.info("kek")    
    loge.error("jek")

if __name__ == "__main__":
    main()
