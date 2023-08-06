import sys

from rapi.__main__ import main


def test_main():
    sys.argv = ["test3.py", "--version", "--test-par"]
    main()
