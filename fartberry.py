#!/usr/bin/env python3
import signal
import sys
import time
from datetime import datetime
from os import path

from config import config
from database import database
from logger import logger
from pms_5003_sensor import pms_5003_sensor


def signal_handler(signal, frame):
    database.close()
    logger.info('Closing program')
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)  # handle ctrl-c

    while True:
        try:
            particulate_matter = pms_5003_sensor.get_particulate_matter()
            timestamp = datetime.now()
            logger.info(particulate_matter)
            database.insert(timestamp, particulate_matter)
        except Exception as e:
            logger.exception(e)

        time.sleep(config.polling_frequency_in_sec)


if __name__ == '__main__':
    main()
