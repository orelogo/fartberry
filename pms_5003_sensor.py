#!/usr/bin/env python3
from serial import Serial
import logging

import constants

DEVICE = '/dev/ttyAMA0'
BYTE_COUNT = 32
FIRST_BYTE = 0x42
SECOND_BYTE = 0x4d
FRAME_LENGTH = 0x1c
MAX_ATTEMPTS = 3


class Pms5003Sensor():
    def __init__(self) -> None:
        self.connection = Serial(DEVICE, baudrate=9600, timeout=3.0)

    def get_particulate_matter(self) -> constants.ParticulateMatter:
        data = self._read_sensor()

        particulate_matter = constants.ParticulateMatter(
            **{
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

        return particulate_matter

    def _read_sensor(self) -> bytes:
        # assuming that we can't be sure where in the byte stream the read starts,
        # this is the minimum number of bytes required to ensure we can capute an
        # entire valid frame of data
        bytes_to_read = BYTE_COUNT * 2 - 1

        data = self.connection.read(bytes_to_read)
        logging.debug(self._bytes_to_str(data))
        trimmed_data = self._get_in_frame_data(data)
        logging.debug(self._bytes_to_str(trimmed_data))

        check_sum_expected = int.from_bytes(
            trimmed_data[30:32], byteorder='big')
        check_sum_calculated = 0
        for i in range(0, BYTE_COUNT - 2):
            check_sum_calculated += trimmed_data[i]

        if (check_sum_calculated == check_sum_expected):
            return trimmed_data
        else:
            raise IOError(f'Check sum failed: {self._bytes_to_str(trimmed_data)}')

    def _get_in_frame_data(self, data: bytes) -> bytes:
        starting_sequence = bytes(
            [FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH])
        start = data.index(starting_sequence)
        end = start + BYTE_COUNT
        return data[start:end]

    def _bytes_to_str(self, data: bytes) -> str:
        return ' '.join('0x{:02x}'.format(byte) for byte in data)
