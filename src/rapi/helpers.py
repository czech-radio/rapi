import os


def is_file_readable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def str_join_no_empty(*args: str) -> str:
    non_empty_strings = [s for s in args if s]
    return "_".join(non_empty_strings)
