#!/usr/bin/env python3

import psycopg2
import constants

DATABASE = 'fartberry'
TABLE = 'airquality'
USER = 'pi'

connection = None


def open():
    global connection
    connection = psycopg2.connect(database=DATABASE, user=USER)
    connection.autocommit = True
    cur = connection.cursor()

    cur.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE} (
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
    return connection


def insert(air_quality: constants.AirQuality) -> bool:
    cur = connection.cursor()
    cur.execute(f"""INSERT INTO {TABLE} (
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
                    );""", air_quality._asdict())

    cur.close()
    return True


def close():
    connection.close()
