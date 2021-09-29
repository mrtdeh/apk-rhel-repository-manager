import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from config.config import get_config
import os
import gzip
config_app = get_config()
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(lineno)s — %(message)s")
LOG_FILE = config_app["logger"]["log_dir"]
if LOG_FILE == ".":
    LOG_FILE = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "log_file")
LOG_LEVEL = {"DEBUG": logging.DEBUG, "INFO": logging.INFO,
             "WARNING": logging.WARNING, "ERROR": logging.ERROR,
             "CRITICAL": logging.CRITICAL}


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when='D',
        interval=config_app["logger"]["log_rotate_time_by_day"], backupCount=1)
    file_handler.setFormatter(FORMATTER)
    file_handler.rotator = GZipRotator()
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    log_level = LOG_LEVEL[config_app["logger"]["log_level"].upper()]
    logger.setLevel(log_level)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


class GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)
