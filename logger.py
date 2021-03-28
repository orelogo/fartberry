#!/usr/bin/env python3
import logging
from os import path

LOGGER_NAME = 'fartberry'
LOG_FORMAT = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

print_handler = logging.StreamHandler()
print_formatter = logging.Formatter(LOG_FORMAT + '\n')
print_handler.setFormatter(print_formatter)
print_handler.setLevel(logging.INFO)
logger.addHandler(print_handler)

abs_log_path = path.join(path.dirname(__file__), 'fartberry.log')
file_handler = logging.FileHandler(abs_log_path)
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
