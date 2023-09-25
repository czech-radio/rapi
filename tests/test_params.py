import argparse as AP
import sys

import pytest

from rapi.config._config import _params


@pytest.mark.params
def test_params_yml_config() -> None:
    sys.argv = ["rapi", "-vv"]
    argp = _params.params_yml_config()
    pars = argp.parse_args()
    print(pars)
