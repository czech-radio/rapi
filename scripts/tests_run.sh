#!/bin/bash
# pytest --capture=tee-sys tests/test_command.py 

### helper
pytest --capture=tee-sys tests/test_helper.py::test_dict_get

### config
# pytest --capture=tee-sys tests/test_config.py 
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_env
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_params
# pytest --capture=tee-sys tests/test_config.py::test_set_runtime_var
# pytest --capture=tee-sys tests/test_config.py::test_Cfg_default
# pytest tests/test_command.py
# pytest --capture=tee-sys tests/test_config.py::test_var_from_env
# pytest --capture=tee-sys tests/test_config.py::test_var_from_cfg
# pytest --capture=tee-sys tests/test_config.py::test_get_var
# pytest --capture=tee-sys tests/test_config.py::test_get_var
# pytest --capture=tee-sys tests/test_manifest.py
# ::test_manifest

# pytest --capture=tee-sys tests/test_import.py
# pytest --capture=tee-sys tests/test_config.py::



