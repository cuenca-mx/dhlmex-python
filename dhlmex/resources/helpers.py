import re
from typing import Dict

from bs4 import BeautifulSoup
from requests import Response

from dhlmex import DhlmexException


def get_data(resp: Response, action: Dict) -> Dict:
    if 'Login / Admin' in resp.text:
        raise DhlmexException('Client not logged in')
    soup = BeautifulSoup(resp.text, features='html.parser')
    view_state = soup.find('input', id='javax.faces.ViewState').attrs['value']
    js = soup.find('a', text=action['text']).attrs['onclick']
    matches = re.findall(r"\'(.+?)\'", js)
    form_ids = [match for match in matches if match.startswith('j_id')]
    j_pair_id = form_ids[1].split(',')[0]
    j_id = form_ids[0]

    return {
        j_id: j_id,
        j_pair_id: action['code'],
        'javax.faces.ViewState': view_state,
        action['end']: action['end'],
    }
