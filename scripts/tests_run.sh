#!/bin/bash
# pytest --capture=tee-sys tests/test_command.py 
# pytest tests/test_command.py
pytest --capture=tee-sys tests/test_config.py::test_var_from_env
# pytest --capture=tee-sys tests/test_config.py::test_var_from_cfg
# pytest --capture=tee-sys tests/test_config.py::test_get_var



