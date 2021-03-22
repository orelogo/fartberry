#!/usr/bin/env python3
import psycopg2
import constants
from config import Config
import geo


class Database():
    TABLE = 'air_quality'
    TIMESTAMP = "timestamp"

    def __init__(self) -> None:
        config = Config()
        self.connection = psycopg2.connect(
            database=config.postgres_database, user=config.postgres_user)
        self.connection.autocommit = True
        self.cur = self.connection.cursor()

        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.TABLE} (
                            id serial PRIMARY KEY,
                            {self.TIMESTAMP} TIMESTAMP WITH TIME ZONE,
                            {geo.LAT} FLOAT4,
                            {geo.LON} FLOAT4,
                            {geo.COUNTRY_CODE} CHAR(2),
                            {geo.REGION_NAME} VARCHAR,
                            {geo.CITY} VARCHAR,
                            {geo.ZIP} VARCHAR,
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
                            {constants.PARTICLES_10} INT2
                        );""")
        self.geo = geo.Geo()

    def insert(self, timestamp, particulate_matter: constants.ParticulateMatter) -> None:
        values = {self.TIMESTAMP: timestamp,
                  **self.geo.data._asdict(),
                  **particulate_matter._asdict()}

        self.cur.execute(f"""INSERT INTO {self.TABLE} (
                            {self.TIMESTAMP},
                            {geo.COUNTRY_CODE},
                            {geo.REGION_NAME},
                            {geo.CITY},
                            {geo.ZIP},
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
                            %(country_code)s,
                            %(region_name)s,
                            %(city)s,
                            %(zip)s,
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
                        );""", values)

    def close(self) -> None:
        self.cur.close()
        self.connection.close()
