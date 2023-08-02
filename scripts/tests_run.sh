#!/bin/bash
declare -a pytestcmd=(
  "pytest"
  --capture=tee-sys
)
ptest="${pytestcmd[@]}"

### modules
$ptest tests/
# $ptest tests/test_command.py 
# $ptest tests/test_config.py 
# $ptest tests/test_helper.py

### config
# $ptest tests/test_config.py 
#### config.Cfg_?
# $ptest tests/test_config.py::test_Cfg_default
# $ptest tests/test_config.py::test_Cfg_file
# $ptest tests/test_config.py::test_Cfg_env
# $ptest tests/test_config.py::test_Cfg_params

#### config.CFG
# $ptest tests/test_config.py::test_CFG

#### helper
# $ptest tests/test_helper.py::test_dict_paths_vectors

