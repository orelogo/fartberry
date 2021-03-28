#!/usr/bin/env python3
import logging
import signal
import sys
import time
from datetime import datetime
from os import path

from config import config
from database import Database
from pms_5003_sensor import Pms5003Sensor


class Fartberry:
    def __init__(self):
        signal.signal(signal.SIGINT, self._signal_handler)  # handle ctrl-c
        self.database = Database()
        self.particulate_matter_sensor = Pms5003Sensor()

    def _signal_handler(self, signal, frame):
        self.database.close()
        logging.info('Closing program')
        print('Closing program')
        sys.exit(0)

    def run(self):
        while True:
            try:
                particulate_matter = self.particulate_matter_sensor.get_particulate_matter()
                timestamp = datetime.now()

                self.database.insert(timestamp, particulate_matter)
                logging.info(particulate_matter)
                print(f'{str(timestamp)} - {particulate_matter}\n')

            except Exception as e:
                logging.exception(e)

            time.sleep(config.polling_frequency_in_sec)


def main():
    logging.basicConfig(filename='fartberry.log', level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s - %(message)s')

    fartberry = Fartberry()
    fartberry.run()


if __name__ == '__main__':
    main()
