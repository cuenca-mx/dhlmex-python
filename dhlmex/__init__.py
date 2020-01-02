__all__ = ['__version__', 'Client']

import re
from typing import Dict

from bs4 import BeautifulSoup
from requests import HTTPError

from dhlmex.exceptions import DhlmexException
from dhlmex.resources.helpers import get_data
from dhlmex.resources.urls import actions, dhl_urls

from .client import Client
from .version import __version__


def get_guides_data(client: Client) -> Dict:
    resp = client.post(dhl_urls['home'], {})
    data = get_data(resp, actions['print'])
    soup = BeautifulSoup(resp.text, features='html.parser')
    field = soup.find('input', id=re.compile('panelBarInput')).attrs['name']
    data[field] = actions['print']['code']
    guides_data = {}
    try:
        resp = client.post(dhl_urls['home'], data)
    except HTTPError as httpe:
        raise httpe
    if 'seleccionar' in resp.text:
        soup = BeautifulSoup(resp.text, features='html.parser')
        view_state = soup.find('input', id='javax.faces.ViewState').attrs[
            'value'
        ]
        table = soup.find('table', id='j_id6:pnlOrdenesEncontradas')
        table_body = table.find('tbody')
        js = table_body.find('a', text='seleccionar').attrs['onclick']
        matches = re.findall(r"\'(.+?)\'", js)
        form_ids = [match for match in matches if match.startswith('j_id')]
        j_pair_id = form_ids[1]
        j_id = form_ids[0]
        guides_data = {
            'AJAXREQUEST': '_viewRoot',
            j_id: j_id,
            'javax.faces.ViewState': view_state,
            j_pair_id: j_pair_id,
        }
    return guides_data


def select_guide(client: Client, guides_data: Dict) -> Dict:
    resp = client.post(dhl_urls['guide'], guides_data)
    soup = BeautifulSoup(resp.text, features='html.parser')
    view_state = soup.find('input', id='javax.faces.ViewState').attrs['value']
    js = soup.find('input', value='').attrs['onkeyup']
    matches = re.findall(r"\'(.+?)\'", js)
    form_ids = [match for match in matches if match.startswith('j_id')]
    j_pair_id = form_ids[1]
    j_id = form_ids[0]
    select_data = {
        'AJAXREQUEST': '_viewRoot',
        j_id: j_id,
        j_pair_id: '1',
        'javax.faces.ViewState': view_state,
        'javax.faces.ViewState': 'j_id2',
        'j_id6:btnGuardarCotizacion': 'j_id6:btnGuardarCotizacion',
    }
    return select_data


def create_guide(username: str, password: str):
    try:
        dhl_client = Client(username, password)
        guides_data = get_guides_data(dhl_client)
        if guides_data:  # Check if there are available guides
            resp = dhl_client.post(dhl_urls['guide'], guides_data)
        else:
            raise DhlmexException('No available guides')
    except HTTPError as httpe:
        raise httpe

    finally:
        dhl_client._logout()
