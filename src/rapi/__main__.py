import os

from rapi import CFG, Client
from rapi._command import commands

__all__ = "main"


def main() -> None:
    Cfg = CFG()
    Cfg.cfg_runtime_set_defaults()
    commands(Cfg)


if __name__ == "__main__":
    main()
