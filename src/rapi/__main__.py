import os

from rapi import command, config, helpers, params


def main() -> None:
    Cfg = config.CFG()
    os.environ["test_env"] = "env"
    ### initialize cfg sources
    cfgp = config.Cfg_params()
    cfge = config.Cfg_env()
    cfgd = config.Cfg_default()
    ### print current version of program
    if cfgp.cfg.get("version"):
        print(config.__version__)
        return
    ### set user specified config file
    path = ["usercfg", "file"]
    cfg_fname = helpers.get_first_not_none(path, [cfgp, cfge, cfgd])
    if cfg_fname is not None:
        cfgf = config.Cfg_file(cfg_fname)
    else:
        cfgf = None
    # Cfg.add_sources([cfge, cfgp, cfgf])
    Cfg.add_sources([cfgp, cfge, cfgf])
    Cfg.cfg_runtime_set()
    command.command(Cfg, cfgp.pars)


if __name__ == "__main__":
    main()
