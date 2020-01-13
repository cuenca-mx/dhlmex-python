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
    j_id2 = soup.find('input', value='').attrs['name']
    js = soup.find('input', value='').attrs['onkeyup']
    matches = re.findall(r"\'(.+?)\'", js)
    form_ids = [match for match in matches if match.startswith('j_id')]
    j_pair_id = form_ids[1]
    j_id = form_ids[0]
    select_data = {
        'AJAXREQUEST': '_viewRoot',
        j_id: j_id,
        j_id2: '1',
        'javax.faces.ViewState': view_state,
        j_pair_id: j_pair_id,
        'AJAX:EVENTS_COUNT': '1',
    }
    client.post(dhl_urls['guide'], select_data)
    select_data.pop(j_pair_id, None)
    select_data.pop('AJAX:EVENTS_COUNT', None)
    select_data['j_id6:btnGuardarCotizacion'] = 'j_id6:btnGuardarCotizacion'
    return select_data


def validate_postal_codes(
    client: Client, origin: Dict, destiny: Dict, view_state: str
) -> Dict:
    fill_data = {
        'AJAXREQUEST': '_viewRoot',
        'datos': 'datos',
        'datos:j_id10': 'j_id11',
        'datos:j_id15': '',
        'datos:j_id19': '',
        'datos:emailOrigen': '',
        'datos:j_id24': '',
        'datos:j_id28': '',
        'datos:j_id30': '',
        'datos:j_id32': '',
        'datos:j_id36': origin['postal_code'],
        'datos:j_id41': '',
        'datos:j_id45': '',
        'datos:j_id49': '',
        'datos:j_id54': '',
        'datos:j_id58': '',
        'datos:emailDestino': '',
        'datos:j_id63': '',
        'datos:j_id67': '',
        'datos:j_id69': '',
        'datos:j_id71': '',
        'datos:j_id75': '',
        'datos:j_id80': '',
        'datos:j_id84': '',
        'datos:j_id88': '',
        'datos:j_id93': '',
        'datos:j_id95': '',
        'javax.faces.ViewState': view_state,
        'datos:j_id37': 'datos:j_id37',
    }
    resp = client.post(dhl_urls['capture'], fill_data)
    if 'Código Postal válido' in resp.text:
        fill_data.pop('datos:j_id37')
        # validate also destiny postal_code
        fill_data['datos:j_id76'] = 'datos:j_id76'
        fill_data['datos:j_id75'] = destiny['postal_code']
        resp = client.post(dhl_urls['capture'], fill_data)
        if 'Código Postal válido' in resp.text:
            fill_data.pop('datos:j_id76')
            return fill_data
        else:
            raise DhlmexException('Invalid destiny postal code')
    else:
        raise DhlmexException('Invalid origin postal code')


def fill_guide_table(
    client: Client, origin: Dict, destiny: Dict, details: Dict
) -> Dict:
    resp = client.get(dhl_urls['capture'])
    soup = BeautifulSoup(resp.text, features='html.parser')
    view_state = soup.find('input', id='javax.faces.ViewState').attrs['value']
    fill_data = validate_postal_codes(client, origin, destiny, view_state)
    fill_data['datos:j_id15'] = origin['company']
    fill_data['datos:j_id19'] = origin['contact']
    fill_data['datos:emailOrigen'] = origin['mail']
    fill_data['datos:j_id24'] = origin['phone']
    fill_data['datos:j_id28'] = origin['address1']
    fill_data['datos:j_id36'] = origin['postal_code']
    fill_data['datos:j_id41'] = origin['neighborhood']
    fill_data['datos:j_id45'] = origin['city']
    fill_data['datos:j_id49'] = origin['state']
    fill_data['datos:j_id54'] = destiny['company']
    fill_data['datos:j_id58'] = destiny['contact']
    fill_data['datos:emailDestino'] = destiny['mail']
    fill_data['datos:j_id63'] = destiny['phone']
    fill_data['datos:j_id67'] = destiny['address1']
    fill_data['datos:j_id75'] = destiny['postal_code']
    fill_data['datos:j_id80'] = destiny['neighborhood']
    fill_data['datos:j_id84'] = destiny['city']
    fill_data['datos:j_id88'] = destiny['state']
    fill_data['datos:j_id93'] = details['description']
    fill_data['datos:j_id95'] = details['content']
    fill_data['javax.faces.ViewState'] = view_state
    fill_data['datos:j_id105'] = 'datos:j_id105'

    return fill_data


def confirm_capture(client: Client, view_state: str) -> Dict:
    confirm_data = {
        'AJAXREQUEST': '_viewRoot',
        'j_id109': 'j_id109',
        'javax.faces.ViewState': view_state,
        'j_id109:j_id112': 'j_id109:j_id112',
    }
    return client.post(dhl_urls['capture'], confirm_data)


def force_percent(client: Client, view_state: str) -> str:
    force_data = {
        'AJAXREQUEST': '_viewRoot',
        'j_id115': 'j_id115',
        'javax.faces.ViewState': view_state,
        'j_id115:pb_sub': 'j_id115:pb_sub',
        'forcePercent': 'complete',
        'ajaxSingle': 'j_id115:pb_sub',
    }
    resp = client.post(dhl_urls['capture'], force_data)
    if 'Procesada correctamente' in resp.text:
        soup = BeautifulSoup(resp.text, features='html.parser')
        return soup.find('td', id='j_id115:tblElementos:0:j_id123').text
    else:
        raise DhlmexException('Error while processing guide')


def download_pdf(client: Client, guide_number: str, view_state: str):
    guide_data = {
        'AJAXREQUEST': '_viewRoot',
        'j_id115': 'j_id115',
        'javax.faces.ViewState': view_state,
        'j_id6:tblElementos:0:j_id35' : 'j_id6:tblElementos:0:j_id35',
    }
    resp = client.post(dhl_urls['print'], guide_data)
    resp = client.get('/generaImpresionPDF')
    with open(f'{guide_number}.pdf', 'wb') as f:
        f.write(resp.content)

def create_guide(client: Client, origin, destiny, details):
    try:
        guides_data = get_guides_data(client)
        if guides_data:  # Check if there are available guides
            select_data = select_guide(client, guides_data)
            client.post(dhl_urls['guide'], select_data)
            fill_data = fill_guide_table(client, origin, destiny, details)
            client.post(dhl_urls['capture'], fill_data)
            view_state = fill_data['javax.faces.ViewState']
            resp = confirm_capture(client, view_state)
            guide_number = force_percent(client, view_state)
            download_pdf(client, guide_number, view_state)

            if resp.ok:
                return resp
            else:
                return resp
        else:
            raise DhlmexException('No available guides')
    except HTTPError as httpe:
        raise httpe

    finally:
        client._logout()
