#!/usr/bin/env python3
import json
from pathlib import Path

from fartberry.logger import logger

POSTGRES_USER = 'postgres_user'
POSTGRES_DATABASE = 'postgres_database'
IS_GEOLOCATION_ENABLED = 'is_geolocation_enabled'
POLLING_FREQUENCY_IN_SEC = 'polling_frequency_in_sec'


class _Config():
    def __init__(self) -> None:
        abs_config_path = str(Path(__file__).parent.parent / 'config.json')
        with open(abs_config_path, 'r') as f:
            config_json = json.load(f)

        self.postgres_user = config_json[POSTGRES_USER]
        self.postgres_database = config_json[POSTGRES_DATABASE]
        self.is_geolocation_enabled = config_json[IS_GEOLOCATION_ENABLED]
        self.polling_frequency_in_sec = config_json[POLLING_FREQUENCY_IN_SEC]
        logger.debug('Config loaded')


config = _Config()
