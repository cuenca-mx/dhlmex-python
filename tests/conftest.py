from urllib import parse

import pytest
from vcr import request


def remove_creds(request: request.Request) -> request.Request:
    if request.path.endswith('/jsp/app/login/login.xhtml'):
        username_key = 'j_id6:j_id20'
        password_key = 'j_id6:j_id22'
        body = parse.parse_qs(request.body.decode('utf-8'))
        body[username_key] = ['USERNAME']
        body[password_key] = ['PASSWORD']
        request.body = parse.urlencode(body)
    return request


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict(before_record_request=remove_creds)
    return config
