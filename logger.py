#!/usr/bin/env python3
import logging

LOGGER_NAME = 'fartberry'
LOG_FILENAME = 'fartberry.log'
LOG_FORMAT = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

print_handler = logging.StreamHandler()
print_formatter = logging.Formatter(LOG_FORMAT + '\n')
print_handler.setFormatter(print_formatter)
print_handler.setLevel(logging.INFO)
logger.addHandler(print_handler)

file_handler = logging.FileHandler(LOG_FILENAME)
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
