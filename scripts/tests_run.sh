#!/bin/bash
### modules
# pytest --capture=tee-sys tests/test_command.py 
# pytest --capture=tee-sys tests/test_config.py 
# pytest --capture=tee-sys tests/test_helper.py

### config
# pytest --capture=tee-sys tests/test_config.py 

#### config.Cfg_?
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_default
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_file
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_env
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_params

#### config.CFG
pytest --capture=tee-sys tests/test_config.py::test_CFG


