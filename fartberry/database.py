#!/usr/bin/env python3
from datetime import datetime
from typing import Optional

import psycopg2

from fartberry import bme_680_sensor, geo, pms_5003_sensor
from fartberry.config import config
from fartberry.logger import logger

TABLE_GEO = 'geolocation'
TABLE_AIR_QUALITY = 'air_quality'
TIMESTAMP = "timestamp"


class _Database():
    def __init__(self) -> None:
        self._conn = psycopg2.connect(
            database=config.postgres_database, user=config.postgres_user)
        self._conn.autocommit = True
        self._cur = self._conn.cursor()

    def create_air_quality_table(self) -> None:
        self._cur.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_AIR_QUALITY} (
                    id serial PRIMARY KEY,
                    {TIMESTAMP} TIMESTAMP WITH TIME ZONE,
                    {geo.LAT} FLOAT4,
                    {geo.LON} FLOAT4,
                    {bme_680_sensor.TEMPERATURE} FLOAT4,
                    {bme_680_sensor.HUMIDITY} FLOAT4,
                    {bme_680_sensor.PRESSURE} FLOAT4,
                    {pms_5003_sensor.PM1_STANDARD} INT2,
                    {pms_5003_sensor.PM25_STANDARD} INT2,
                    {pms_5003_sensor.PM10_STANDARD} INT2,
                    {pms_5003_sensor.PM1_AMBIENT} INT2,
                    {pms_5003_sensor.PM25_AMBIENT} INT2,
                    {pms_5003_sensor.PM10_AMBIENT} INT2,
                    {pms_5003_sensor.PARTICLES_03} INT2,
                    {pms_5003_sensor.PARTICLES_05} INT2,
                    {pms_5003_sensor.PARTICLES_1} INT2,
                    {pms_5003_sensor.PARTICLES_25} INT2,
                    {pms_5003_sensor.PARTICLES_5} INT2,
                    {pms_5003_sensor.PARTICLES_10} INT2,
                    FOREIGN KEY ({geo.LAT}, {geo.LON})
                        REFERENCES {TABLE_GEO} ({geo.LAT}, {geo.LON})
                );''')

    def insert(self,
               timestamp,
               gas_properties: bme_680_sensor.GasProperties,
               particulate_matter: pms_5003_sensor.ParticulateMatter,
               geolocation: Optional[geo.Geolocation]) -> None:

        if geolocation:
            values = {TIMESTAMP: timestamp,
                      **geolocation._asdict(),
                      **gas_properties._asdict(),
                      **particulate_matter._asdict()}
        else:
            values = {TIMESTAMP: timestamp,
                      geo.LAT: None,
                      geo.LON: None,
                      **gas_properties._asdict(),
                      **particulate_matter._asdict()}

        self._cur.execute(f'''INSERT INTO {TABLE_AIR_QUALITY} (
                            {TIMESTAMP},
                            {geo.LAT},
                            {geo.LON},
                            {bme_680_sensor.TEMPERATURE},
                            {bme_680_sensor.HUMIDITY},
                            {bme_680_sensor.PRESSURE},
                            {pms_5003_sensor.PM1_STANDARD},
                            {pms_5003_sensor.PM25_STANDARD},
                            {pms_5003_sensor.PM10_STANDARD},
                            {pms_5003_sensor.PM1_AMBIENT},
                            {pms_5003_sensor.PM25_AMBIENT},
                            {pms_5003_sensor.PM10_AMBIENT},
                            {pms_5003_sensor.PARTICLES_03},
                            {pms_5003_sensor.PARTICLES_05},
                            {pms_5003_sensor.PARTICLES_1},
                            {pms_5003_sensor.PARTICLES_25},
                            {pms_5003_sensor.PARTICLES_5},
                            {pms_5003_sensor.PARTICLES_10})
                        VALUES (
                            %(timestamp)s,
                            %(lat)s,
                            %(lon)s,
                            %(temperature)s,
                            %(humidity)s,
                            %(pressure)s,
                            %(pm1_standard)s,
                            %(pm25_standard)s,
                            %(pm10_standard)s,
                            %(pm1_ambient)s,
                            %(pm25_ambient)s,
                            %(pm10_ambient)s,
                            %(particles_03)s,
                            %(particles_05)s,
                            %(particles_1)s,
                            %(particles_25)s,
                            %(particles_5)s,
                            %(particles_10)s
                        ); ''', values)
        logger.debug('Air quality inserted into database')

    def create_geolocation_table_and_insert(self, geolocation: geo.Geolocation) -> None:
        self._cur.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_GEO} (
                            {TIMESTAMP} TIMESTAMP WITH TIME ZONE,
                            {geo.LAT} FLOAT4,
                            {geo.LON} FLOAT4,
                            {geo.COUNTRY_CODE} CHAR(2),
                            {geo.REGION_NAME} VARCHAR,
                            {geo.CITY} VARCHAR,
                            {geo.ZIP} VARCHAR,
                            PRIMARY KEY ({geo.LAT}, {geo.LON})
                        );''')

        values = {TIMESTAMP: datetime.now(),
                  **geolocation._asdict()}

        self._cur.execute(f'''INSERT INTO {TABLE_GEO} (
                                {TIMESTAMP},
                                {geo.LAT},
                                {geo.LON},
                                {geo.COUNTRY_CODE},
                                {geo.REGION_NAME},
                                {geo.CITY},
                                {geo.ZIP})
                            VALUES (
                                %(timestamp)s,
                                %(lat)s,
                                %(lon)s,
                                %(country_code)s,
                                %(region_name)s,
                                %(city)s,
                                %(zip)s
                            ) ON CONFLICT DO NOTHING;''',
                          values)

    def close(self) -> None:
        self._cur.close()
        self._conn.close()


database = _Database()
