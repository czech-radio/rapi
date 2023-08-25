import sys

from rapi import _config, _helpers, _model, _params
from rapi._station_ids import StationIDs

### test setup
Cfg = _config.CFG()
sys.argv = [
    "test3.py",
    "-vv",
]
cfgp = _config.Cfg_params()
cfge = _config.Cfg_env()
cfgf = _config.Cfg_file("./tests/data/defaults_alt.yml")
Cfg.add_sources([cfge, cfgp, cfgf])
Cfg.cfg_runtime_set()
Sids = StationIDs(Cfg)


def test_get_pkey_list() -> None:
    print()
    pkeys = Sids.get_pkey_list()
    assert pkeys
    _helpers.pp(pkeys)


def test_get_table() -> None:
    print()
    table = Sids.get_table()
    assert table
    _helpers.pp(table)


def test_get_row_by_pkey() -> None:
    print()
    fkeys = Sids.get_row_by_pkey(str(11))
    assert fkeys
    # print(fkeys)


def test_get_fkey() -> None:
    print()
    si = _model.StationIDs()
    sid = si.__dict__
    for k in sid:
        val = Sids.get_fkey("11", sid[k])
        assert val
        # print(val)
