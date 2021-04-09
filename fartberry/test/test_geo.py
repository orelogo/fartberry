
#!/usr/bin/env python3
import json
from unittest import TestCase, mock

import requests
from fartberry.geo import *


class TestGeo(TestCase):
    @mock.patch('fartberry.geo.requests')
    @mock.patch('fartberry.geo.config')
    def test_get_geolocation_success(self, config, requests) -> None:
        config.is_geolocation_enabled = True

        expected_geolocation = Geolocation(
            **{
                COUNTRY: 'United States',
                COUNTRY_CODE: 'US',
                REGION: 'WA',
                REGION_NAME: 'Washington',
                CITY: 'Seattle',
                ZIP: '90210',
                LAT: 40.000,
                LON: 69.000,
                TIMEZONE: 'America/Los_Angeles',
                IPV4: '127.0.0.1',
            }
        )

        json_response = {
            'country': expected_geolocation.country,
            'countryCode': expected_geolocation.country_code,
            'region': expected_geolocation.region,
            'regionName': expected_geolocation.region_name,
            'city': expected_geolocation.city,
            'zip': expected_geolocation.zip,
            'lat': expected_geolocation.lat,
            'lon': expected_geolocation.lon,
            'timezone': expected_geolocation.timezone,
            'query': expected_geolocation.ipv4,
        }

        response = mock.Mock()
        response.json.return_value = json_response
        requests.get.return_value = response

        geolocation = geo.get_geolocation()
        self.assertEqual(geolocation, expected_geolocation)

        requests.get.assert_called_once()

    @mock.patch('fartberry.geo.requests')
    @mock.patch('fartberry.geo.config')
    def test_get_geolocation_none_when_disabled_in_config(self, config, requests) -> None:
        config.is_geolocation_enabled = False

        geolocation = geo.get_geolocation()
        self.assertIsNone(geolocation)

        requests.get.assert_not_called()

    @mock.patch('fartberry.geo.requests')
    @mock.patch('fartberry.geo.config')
    def test_get_geolocation_none_when_request_fails(self, config, requests) -> None:
        config.is_geolocation_enabled = True
        requests.get.side_effect = Exception

        geolocation = geo.get_geolocation()
        self.assertIsNone(geolocation)

        requests.get.assert_called_once()
