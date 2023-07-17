import pytest, os, sys, argparse
import unittest
import tempfile
import time
from rapi import params
from rapi import command

import logging
logt = logging.getLogger('log_test')
logt.setLevel(logging.INFO)
# from rapi.logger import log_stdout as logo
# from rapi.logger import log_stdout as loge

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
    sys.argv=['test3.py','--version']
    pars=params.args_read()
    command.command(pars)

def test_test_logs_lv1():
    sys.argv=['test3.py','--test-logs', '-v']
    pars=params.args_read()
    command.command(pars)

def test_test_logs_lv2():
    sys.argv=['test3.py','--test-logs', '-vv']
    pars=params.args_read()
    command.command(pars)

def test_test_logs_lv0():
    sys.argv=['test3.py','--test-logs']
    pars=params.args_read()
    command.command(pars)
