# coding: utf-8
import logging
import os
import coloredlogs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file_name = os.getenv('A170_LOG_FILE_NAME', 'a170.log')
log_file_name = log_file_name.format()
if log_file_name:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(log_file_name)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

coloredlogs_fmt = '%(asctime)s - %(levelname)s - %(message)s'
coloredlogs.install(level='DEBUG', logger=logger, fmt=coloredlogs_fmt)
