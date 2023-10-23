import logging
import sys

default_format = "%(asctime)s [%(levelname)1s] %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s"


class ShortenedLevelFormatter(logging.Formatter):
    """Shorten level name to one letter."""

    def format(self, record):
        if record.levelname:
            record.levelname = record.levelname[0]
        return super().format(record)


# Standard Output Logger Configuration
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.INFO)
info_handler = logging.StreamHandler(sys.stdout)
info_formatter = logging.Formatter(default_format)
info_handler.setFormatter(info_formatter)
log_stdout.addHandler(info_handler)

# Standard Error Logger Configuration
log_stderr = logging.getLogger("log_stderr")
log_stderr.setLevel(logging.ERROR)
error_handler = logging.StreamHandler()
error_formatter = logging.Formatter(default_format)
error_handler.setFormatter(error_formatter)
log_stderr.addHandler(error_handler)


def set_level(verbose_level: int = 0) -> None:
    # NOTE: The log level can be set also as:
    # log = logging.getLogger("log_stdout")
    # log.setLevel(logging.DEBUG)
    levels = [
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    level = levels[min(verbose_level, len(levels) - 1)]
    log_stderr.setLevel(level)
    log_stdout.setLevel(level)


def test_logs() -> None:
    log_stdout.debug("this is debug_level message")
    log_stdout.info("Info message")
    log_stdout.warning("warning message")
    log_stderr.error("Error message")
