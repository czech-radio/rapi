# demarks position of variables
flag_places={
        "shortname": 0,
        "value_default": 1,
        "value_type": 2,
        "action": 3,
        "help": 4,
        }

flags_main={
        "verbose": ["-v", 0, "int", "count", "log level"],
        "version": ["-V", "false", "int", "store_true", "print version of program"],
        }

flags_debug={
        "debug_cfg": ["-dc","false","bool", "store_true", "debug runtime config"],
        }

flags_test={
        "test_par": ["-tp", "", "str", "store", "test par"],
        "test_env": ["-te", "", "str", "store", "test env"],
        "test_def": ["-td", "", "str", "store", "test def"],
        "test_alt": ["-ta", "", "str", "store", "test alt"],
        "test_cfg_prio": ["-tcp", "def_dict", "str", "store", "which source wins?"],
        }

subcommands={
        "station": [],
        "station_ids": [],
        }

configure_dict={
        **flags_main,
        **flags_debug,
        **flags_test,
        }
