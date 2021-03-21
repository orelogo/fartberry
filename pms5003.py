#!/usr/bin/env python3

import serial
import datetime

from os import path
import constants
import db

BYTE_COUNT = 32
FIRST_BYTE = 0x42
SECOND_BYTE = 0x4d
FRAME_LENGTH = 28


def verify_data(data: bytes) -> bool:
    if not data:
        print("No data received from sensor")
        return False

    frame_length = int.from_bytes(data[2:4], byteorder='big')
    check_sum_expected = int.from_bytes(data[30:32], byteorder='big')
    check_sum_calculated = 0
    for i in range(0, BYTE_COUNT - 2):
        check_sum_calculated += data[i]

    if (data[0] != FIRST_BYTE
            or data[1] != SECOND_BYTE
            or frame_length != FRAME_LENGTH
            or check_sum_calculated != check_sum_expected):
        print("Unexpected data received from sensor")
        return False

    return True


serial_port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
abs_log_path = path.join(path.dirname(__file__), "pms5003_log.txt")
log = open(abs_log_path, "a+")
db.open()

try:
    while True:
        data = serial_port.read(BYTE_COUNT)
        if not verify_data(data):
            print("Terminating connection with sensor")
            break

        air_quality = constants.AirQuality(
            **{
                constants.TIMESTAMP: datetime.datetime.now(),
                constants.PM1_STANDARD: int.from_bytes(data[4:6], byteorder='big'),
                constants.PM25_STANDARD: int.from_bytes(data[6:8], byteorder='big'),
                constants.PM10_STANDARD: int.from_bytes(data[8:10], byteorder='big'),
                constants.PM1_AMBIENT: int.from_bytes(data[10:12], byteorder='big'),
                constants.PM25_AMBIENT: int.from_bytes(data[12:14], byteorder='big'),
                constants.PM10_AMBIENT: int.from_bytes(data[14:16], byteorder='big'),
                constants.PARTICLES_03: int.from_bytes(data[16:18], byteorder='big'),
                constants.PARTICLES_05: int.from_bytes(data[18:20], byteorder='big'),
                constants.PARTICLES_1: int.from_bytes(data[20:22], byteorder='big'),
                constants.PARTICLES_25: int.from_bytes(data[22:24], byteorder='big'),
                constants.PARTICLES_5: int.from_bytes(data[24:26], byteorder='big'),
                constants.PARTICLES_10: int.from_bytes(data[26:28], byteorder='big'),
            }
        )

        db.insert(air_quality)
        log.write(str(air_quality))
        log.flush()
        print(str(air_quality))

finally:
    db.close()
    log.close()
    print("Closing program")
