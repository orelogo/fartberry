#!/usr/bin/env python3
from datetime import datetime
from os import path
import time

import constants
from database import Database
from pms_5003_sensor import Pms5003Sensor
from config import Config

abs_log_path = path.join(path.dirname(__file__), "pms5003_log.txt")
log = open(abs_log_path, "a+")
config = Config()
database = Database()
particulate_matter_sensor = Pms5003Sensor()

try:
    while True:
        particulate_matter = particulate_matter_sensor.get_particulate_matter()
        timestamp = datetime.now()

        database.insert(timestamp, particulate_matter)
        log.write(f"{str(timestamp)} - {particulate_matter}\n")
        log.flush()
        print(f"{str(timestamp)} - {particulate_matter}\n")
        
        time.sleep(config.polling_frequency_in_sec)

finally:
    database.close()
    log.close()
    print("Closing program")
