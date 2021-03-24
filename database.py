#!/usr/bin/env python3
from datetime import datetime

import psycopg2

import constants
import geo
from config import Config

TABLE_GEO = 'geo'
TABLE_AIR_QUALITY = 'air_quality'
TIMESTAMP = "timestamp"


class Database():
    def __init__(self) -> None:
        config = Config()
        self.conn = psycopg2.connect(
            database=config.postgres_database, user=config.postgres_user)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

        self._create_tables()
        self._insert_geo()

    def _create_tables(self) -> None:
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_GEO} (
                            {TIMESTAMP} TIMESTAMP WITH TIME ZONE,
                            {geo.LAT} FLOAT4,
                            {geo.LON} FLOAT4,
                            {geo.COUNTRY_CODE} CHAR(2),
                            {geo.REGION_NAME} VARCHAR,
                            {geo.CITY} VARCHAR,
                            {geo.ZIP} VARCHAR,
                            PRIMARY KEY ({geo.LAT}, {geo.LON})
                        );''')

        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_AIR_QUALITY} (
                            id serial PRIMARY KEY,
                            {TIMESTAMP} TIMESTAMP WITH TIME ZONE,
                            {geo.LAT} FLOAT4,
                            {geo.LON} FLOAT4,
                            {constants.PM1_STANDARD} INT2,
                            {constants.PM25_STANDARD} INT2,
                            {constants.PM10_STANDARD} INT2,
                            {constants.PM1_AMBIENT} INT2,
                            {constants.PM25_AMBIENT} INT2,
                            {constants.PM10_AMBIENT} INT2,
                            {constants.PARTICLES_03} INT2,
                            {constants.PARTICLES_05} INT2,
                            {constants.PARTICLES_1} INT2,
                            {constants.PARTICLES_25} INT2,
                            {constants.PARTICLES_5} INT2,
                            {constants.PARTICLES_10} INT2,
                            FOREIGN KEY ({geo.LAT}, {geo.LON})
                                REFERENCES {TABLE_GEO} ({geo.LAT}, {geo.LON})
                        );''')

    def _insert_geo(self) -> None:
        self.geo = geo.Geo()

        if (self.geo.data):
            values = {TIMESTAMP: datetime.now(),
                      **self.geo.data._asdict()}

            self.cur.execute(f'''INSERT INTO {TABLE_GEO} (
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

    def insert(self, timestamp, particulate_matter: constants.ParticulateMatter) -> None:
        if (self.geo.data):
            values = {TIMESTAMP: timestamp,
                      **self.geo.data._asdict(),
                      **particulate_matter._asdict()}
        else:
            values = {TIMESTAMP: timestamp,
                      geo.LAT: None,
                      geo.LON: None,
                      **particulate_matter._asdict()}

        self.cur.execute(f'''INSERT INTO {TABLE_AIR_QUALITY} (
                            {TIMESTAMP},
                            {geo.LAT},
                            {geo.LON},
                            {constants.PM1_STANDARD},
                            {constants.PM25_STANDARD},
                            {constants.PM10_STANDARD},
                            {constants.PM1_AMBIENT},
                            {constants.PM25_AMBIENT},
                            {constants.PM10_AMBIENT},
                            {constants.PARTICLES_03},
                            {constants.PARTICLES_05},
                            {constants.PARTICLES_1},
                            {constants.PARTICLES_25},
                            {constants.PARTICLES_5},
                            {constants.PARTICLES_10})
                        VALUES (
                            %(timestamp)s,
                            %(lat)s,
                            %(lon)s,
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
                        );''', values)

    def close(self) -> None:
        self.cur.close()
        self.conn.close()
