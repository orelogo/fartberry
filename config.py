#!/usr/bin/env python3
import json
from os import path

POSTGRES_USER = 'postgres_user'
POSTGRES_DATABASE = 'postgres_database'
POLLING_FREQUENCY_IN_SEC = 'polling_frequency_in_sec'


class Config():
    def __init__(self) -> None:

        abs_config_path = path.join(path.dirname(__file__), 'config.json')
        with open(abs_config_path, 'r') as f:
            config_json = json.load(f)

        self.postgres_user = config_json[POSTGRES_USER]
        self.postgres_database = config_json[POSTGRES_DATABASE]
        self.polling_frequency_in_sec = config_json[POLLING_FREQUENCY_IN_SEC]
