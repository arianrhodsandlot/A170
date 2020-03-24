# coding: utf-8
import os
import coloredlogs
import verboselogs
from logging.handlers import TimedRotatingFileHandler
from .config import LOG_DIRNAME, LOG_FILENAME

if not os.path.exists(LOG_DIRNAME):
    os.makedirs(LOG_DIRNAME)

log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
logger = verboselogs.VerboseLogger(__name__)


log_file_path = os.path.join(LOG_DIRNAME, LOG_FILENAME)
fh = TimedRotatingFileHandler(filename=log_file_path, when='h')
fh.setLevel(verboselogs.NOTICE)
formatter = verboselogs.logging.Formatter(fmt=log_fmt)
fh.setFormatter(formatter)
logger.addHandler(fh)

coloredlogs.install(level=verboselogs.SPAM, logger=logger, fmt=log_fmt)
