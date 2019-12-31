from typing import Dict
from urllib import parse

import pytest
from vcr import request

from dhlmex.resources.urls import dhl_urls


def remove_creds(req: request.Request) -> request.Request:
    if req.path.endswith(dhl_urls['login']) and req.method == 'POST':
        username_key = 'j_id6:j_id20'
        password_key = 'j_id6:j_id22'
        body = parse.parse_qs(req.body.decode('utf-8'))
        body[username_key] = ['USERNAME']
        body[password_key] = ['PASSWORD']
        req.body = parse.urlencode(body)
    return req


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict(before_record_request=remove_creds)
    return config


@pytest.fixture
def site_urls() -> Dict:
    return dhl_urls
