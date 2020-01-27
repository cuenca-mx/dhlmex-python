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
        email='gino@cuenca.com',
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
        company='JOSE DE JESUS ALVARADO YERENA',
        contact='JOSE DE JESUS ALVARADO YERENA',
        email='yerena13_24@hotmail.com',
        phone='3223444645',
        address1='CALLE PEONIAS 40A',
        postal_code='63737',
        neighborhood='JARDINES DEL SOL',
        city='FRACCIONAMIENTO SANTA FE',
        state='NAY',
    )


@pytest.fixture
def invalid_destination() -> Destination:
    return Destination(
        company='GLENDA LOPEZ',
        contact='GLENDA LOPEZ',
        email='glenda@hotmail.com',
        phone='550909090',
        address1='EMILIANO ZAPATA 2',
        postal_code='37800',
        neighborhood='REVOLUCION',
        city='DOLORES HIDALGO CUNA DE LA INDEPENDENCIA NACIONAL',
        state='GTO',
    )


@pytest.fixture
def invalid_postal_code() -> Destination:
    return Destination(
        company='ALEJANDRO VIZQUEZ',
        contact='ALEJANDRO VIZQUEZ',
        email='alex_visquets@hotmail.com',
        phone='5560934315',
        address1='TOMAS ALVA EDISON 169',
        postal_code='00000',
        neighborhood='SAN RAFAEL',
        city='CUAUHTEMOC',
        state='CDMX',
    )


@pytest.fixture
def fake_destination() -> Destination:
    return Destination(
        company='GUADALUPE IVONNE SANTILLANES SANTILLANES',
        contact='GUADALUPE IVONNE SANTILLANES SANTILLANES',
        email='ivonnesantillanes0@gmail.com',
        phone='6623262213',
        address1='AVENIDA ARCELIA MORAGA 171',
        postal_code='83105',
        neighborhood='CARIDAD',
        city='HERMOSILLO',
        state='SON',
    )


@pytest.fixture
def details() -> OrderDetails:
    return OrderDetails(
        description='CASA COLOR VERDE', content='Tarjetas de presentacion',
    )
