# Config: one config to rull them all

## PURPOSE
- There are many ways how to modify program variables:
commandline parameters, environmental variables, user config files, or python dictionaries created at runtime. 

- The relevant environmental variables must be parsed in source code with os.getenv or with os.environ.items(). List of relevant env vars must be somewhere. One file for use second in source code.

- The parameters must defined in source code, with argparse:

    ```python
    parser.add_argument(
        "-s", "--stations", required=True, help="The station for the schedule."
    )
    ```

Programmer has to then somehow establish the source priority of variable value.

I think that it is convenient to have definition of: default variables, relevant environment variables, commadline parameters, user modifiable variables, recipe for creating the program and documentation in one file. Further layers can be added using yaml comments. For example docker-compose.yml (not implemented).

## CONFIG SOURES

- commandline parameters:

    ```shell
    rapi --debug-cfg 
    ```

- environmental variables:

    - shell 

	```shell
	printenv
    export <varname>=<value>
    printenv <varname>
    export debug_cfg=True
    ```

    - powershell

    ```powershell
    $Env
    $Env:<varname> = "<value>"
    $Env:<varname>
    $Env:debug_cfg=True
    ```

- default configuration file default.yml:

    ```
    debug:
      cfg: true  # -dc; bool; store_true; debug runtime
    not_a_par: "hello_world"
    commands:
      stations:
        station_id: # -si; int; store; filter station by id
    ```
   
   The comment following inline '#' is recipe how to parse variable as parameter. The comment has to have 4 fields delimited by ';':

    1. field must be unique shorthend
    2. field is variable type
    3. field is parameter type: 'store' means that the parameter must have value. e.g. rapi --test-par="hello". 'store_true' means that the parameter does not tak any value. (same meaning as in argparse) 
    4. field is help string

    All such defined parameters can be also displayed with '-h' switch. Without valid comment the corresponding parameter will not be created. The value of variable can be then modified only by environment or by user config file if desired. 

    commands: is a special secstion. It serves as recipe how to create program subcommands.

- user config.yml:
can be any subset of default.yml. User cannot create, set any other variables or subcommands not explicitly given by default.yml.

    ```
    debug:
      cfg: true
    not_a_par: "world_hello"

## USAGE
### default usage
- cfg_runtime_set_defaults() will load following sources of variables and merge them in with dictionary constructed from defaults.yml in order of decreasing priority:

    1. commandline parameters 
    2. environmental variables
    3. user specified config file


    ```python
    Cfg = config.CFG()
    Cfg.cfg_runtime_set_defaults()
    varname=Cfg.runtime_get(["debug","cfg"])
    ```

### usage with selected variables sources with specified priority 

    ```
    Cfg = config.CFG()
    cfgp = config.Cfg_params()               # load commandline parameters given by user
    cfge = config.Cfg_env()                  # load env variables
    cfgf = config.Cfg_file("./user_cfg.yml") # load variables from user defined/modified file containing subset of defaults.yml
    cfgd: dict={}                            # specify subset dictionary of defaults.yml
    Cfg.add_sources([cfgp,cfge,cfgd])        # specify the source priority (in order of decreasing priority:
                                             # if first source does not have variable defined
                                             # the value from next source will be taken)
    Cfg.cfg_runtime_set()
    varname=Cfg.runtime_get(["debug","cfg"])
    ```

## DEVELOPEMENT NOTES

- given in ./rapi/src/rapi/params.py

  

    
    

