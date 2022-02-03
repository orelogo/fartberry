#!/usr/bin/env python3
import struct
from typing import NamedTuple

from serial import Serial

from fartberry.logger import logger

# PM 1.0 concentration in μg/m^3, corrected to standard atmophere conditions
PM1_STANDARD = 'pm1_standard'
# PM 2.5 concentration in μg/m^3, corrected to standard atmophere conditions
PM25_STANDARD = 'pm25_standard'
# PM 10 concentration in μg/m^3, corrected to standard atmophere conditions
PM10_STANDARD = 'pm10_standard'
# PM 1.0 concentration in μg/m^3, in the current ambient conditions
PM1_AMBIENT = 'pm1_ambient'
# PM 2.5 concentration in μg/m^3, in the current ambient conditions
PM25_AMBIENT = 'pm25_ambient'
# PM 10  concentration in μg/m^3, in the current ambient conditions
PM10_AMBIENT = 'pm10_ambient'
# Number of particles with diameter >0.3 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_03 = 'particles_03'
# Number of particles with diameter >0.5 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_05 = 'particles_05'
# Number of particles with diameter >1.0 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_1 = 'particles_1'
# Number of particles with diameter >2.5 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_25 = 'particles_25'
# Number of particles with diameter >5.0 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_5 = 'particles_5'
# Number of particles with diameter >10.0 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_10 = 'particles_10'

ParticulateMatter = NamedTuple('ParticulateMatter', [
    (PM1_STANDARD, int),
    (PM25_STANDARD, int),
    (PM10_STANDARD, int),
    (PM1_AMBIENT, int),
    (PM25_AMBIENT, int),
    (PM10_AMBIENT, int),
    (PARTICLES_03, int),
    (PARTICLES_05, int),
    (PARTICLES_1, int),
    (PARTICLES_25, int),
    (PARTICLES_5, int),
    (PARTICLES_10, int),
])

DEVICE = '/dev/ttyAMA0'
BYTE_COUNT = 32
FIRST_BYTE = 0x42
SECOND_BYTE = 0x4d
FRAME_LENGTH = 0x1c


class _Pms5003Sensor():
    def __init__(self) -> None:
        self.connection = Serial(DEVICE, baudrate=9600, timeout=3.0)

    def get_particulate_matter(self) -> ParticulateMatter:
        data = self._read_sensor()

        particulate_matter = ParticulateMatter(
            **{
                PM1_STANDARD: int.from_bytes(data[4:6], byteorder='big'),
                PM25_STANDARD: int.from_bytes(data[6:8], byteorder='big'),
                PM10_STANDARD: int.from_bytes(data[8:10], byteorder='big'),
                PM1_AMBIENT: int.from_bytes(data[10:12], byteorder='big'),
                PM25_AMBIENT: int.from_bytes(data[12:14], byteorder='big'),
                PM10_AMBIENT: int.from_bytes(data[14:16], byteorder='big'),
                PARTICLES_03: int.from_bytes(data[16:18], byteorder='big'),
                PARTICLES_05: int.from_bytes(data[18:20], byteorder='big'),
                PARTICLES_1: int.from_bytes(data[20:22], byteorder='big'),
                PARTICLES_25: int.from_bytes(data[22:24], byteorder='big'),
                PARTICLES_5: int.from_bytes(data[24:26], byteorder='big'),
                PARTICLES_10: int.from_bytes(data[26:28], byteorder='big'),
            }
        )

        return particulate_matter

    def _read_sensor(self) -> bytes:
        # We cannot be sure where in the byte stream the read starts and sometimes
        # the initial data is invalid. This buffer gives us a better chance of receiving
        # a full valid stream
        bytes_to_read = BYTE_COUNT * 3

        data = self.connection.read(bytes_to_read)
        logger.debug(f'Raw data: {self._bytes_to_str(data)}')
        if (not data):
            raise IOError(
                f'No data received from sensor. Check that it is turned on.')

        trimmed_data = self._get_in_frame_data(data)
        logger.debug(f'Trimmed data: {self._bytes_to_str(trimmed_data)}')

        self._validate_check_sum(trimmed_data)
        return trimmed_data

    def _get_in_frame_data(self, data: bytes) -> bytes:
        starting_sequence = bytes(
            [FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH])
        start = data.index(starting_sequence)
        end = start + BYTE_COUNT
        return data[start:end]

    def _validate_check_sum(self, data: bytes) -> None:
        check_sum_calculated = 0
        for i in range(0, BYTE_COUNT - 2):
            check_sum_calculated += data[i]

        check_sum_expected = int.from_bytes(
            data[30:32], byteorder='big')

        if check_sum_calculated != check_sum_expected:
            # convert int to 2 bytes, big endian, for easier comparison
            check_sum_calculated_bytes = struct.pack(
                '>h', check_sum_calculated)
            check_sum_expected_bytes = struct.pack(
                '>h', check_sum_expected)
            raise IOError(
                (f'Check sum failed.\n'
                    f'Calculated checksum: {self._bytes_to_str(check_sum_calculated_bytes)}.\n'
                    f'Expected checksum: {self._bytes_to_str(check_sum_expected_bytes)}.\n'
                    f'Trimmed data: {self._bytes_to_str(data)}')
            )

    def _bytes_to_str(self, data: bytes) -> str:
        return ' '.join('0x{:02x}'.format(byte) for byte in data)


pms_5003_sensor = _Pms5003Sensor()
