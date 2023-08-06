import sys

from rapi import broadcast, config, helpers, model, params
from rapi.helpers import analyze as an
from rapi.helpers import pprint as pp
from rapi.station_ids import StationIDs

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
Sids = StationIDs(Cfg)


def test_get_pkey_list() -> None:
    print()
    pkeys = Sids.get_pkey_list()
    assert pkeys
    helpers.pprint(pkeys)


def test_get_table() -> None:
    print()
    table = Sids.get_table()
    assert table
    helpers.pprint(table)


def test_get_row_by_pkey() -> None:
    print()
    fkeys = Sids.get_row_by_pkey(str(11))
    assert fkeys
    # print(fkeys)


def test_get_fkey() -> None:
    print()
    si = model.station_ids()
    sid = si.__dict__
    for k in sid:
        val = Sids.get_fkey("11", sid[k])
        assert val
        # print(val)
