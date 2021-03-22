#!/usr/bin/env python3
from serial import Serial
import constants


class Pms5003Sensor():
    DEVICE = "/dev/ttyAMA0"
    BYTE_COUNT = 32
    FIRST_BYTE = 0x42
    SECOND_BYTE = 0x4d
    FRAME_LENGTH = 28
    MAX_ATTEMPTS = 3

    def __init__(self) -> None:
        self.connection = Serial(self.DEVICE, baudrate=9600, timeout=3.0)

    def _read_sensor(self) -> bytes:
        # retries necessary because sometimes the inital sensor read does not align correctly
        for i in range(self.MAX_ATTEMPTS):
            data = self.connection.read(self.BYTE_COUNT)

            frame_length = int.from_bytes(data[2:4], byteorder='big')
            check_sum_expected = int.from_bytes(data[30:32], byteorder='big')
            check_sum_calculated = 0
            for i in range(0, self.BYTE_COUNT - 2):
                check_sum_calculated += data[i]

            if (data[0] == self.FIRST_BYTE
                and data[1] == self.SECOND_BYTE
                and frame_length == self.FRAME_LENGTH
                    and check_sum_calculated == check_sum_expected):
                return data

        raise IOError(
            f"Unexpected data received from sensor, even after {self.MAX_ATTEMPTS} attempts")

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
