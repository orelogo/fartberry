#!/usr/bin/env python3
import signal
import sys
import time
from datetime import datetime
from os import path

from fartberry.config import config
from fartberry.database import database
from fartberry.logger import logger
from fartberry.pms_5003_sensor import pms_5003_sensor


class _Fartberry:
    def __init__(self):
        signal.signal(signal.SIGINT, self._signal_handler)  # handle ctrl-c

    def run(self):
        while True:
            try:
                particulate_matter = pms_5003_sensor.get_particulate_matter()
                timestamp = datetime.now()
                logger.info(particulate_matter)
                database.insert(timestamp, particulate_matter)
            except Exception as e:
                logger.exception(e)

            time.sleep(config.polling_frequency_in_sec)

    def _signal_handler(self, signal, frame):
        database.close()
        logger.info('Closing program')
        sys.exit(0)


fartberry = _Fartberry()
