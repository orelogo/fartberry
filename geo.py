#!/usr/bin/env python3
import requests
import logging
from collections import namedtuple

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


class Geo():
    URL = 'http://www.ip-api.com/json'  # HTTPS not available in free version

    def __init__(self):

        try:
            resp = requests.get(self.URL).json()
            self.data = GeoData(
                **{
                    COUNTRY: resp['country'],
                    COUNTRY_CODE: resp['countryCode'],
                    REGION: resp['region'],
                    REGION_NAME: resp['regionName'],
                    CITY: resp['city'],
                    ZIP: resp['zip'],
                    LAT: resp['lat'],
                    LON: resp['lon'],
                    TIMEZONE: resp['timezone'],
                    IPV4: resp['query'],
                }
            )
            logging.info(self.data)

        except Exception as ex:
            logging.exception(ex)
            self.data = None
