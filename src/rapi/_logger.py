import logging
import sys

# default_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# default_format='%(asctime)s %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s'
default_format = "%(asctime)s [%(levelname)1s] %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s"


class ShortenedLevelFormatter(logging.Formatter):
    """custom log formater"""

    def format(self, record):
        if record.levelname:
            # shorten level name to one letter
            record.levelname = record.levelname[0]
        return super().format(record)


# STDOUT LOGGER
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.INFO)
info_handler = logging.StreamHandler(sys.stdout)
info_formatter = logging.Formatter(default_format)
# info_formatter = ShortenedLevelFormatter(default_format)
info_handler.setFormatter(info_formatter)
log_stdout.addHandler(info_handler)

# STDERR LOGGER
log_stderr = logging.getLogger("log_stderr")
log_stderr.setLevel(logging.ERROR)
error_handler = logging.StreamHandler()
error_formatter = logging.Formatter(default_format)
error_handler.setFormatter(error_formatter)
log_stderr.addHandler(error_handler)


def set_level(verbose_level: int = 0) -> None:
    # NOTE: Log level of loggers can be set also with:
    # log=logging.getLogger("log_stdout")
    # log.setLevel(logging.DEBUG)
    levels = [
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    level = levels[min(verbose_level, len(levels) - 1)]
    # logging.basicConfig(level=level)
    log_stderr.setLevel(level)
    log_stdout.setLevel(level)


def test_logs() -> None:
    log_stdout.debug("this is debug_level message")
    log_stdout.info("Info message")
    log_stdout.warning("warning message")
    log_stderr.error("Error message")
