from typing import Dict

from dhlmex.exceptions import DhlmexException
from dhlmex.resources.destination import Destination
from dhlmex.resources.origin import Origin

from .base import Resource


class PostCode(Resource):
    @classmethod
    def validate_postal_codes(
        cls, origin: Origin, destination: Destination, view_state: str
    ):
        post_code = cls()
        return post_code._validate_postal_codes(
            origin, destination, view_state
        )

    def _validate_postal_codes(
        self, origin: Origin, destination: Destination, view_state: str
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
            'datos:j_id36': origin.postal_code,
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
        resp = self._client.post(self._urls['capture'], fill_data)
        if 'Código Postal válido' in resp.text:
            fill_data.pop('datos:j_id37')
            # validate also destiny postal_code
            fill_data['datos:j_id76'] = 'datos:j_id76'
            fill_data['datos:j_id75'] = destination.postal_code
            resp = self._client.post(self._urls['capture'], fill_data)
            if 'Código Postal válido' in resp.text:
                fill_data.pop('datos:j_id76')
                return fill_data
            else:
                raise DhlmexException('Invalid destiny postal code')
        else:
            raise DhlmexException('Invalid origin postal code')
