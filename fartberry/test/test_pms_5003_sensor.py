#!/usr/bin/env python3
from unittest import TestCase, mock

from fartberry.pms_5003_sensor import *


class TestPms5003Sensor(TestCase):
    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_success(self, mock_connection):
        mock_connection.read.return_value = bytes([
            FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d, 0x00, 0x14,
            0x00, 0x19, 0x00, 0x0d, 0x00, 0x14, 0x00, 0x19,
            0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c, 0x00, 0x0d,
            0x00, 0x06, 0x00, 0x04, 0x97, 0x00, 0x03, 0x7e,
            FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d, 0x00, 0x14,
            0x00, 0x19, 0x00, 0x0d, 0x00, 0x14, 0x00, 0x19,
            0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c, 0x00, 0x0d,
            0x00, 0x06, 0x00, 0x04, 0x97, 0x00, 0x03])

        actual_bytes = pms_5003_sensor._read_sensor()

        expected_bytes = bytes([FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d, 0x00, 0x14,
                                0x00, 0x19, 0x00, 0x0d, 0x00, 0x14, 0x00, 0x19,
                                0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c, 0x00, 0x0d,
                                0x00, 0x06, 0x00, 0x04, 0x97, 0x00, 0x03, 0x7e])

        self.assertEqual(actual_bytes, expected_bytes)
        mock_connection.read.assert_called_once()

    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_success_mid_stream(self, mock_connection):
        mock_connection.read.return_value = bytes([
            0x03, 0x7e, FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d,
            0x00, 0x14, 0x00, 0x19, 0x00, 0x0d, 0x00, 0x14,
            0x00, 0x19, 0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c,
            0x00, 0x0d, 0x00, 0x06, 0x00, 0x04, 0x97, 0x00,
            0x03, 0x7e, FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d,
            0x00, 0x14, 0x00, 0x19, 0x00, 0x0d, 0x00, 0x14,
            0x00, 0x19, 0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c,
            0x00, 0x0d, 0x00, 0x06, 0x00, 0x04, 0x97])

        actual_bytes = pms_5003_sensor._read_sensor()

        expected_bytes = bytes([FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d, 0x00, 0x14,
                                0x00, 0x19, 0x00, 0x0d, 0x00, 0x14, 0x00, 0x19,
                                0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c, 0x00, 0x0d,
                                0x00, 0x06, 0x00, 0x04, 0x97, 0x00, 0x03, 0x7e])

        self.assertEqual(actual_bytes, expected_bytes)
        mock_connection.read.assert_called_once()

    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_fail_empty(self, mock_connection):
        mock_connection.read.return_value=bytes()

        with self.assertRaises(IOError):
            _actual_bytes=pms_5003_sensor._read_sensor()

        mock_connection.read.assert_called_once()


    @mock.patch('fartberry.pms_5003_sensor.pms_5003_sensor.connection')
    def test_read_sensor_fail_checksum(self, mock_connection):
        mock_connection.read.return_value = bytes([
            0x03, 0x7e, FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d,
            0x00, 0x14, 0x00, 0x19, 0x00, 0x0d, 0x00, 0x14,
            0x00, 0x19, 0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c,
            0x00, 0x0d, 0x00, 0x06, 0x00, 0x04, 0x97, 0x00,
            0x03, 0x7f, FIRST_BYTE, SECOND_BYTE, 0x00, FRAME_LENGTH, 0x00, 0x0d,
            0x00, 0x14, 0x00, 0x19, 0x00, 0x0d, 0x00, 0x14,
            0x00, 0x19, 0x09, 0x78, 0x02, 0xb2, 0x00, 0x7c,
            0x00, 0x0d, 0x00, 0x06, 0x00, 0x04, 0x97])

        with self.assertRaises(IOError):
            _actual_bytes=pms_5003_sensor._read_sensor()

        mock_connection.read.assert_called_once()

        # test geo
        # empty data when request
        # empty data when json not parsable
        # empty data when status error