#!/usr/bin/env python3
import logging
import signal
import sys
import time
from datetime import datetime
from os import path

import constants
from config import Config
from database import Database
from pms_5003_sensor import Pms5003Sensor

logging.basicConfig(filename='fartberry.log', level=logging.INFO, format='%(asctime)s:%(levelname)s - %(message)s')

config = Config()
database = Database()
particulate_matter_sensor = Pms5003Sensor()

def signal_handler(signal, frame):
    database.close()
    logging.info('Closing program')
    print('Closing program')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler) # handle ctrl-c

while True:
    try:
        particulate_matter = particulate_matter_sensor.get_particulate_matter()
        timestamp = datetime.now()

        database.insert(timestamp, particulate_matter)
        logging.info(particulate_matter)
        print(f'{str(timestamp)} - {particulate_matter}\n')

    except Exception as e:
        logging.exception(e)

    time.sleep(config.polling_frequency_in_sec)
