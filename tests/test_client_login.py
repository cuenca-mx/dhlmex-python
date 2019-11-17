import os

import pytest

from dhlmex import Client

DHLMEX_USERNAME = os.environ['DHLMEX_USERNAME']
DHLMEX_PASSWORD = os.environ['DHLMEX_PASSWORD']


@pytest.mark.vcr
def test_successful_login():
    # Just need to make sure it doesn't throw an exception
    assert Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
