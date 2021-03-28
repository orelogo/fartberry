
#!/usr/bin/env python3
from unittest import TestCase, mock

import requests
from fartberry.geo import _Geo


class TestGeo(TestCase):
    @mock.patch('requests.get')
    def test(self, mock_connection):
        assert(1, 1)

        # empty data when request
        # empty data when json not parsable
        # empty data when status error
