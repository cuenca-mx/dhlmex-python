import re
from typing import ClassVar, Dict

from bs4 import BeautifulSoup
from requests import Response


class Resource:
    _client: ClassVar["dhlmex.Client"]  # type: ignore
    _urls: Dict[str, str] = {
        'login': '/jsp/app/login/login.xhtml',
        'home': '/jsp/app/inicio/inicio.xhtml',
        'guide': '/jsp/app/cliente/impresionClienteSubUsuario.xhtml',
        'capture': '/jsp/app/cliente/capturaDatosImpresionClienteSU.xhtml',
        'print': '/jsp/app/cliente/guiasImpresas.xhtml',
        'pdf': '/generaImpresionPDF',
    }
    _actions: Dict[str, Dict[str, str]] = {
        'close': {
            'text': 'Cerrar Sesión',
            'code': 'j_id9:j_id26',
            'end': 'j_id9:j_id30',
        },
        'print': {
            'text': 'Impresión Sub Usuario',
            'code': 'j_id9:j_id14',
            'end': 'j_id9:j_id16',
        },
        'download': {
            'text': 'Guías Impresas',
            'code': 'j_id9:j_id18',
            'end': 'j_id9:j_id10',
        },
    }

    @staticmethod
    def get_data(resp: Response, action: Dict) -> Dict:
        soup = BeautifulSoup(resp.text, features='html.parser')
        view_state = soup.find('input', id='javax.faces.ViewState').attrs[
            'value'
        ]
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
