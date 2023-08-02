import os

from rapi import command, config, params


def main() -> None:
    Cfg = config.CFG()
    # os.environ["test_env"]="env"
    cfge = config.Cfg_env()
    cfgp = config.Cfg_params()
    if cfgp.cfg.get("version"):
        print(config.__version__)
        return
    cfgf = config.Cfg_file("./tests/defaults_alt.yml")
    Cfg.add_sources([cfge, cfgp, cfgf])
    Cfg.cfg_runtime_set()
    # command.command(Cfg.cfg_runtime)
    command.command(Cfg)


if __name__ == "__main__":
    main()
