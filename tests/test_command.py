import pytest, os, sys, argparse
import unittest
import tempfile
from rapi import params
from rapi import command

import logging
logo=logging.getLogger("log_stdout")
loge=logging.getLogger("log_stderr")

def test_version():
    sys.argv=['test3.py','--version']
    pars=params.args_read()
    command.command(pars)
    logo.warning("helo")

def test_test_logs():
    sys.argv=['test3.py','--test-logs']
    pars=params.args_read()
    command.command(pars)
