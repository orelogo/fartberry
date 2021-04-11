#!/usr/bin/env python3

from typing import NamedTuple, Optional

import requests

from fartberry.config import config
from fartberry.logger import logger

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

Geolocation = NamedTuple('Geolocation', [
    (COUNTRY, str),
    (COUNTRY_CODE, str),
    (REGION, str),
    (REGION_NAME, str),
    (CITY, str),
    (ZIP, str),
    (LAT, float),
    (LON, float),
    (TIMEZONE, str),
    (IPV4, str),
])

URL = 'http://www.ip-api.com/json'  # HTTPS not available in free version


class _Geo():
    def __init__(self) -> None:
        self._data: Optional[Geolocation] = None

    def get_geolocation(self) -> Optional[Geolocation]:
        if not config.is_geolocation_enabled:
            self._data = None
            logger.info('Geolocation disabled')
            return self._data

        if not self._data:
            self._data = self._request_geolocation()

        return self._data

    def _request_geolocation(self) -> Optional[Geolocation]:
        try:
            resp = requests.get(URL)
            resp.raise_for_status()
            json = resp.json()
            geolocation = Geolocation(
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
            logger.info(geolocation)
            return geolocation

        except Exception as ex:
            logger.exception(ex)
            return None


geo = _Geo()
