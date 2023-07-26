from . import command, params


def main() -> None:
    pars = params.args_read()
    command.command(pars)


if __name__ == "__main__":
    main()
