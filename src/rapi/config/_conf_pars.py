from rapi.config._conf_vars import flag_places
import argparse as AP
import sys
from rapi.helpers import helpers

def parse_config_dict(config_dict: dict)->AP.ArgumentParser:
    argp = AP.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    cdict=config_dict
    citems=cdict.items()
    for flag,receipt in citems:
        if not isinstance(receipt,list):
            continue
        if len(receipt) != 5:
            continue
        add_parameter(argp,flag,receipt)
    return argp

def add_parameter(argp: AP.ArgumentParser, keyname: str, receipt: list[str])->AP.ArgumentParser:
    # value=flag_places['value_default']
    shortname=receipt[flag_places['shortname']]
    action=receipt[flag_places['action']]
    help=receipt[flag_places['help']]
    argp.add_argument(
            shortname,
            "--"+keyname,
            required=False,
            action=action,
            help=help,
            )
    return argp

def params_vars_cfg_intersec(dcfg: dict, pars: dict) -> dict:
    paths = helpers.dict_paths_vectors(dcfg, list())
    dictr: dict = {}
    for p in paths:
        val = pars.get("_".join(p))
        if val is not None:
            helpers.dict_create_path(dictr, p, val)
    return dictr

# ArgumentParser(prog='pytest', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)
class Cfg_params:
    def __init__(self,config_dict: dict):
        launcher = helpers.filepath_to_vector(sys.argv[0])[-1]
        sysargbak = sys.argv
        match launcher:
            case "rapi":
                pass
            case _:
                # e.g. "ipykernel_launcher.py"
                sys.argv = ["rapi"]
            # NOTE: calling from playbook sys.argv is set to some bullshit ['/home/user/rapi/.venv/lib/python3.11/site-packages/ipykernel_launcher.py', '-f', '/home/user/.local/share/jupyter/runtime/kernel-d916e01b-a4eb-42eb-998a-ec7eeb156cff.json'] so commandline args cannot be properly defined/parsed
        try:
            argsparser = parse_config_dict(config_dict)
            params_namespace=argsparser.parse_args()
        except SystemExit as e:
            sys.exit(e.code)
        except BaseException as e:
            raise ValueError(
                f"__name__={__name__}, __package__={__package__}, sys.argv={sys.argv}, launcher={launcher}, err: {e}"
            )
        sys.argv = sysargbak
        self.cfg = params_vars_cfg_intersec(
                config_dict,
                vars(params_namespace),
        )
