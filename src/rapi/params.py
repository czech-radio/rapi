import argparse
import os
import sys
from typing import Dict

from .logger import log_stdout as logo
from .logger import log_stderr as loge

class HelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()

def args_read() -> Dict[str, any]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-v",
            "--version",
            required=False,
            help="version of program",
            action="store_true",
            )

    parser.add_argument(
            "--test-logs",
            required=False,
            help="testing logging",
            action="store_true",
            )
    parser.add_argument(
            "--swagger-download",
            required=False,
            nargs='?', 
            type=str,
            help="download swagger openapi definition yaml file",
            const="https://rapidoc.croapp.cz/apifile/openapi.yaml",
            )
    parser.add_argument(
            "--swagger-parse",
            required=False,
            nargs='?', 
            type=str,
            help="parse swagger openapi definition yaml file",
            const=".runtime/rapidev_cropapp.yml",
            )
    params = parser.parse_args()

    ### no parameter given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return params


