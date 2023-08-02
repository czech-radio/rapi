import argparse
import os
import sys
from typing import Dict

from rapi import config


class HelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


# def args_read() -> Dict[str, any]:
def args_read() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-V",
        "--version",
        required=False,
        help="version of program",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="logging verbosity (-v for INFO, -vv for DEBUG)",
    )
    parser.add_argument(
        "--test-par",
        required=False,
        action="store_true",
        help="testing parameter",
    ),
    parser.add_argument(
        "--dummy",
        required=False,
        help="dummy run",
        action="store_true",
    ),
    parser.add_argument(
        "--cfg-file",
        required=False,
        type=str,
        help="specify config file",
    ),
    parser.add_argument(
        "--test-logs",
        required=False,
        help="testing logging",
        action="store_true",
    )
    parser.add_argument(
        "--swagger-download",
        required=False,
        nargs="?",
        type=str,
        help="download swagger openapi definition yaml file",
        const="https://rapidoc.croapp.cz/apifile/openapi.yaml",
    )
    parser.add_argument(
        "--swagger-parse",
        required=False,
        nargs="?",
        type=str,
        help="parse swagger openapi definition yaml file",
        const="./runtime/rapidev_croapp.yml",
    )
    parser.add_argument(
        "--broadcast",
        required=False,
        help="request station data",
        action="store_true",
    )
    ##TODO: DT:2023/07/17_13:37:47, LV:1
    ###SD: Add mutually exclusive command group
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-a', action='store_true')
    params = parser.parse_args()

    ### no parameter given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return params
