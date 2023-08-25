import logging
import os
import sys

# default_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# default_format='%(asctime)s %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s'
default_format = "%(asctime)s [%(levelname)1s] %(filename)s:%(funcName)s:%(lineno)d - %(message)s - %(name)s"


### ShortenedLevelFormatter
#### modify format fields
class ShortenedLevelFormatter(logging.Formatter):
    def format(self, record):
        if record.levelname:
            ### shorten lelvel name to one letter
            record.levelname = record.levelname[0]
        return super().format(record)


### FILE LOGGER
#### NOTE: dir path must exist. Maybe use /tmp as default ?
# log_file = logging.getLogger("log_file")
# log_file.setLevel(logging.DEBUG)
# debug_handler = logging.FileHandler("./runtime/debug.log")
# debug_formatter = logging.Formatter(default_format)
# debug_handler.setFormatter(debug_formatter)
# log_file.addHandler(debug_handler)

### STDOUT LOGGER
log_stdout = logging.getLogger("log_stdout")
log_stdout.setLevel(logging.INFO)
info_handler = logging.StreamHandler(sys.stdout)
info_formatter = logging.Formatter(default_format)
# info_formatter = ShortenedLevelFormatter(default_format)
info_handler.setFormatter(info_formatter)
log_stdout.addHandler(info_handler)

### STDERR LOGGER
log_stderr = logging.getLogger("log_stderr")
log_stderr.setLevel(logging.ERROR)
error_handler = logging.StreamHandler()
error_formatter = logging.Formatter(default_format)
error_handler.setFormatter(error_formatter)
log_stderr.addHandler(error_handler)

### Log some messages
# log_file.debug('Debug message')
# log_stdout.info('Info message')
# log_stdout.warning('warning message')
# log_stderr.error('Error message')