import logging
import sys

DEFAULT_FORMAT = "%(asctime)s [%(levelname)1s] %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s"


class ShortenedLevelFormatter(logging.Formatter):
    def format(self, record):
        if record.levelname:
            record.levelname = record.levelname[0]
        return super().format(record)


log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.INFO)
info_handler = logging.StreamHandler(sys.stdout)
info_formatter = logging.Formatter(DEFAULT_FORMAT)
info_handler.setFormatter(info_formatter)
log_stdout.addHandler(info_handler)

log_stderr = logging.getLogger("log_stderr")
log_stderr.setLevel(logging.ERROR)
error_handler = logging.StreamHandler()
error_formatter = logging.Formatter(DEFAULT_FORMAT)
error_handler.setFormatter(error_formatter)
log_stderr.addHandler(error_handler)
