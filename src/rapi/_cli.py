from rapi._command import commands
from rapi.config._config import Config


def main() -> None:
    Cfg = Config(__package__)
    Cfg.cfg_runtime_set_defaults()
    commands(Cfg)


if __name__ == "__main__":
    main()
