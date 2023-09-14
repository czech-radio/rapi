from rapi import Client, Config
from rapi._command import commands


def main() -> None:
    Cfg = Config()
    Cfg.cfg_runtime_set_defaults()
    commands(Cfg)


if __name__ == "__main__":
    main()
