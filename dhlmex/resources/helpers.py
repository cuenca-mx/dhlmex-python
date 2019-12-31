import re
from typing import Dict

from bs4 import BeautifulSoup
from requests import Response


def get_data(resp: Response) -> Dict:
    soup = BeautifulSoup(resp.text, features='html.parser')
    js = soup.find('td', text='Cerrar Sesión').find('a').attrs['onclick']
    matches = re.findall(r"\'(.+?)\'", js)
    form_ids = [match for match in matches if match.startswith('j_id')]
    j_pair_id = form_ids[1].split(',')[0]
    j_id = form_ids[0]
    form = soup.find('form', id='j_id9')
    view_state = form.find('input', id='javax.faces.ViewState').attrs['value']

    return {
        j_id: j_id,
        j_pair_id: 'j_id9:j_id26',
        'javax.faces.ViewState': view_state,
        'j_id9:j_id30': 'j_id9:j_id30',
    }
