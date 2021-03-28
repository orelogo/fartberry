#!/usr/bin/env python3
import logging
from collections import namedtuple

import requests

from config import config

COUNTRY = 'country'
COUNTRY_CODE = 'country_code'  # two-letter country code ISO 3166-1 alpha-2, eg. US
REGION = 'region'  # region/state short code, eg. CA for California
REGION_NAME = 'region_name'  # region/state name, eg. California
CITY = 'city'
ZIP = 'zip'  # for US, zip code, eg. 90210
LAT = 'lat'
LON = 'lon'
TIMEZONE = 'timezone'  # eg. America/Los_Angeles
IPV4 = 'ipv4'

GeoData = namedtuple('GeoData', [
    COUNTRY,
    COUNTRY_CODE,
    REGION,
    REGION_NAME,
    CITY,
    ZIP,
    LAT,
    LON,
    TIMEZONE,
    IPV4
])

URL = 'http://www.ip-api.com/json'  # HTTPS not available in free version


class Geo():
    def __init__(self):
        if (not config.is_geolocation_enabled):
            self.data = None
            logging.info('Geolocation disabled')
            return

        try:
            resp = requests.get(URL)
            resp.raise_for_status()
            json = resp.json()
            self.data = GeoData(
                **{
                    COUNTRY: json['country'],
                    COUNTRY_CODE: json['countryCode'],
                    REGION: json['region'],
                    REGION_NAME: json['regionName'],
                    CITY: json['city'],
                    ZIP: json['zip'],
                    LAT: json['lat'],
                    LON: json['lon'],
                    TIMEZONE: json['timezone'],
                    IPV4: json['query'],
                }
            )
            logging.info(self.data)

        except Exception as ex:
            logging.exception(ex)
            self.data = None
