#!/usr/bin/env python3
from unittest import TestCase, mock

from fartberry.pms_5003_sensor import *


class TestPms5003Sensor(TestCase):
    def setUp(self) -> None:
        CHECK_SUM = [0x01, 0x90]

        self._valid_bytes = bytes([
            FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x01, 0x00, 0x02,
            0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06,
            0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0a,
            0x00, 0x0b, 0x00, 0x0c, 0x97, 0x00] + CHECK_SUM)

        self._particulate_matter = ParticulateMatter(
            **{
                PM1_STANDARD: int.from_bytes(self._valid_bytes[4:6], byteorder='big'),
                PM25_STANDARD: int.from_bytes(self._valid_bytes[6:8], byteorder='big'),
                PM10_STANDARD: int.from_bytes(self._valid_bytes[8:10], byteorder='big'),
                PM1_AMBIENT: int.from_bytes(self._valid_bytes[10:12], byteorder='big'),
                PM25_AMBIENT: int.from_bytes(self._valid_bytes[12:14], byteorder='big'),
                PM10_AMBIENT: int.from_bytes(self._valid_bytes[14:16], byteorder='big'),
                PARTICLES_03: int.from_bytes(self._valid_bytes[16:18], byteorder='big'),
                PARTICLES_05: int.from_bytes(self._valid_bytes[18:20], byteorder='big'),
                PARTICLES_1: int.from_bytes(self._valid_bytes[20:22], byteorder='big'),
                PARTICLES_25: int.from_bytes(self._valid_bytes[22:24], byteorder='big'),
                PARTICLES_5: int.from_bytes(self._valid_bytes[24:26], byteorder='big'),
                PARTICLES_10: int.from_bytes(self._valid_bytes[26:28], byteorder='big'),
            }
        )

    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_success(self, mock_connection) -> None:
        suffix_bytes = self._valid_bytes[0:BYTE_COUNT - 1]
        mock_connection.read.return_value = self._valid_bytes + suffix_bytes

        particulate_matter = pms_5003_sensor.get_particulate_matter()

        self.assertEqual(particulate_matter, self._particulate_matter)
        mock_connection.read.assert_called_once()

    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_success_mid_stream(self, mock_connection) -> None:
        prefix_bytes = bytes([0x01, 0x01, 0x01])
        suffix_bytes = bytes([0x01, 0x01, 0x01])

        mock_connection.read.return_value = prefix_bytes + self._valid_bytes + suffix_bytes

        particulate_matter = pms_5003_sensor.get_particulate_matter()

        self.assertEqual(particulate_matter, self._particulate_matter)
        mock_connection.read.assert_called_once()

    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_fail_empty(self, mock_connection) -> None:
        mock_connection.read.return_value = bytes()

        with self.assertRaises(IOError):
            _particulate_matter = pms_5003_sensor.get_particulate_matter()

        mock_connection.read.assert_called_once()

    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_fail_checksum(self, mock_connection) -> None:
        invalid_bytes = self._valid_bytes[0:4] + \
            bytes([0xff]) + self._valid_bytes[5:]

        mock_connection.read.return_value = invalid_bytes

        with self.assertRaises(IOError):
            _particulate_matter = pms_5003_sensor.get_particulate_matter()

        mock_connection.read.assert_called_once()
