from string_constants_util import StringConstantUtil
from logging.handlers import RotatingFileHandler
import logging


# Author: Harsha Gangavarapu
# Description: Logger Config
def setup_logger(name):
    # initialize logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File logging handler
    max_bytes_512_mb = 512 * 1024 * 1024
    file_handler = RotatingFileHandler(StringConstantUtil.LOG_FILE_NAME_PATH, maxBytes=max_bytes_512_mb, backupCount=2)
    file_handler.setLevel(logging.DEBUG)

    # console stream logging handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Formatter to log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S %Z')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # register handler
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
