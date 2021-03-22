#!/usr/bin/env python3
import psycopg2
import constants
from config import Config


class Database():
    TABLE = 'air_quality'

    def __init__(self) -> None:
        config = Config()
        self.connection = psycopg2.connect(
            database=config.postgres_database, user=config.postgres_user)
        self.connection.autocommit = True
        self.cur = self.connection.cursor()

        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.TABLE} (
                            id serial PRIMARY KEY,
                            {constants.TIMESTAMP} TIMESTAMP WITH TIME ZONE,
                            {constants.PM1_STANDARD} integer,
                            {constants.PM25_STANDARD} integer,
                            {constants.PM10_STANDARD} integer,
                            {constants.PM1_AMBIENT} integer,
                            {constants.PM25_AMBIENT} integer,
                            {constants.PM10_AMBIENT} integer,
                            {constants.PARTICLES_03} integer,
                            {constants.PARTICLES_05} integer,
                            {constants.PARTICLES_1} integer,
                            {constants.PARTICLES_25} integer,
                            {constants.PARTICLES_5} integer,
                            {constants.PARTICLES_10} integer
                        );""")

    def insert(self, timestamp, particulate_matter: constants.ParticulateMatter) -> None:
        self.cur.execute(f"""INSERT INTO {self.TABLE} (
                            {constants.TIMESTAMP},
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
                        );""", {constants.TIMESTAMP: timestamp, **particulate_matter._asdict()})

    def close(self) -> None:
        self.cur.close()
        self.connection.close()
