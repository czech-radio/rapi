import argparse
import logging
import os
import sys
import tempfile
import time
import unittest

import pytest

from rapi import command, params

logt = logging.getLogger("log_test")
logt.setLevel(logging.INFO)


@pytest.fixture(autouse=True)
def print_test_name(request):
    test_name = request.node.name
    print("\n")
    logt.info(f"RUNNING TEST: {test_name}")

    def fin():
        logt.info("COMPLETED TEST '{}' \n".format(request.node.name))

    request.addfinalizer(fin)


def test_example():
    assert True


def test_version():
    sys.argv = ["test3.py", "--version"]
    # pars = params.args_read()
    # command.command(pars)


# def test_test_logs_lv1():
# sys.argv = ["test3.py", "--test-logs", "-v"]
# pars = params.args_read()
# command.command(pars)


# def test_test_logs_lv2():
# sys.argv = ["test3.py", "--test-logs", "-vv"]
# pars = params.args_read()
# command.command(pars)


# def test_test_logs_lv0():
# sys.argv = ["test3.py", "--test-logs"]
# pars = params.args_read()
# command.command(pars)
