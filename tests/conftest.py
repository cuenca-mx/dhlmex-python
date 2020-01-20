from typing import Dict
from urllib import parse

import pytest
from vcr import request

from dhlmex import Client
from dhlmex.resources import Resource
from dhlmex.resources.destination import Destination
from dhlmex.resources.order_details import OrderDetails
from dhlmex.resources.origin import Origin


def remove_creds(req: request.Request) -> request.Request:
    if req.path.endswith(Resource._urls['login']) and req.method == 'POST':
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
    return Resource._urls


@pytest.fixture
def client():
    client = Client()
    yield client
    client._logout()


@pytest.fixture
def origin() -> Origin:
    return Origin(
        company='CUENCA LABS',
        contact='GINO LAPI',
        mail='gino@cuenca.com',
        phone='5544364200',
        address1='VARSOVIA 36',
        postal_code='06600',
        neighborhood='JUAREZ',
        city='CUAUHTEMOC',
        state='CMX',
    )


@pytest.fixture
def destination() -> Destination:
    return Destination(
        company='AXEL RAMSES NAVARRO NORIEGA',
        contact='AXEL RAMSES NAVARRO NORIEGA',
        mail='axelnavarronoriega@gmail.com',
        phone='3324061266',
        address1='PINO SUAREZ 69',
        postal_code='45610',
        neighborhood='PEDREGAL DEL BOSQUE',
        city='SAN PEDRO TLAQUEPAQUE',
        state='JAL',
    )


@pytest.fixture
def details() -> OrderDetails:
    return OrderDetails(
        description='CASA COLOR VERDE', content='Tarjetas de presentacion',
    )
