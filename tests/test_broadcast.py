import sys

from rapi import broadcast, config, helpers, model, params
from rapi.helpers import analyze as an
from rapi.helpers import pprint as pp

### test setup
Cfg = config.CFG()
sys.argv = [
    "test3.py",
    "--broadcast",
    "-vv",
    # "broadcast-st=10",
    # "--broadcast-station_ids_pkey=openmedia_id",
]
cfgp = config.Cfg_params()
cfge = config.Cfg_env()
cfgf = config.Cfg_file("./tests/data/defaults_alt.yml")
Cfg.add_sources([cfge, cfgp, cfgf])
Cfg.cfg_runtime_set()
BC = broadcast.Broadcast(Cfg)


def test_Broadcast() -> None:
    pass
