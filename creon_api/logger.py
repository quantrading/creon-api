import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from . import utils
from .config import LOG_PATH

utils.make_dir(LOG_PATH)
LOG_FILE_PATH = f"{LOG_PATH}/{datetime.now().date()}.log"
DEFAULT_LOG_FORMAT = "[%(asctime)s][%(levelname)s|%(filename)s:%(funcName)s:%(lineno)s] >> %(message)s"
file_max_byte = 1024 * 1024 * 100

logger = logging.getLogger('myLogger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=file_max_byte, backupCount=10, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
