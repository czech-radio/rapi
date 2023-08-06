#!/bin/bash
declare -a pytestcmd=(
  "pytest"
  --capture=tee-sys
)
ptest="${pytestcmd[@]}"

### modules
# $ptest tests/
# $ptest tests/test_command.py 
# $ptest tests/test_config.py 
# $ptest tests/test_helper.py
# $ptest tests/test_main.py
# $ptest tests/test_broadcast.py

### config
# $ptest tests/test_config.py 
#### config.Cfg_?
# $ptest tests/test_config.py::test_Cfg_default
# $ptest tests/test_config.py::test_Cfg_file
# $ptest tests/test_config.py::test_Cfg_env
# $ptest tests/test_config.py::test_Cfg_params

#### config.CFG
# $ptest tests/test_config.py::test_CFG

### broadcast
par="tests/test_broadcast.py"
# $ptest $par

### stationIDs
par="tests/test_station_ids.py"
# $ptest "${par}::test_get_pkey_list"
# $ptest "${par}::test_get_table"
# $ptest "${par}::test_get_row_by_pkey"
# $ptest "${par}::test_get_fkey"

#### helper
par="tests/test_helpers.py"
# $ptest $par
# $ptest ${par}::test_request_url
# $ptest ${par}::test_request_url_json
# $ptest ${par}::test_request_url_yaml
# $ptest ${par}::test_json_to_csv
$ptest ${par}::test_dict_list_to_rows

