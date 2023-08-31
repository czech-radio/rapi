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
# $ptest tests/test_helpers.py
# $ptest tests/test_main.py
# $ptest tests/test_params.py
# $ptest tests/test_station_ids.py
# $ptest tests/test_broadcast.py

### params
par="tests/test_params.py"
# $ptest $par
# $ptest "${par}::test_parse_all"
# $ptest "${par}::test_params_yml_config"

### config
par="tests/test_config.py"
####
#### config.Cfg_?
# $ptest $par
# $ptest $par::test_config_yml_default
# $ptest $par::test_Cfg_default
# $ptest $par::test_Cfg_file
# $ptest $par::test_Cfg_env
# $ptest $par::test_Cfg_params
# $ptest tests/test_config.py::test_CFG
# $ptest tests/test_config.py::test_CFG_defaults

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
# $ptest $par::test_extract_link_path
# $ptest ${par}::test_request_url
# $ptest ${par}::test_request_url_json
# $ptest ${par}::test_request_url_yaml
# $ptest ${par}::test_json_to_csv
# $ptest ${par}::test_dict_list_to_rows


### client
par="tests/test_client.py"
# $ptest ${par}
# $ptest ${par}::test_DB_local
# $ptest ${par}::test_API
# $ptest ${par}::test_get_swagger
# $ptest ${par}::test_save_swagger
# $ptest ${par}::test_DB_local_endpoint_get_json
# $ptest ${par}::test_DB_local_endpoint_save_json
# $ptest ${par}::test_DB_local_endpoints_save_json
# $ptest ${par}::test_DB_local_csv_update
# $ptest ${par}::test_DB_local_endp_get_full_json

#### api_client_api
par="tests/test_client_api.py"
# $ptest ${par}
$ptest ${par}::test_get_station
# $ptest ${par}::test_get_station_shows
# $ptest ${par}::test_get_stations

### errors
par="tests/test_errors.py"
# $ptest $par
# $ptest $par::test_HelloErr
# $ptest $par::test_return_tuple
# $ptest $par::test_Err_None
# $ptest $par::test_Err
