import pytest
from requests import Request


def remove_creds(request: Request) -> Request:
    # remove username and password
    return request


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict()
    config['before_record_request'] = remove_creds
    return config