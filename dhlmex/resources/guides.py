import re
from time import sleep
from typing import Dict, Optional, Tuple

from bs4 import BeautifulSoup
from requests import HTTPError, Response

from dhlmex.exceptions import DhlmexException
from dhlmex.resources.origin import Origin

from .base import Resource
from .destination import Destination
from .order_details import OrderDetails


class Guide(Resource):
    @classmethod
    def create_guide(
        cls, origin: Origin, destination: Destination, details: OrderDetails,
    ) -> Tuple[str, Optional[bytes]]:
        guide = cls()
        try:
            guides_data = guide._get_guide_data()
            if guides_data:
                guide._select_guide(guides_data)
                view_state = guide._fill_guide_table(
                    origin, destination, details
                )
                guide._confirm_capture(view_state)
                guide_number = guide._force_percent(view_state)
                guide_bytes = guide._download_pdf(guide_number)
                return guide_number, guide_bytes
            else:
                raise DhlmexException('No available guides')
        except HTTPError as httpe:
            raise httpe

    def _get_guide_data(self) -> Dict:
        resp = self._client.post(self._urls['home'], {})
        data = self.get_data(resp, self._actions['print'])
        soup = BeautifulSoup(resp.text, features='html.parser')
        field = soup.find('input', id=re.compile('panelBarInput')).attrs[
            'name'
        ]
        data[field] = self._actions['print']['code']
        guides_data = {}
        resp = self._client.post(self._urls['home'], data)
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

    def _select_guide(self, guides_data: Dict) -> Dict:
        resp = self._client.post(self._urls['guide'], guides_data)
        soup = BeautifulSoup(resp.text, features='html.parser')
        view_state = soup.find('input', id='javax.faces.ViewState').attrs[
            'value'
        ]
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
        self._client.post(self._urls['guide'], select_data)
        select_data.pop(j_pair_id, None)
        select_data.pop('AJAX:EVENTS_COUNT', None)
        select_data[
            'j_id6:btnGuardarCotizacion'
        ] = 'j_id6:btnGuardarCotizacion'
        self._client.post(self._urls['guide'], select_data)
        return select_data

    def _fill_guide_table(
        self, origin: Origin, destination: Destination, details: OrderDetails
    ) -> str:
        resp = self._client.get(self._urls['capture'])
        soup = BeautifulSoup(resp.text, features='html.parser')
        view_state = soup.find('input', id='javax.faces.ViewState').attrs[
            'value'
        ]
        fill_data = self._client.post_codes.validate_postal_codes(
            origin, destination, view_state
        )
        fill_data['datos:j_id15'] = origin.company
        fill_data['datos:j_id19'] = origin.contact
        fill_data['datos:emailOrigen'] = origin.email
        fill_data['datos:j_id24'] = origin.phone
        fill_data['datos:j_id28'] = origin.address1
        fill_data['datos:j_id36'] = origin.postal_code
        fill_data['datos:j_id41'] = origin.neighborhood
        fill_data['datos:j_id45'] = origin.city
        fill_data['datos:j_id49'] = origin.state
        fill_data['datos:j_id54'] = destination.company
        fill_data['datos:j_id58'] = destination.contact
        fill_data['datos:emailDestino'] = destination.email
        fill_data['datos:j_id63'] = destination.phone
        fill_data['datos:j_id67'] = destination.address1
        fill_data['datos:j_id75'] = destination.postal_code
        fill_data['datos:j_id80'] = destination.neighborhood
        fill_data['datos:j_id84'] = destination.city
        fill_data['datos:j_id88'] = destination.state
        fill_data['datos:j_id71'] = details.description
        fill_data['datos:j_id93'] = details.content
        fill_data['javax.faces.ViewState'] = view_state
        fill_data['datos:j_id105'] = 'datos:j_id105'

        msg = self._validate_data(fill_data)
        if msg:
            raise DhlmexException(f'Invalid data: {msg}')
        else:
            return fill_data['javax.faces.ViewState']

    def _validate_data(self, fill_data: Dict) -> str:
        resp = self._client.post(self._urls['capture'], fill_data)
        msg = ''
        if 'messageError' in resp.text:
            soup = BeautifulSoup(resp.text, features='html.parser')
            msg = soup.find('span', {'class': 'rich-messages-label'}).text
        return msg

    def _confirm_capture(self, view_state: str) -> Response:
        confirm_data = {
            'AJAXREQUEST': '_viewRoot',
            'j_id109': 'j_id109',
            'javax.faces.ViewState': view_state,
            'j_id109:j_id112': 'j_id109:j_id112',
        }
        return self._client.post(self._urls['capture'], confirm_data)

    def _force_percent(self, view_state: str, retries: int = 20) -> str:
        force_data = {
            'AJAXREQUEST': '_viewRoot',
            'j_id115': 'j_id115',
            'javax.faces.ViewState': view_state,
            'j_id115:pb_sub': 'j_id115:pb_sub',
            'forcePercent': 'complete',
            'ajaxSingle': 'j_id115:pb_sub',
        }
        guide_number = ''
        while retries:
            resp = self._client.post(self._urls['capture'], force_data)
            if 'Procesada correctamente' in resp.text:
                soup = BeautifulSoup(resp.text, features='html.parser')
                guide_number = soup.find(
                    'td', id='j_id115:tblElementos:0:j_id123'
                ).text
                break
            else:
                sleep(1)
                retries -= 1
        if retries == 0:
            raise DhlmexException('Error while capturing guide data')
        return guide_number

    def _move_page(self, view_state: str, page: str) -> Response:
        final_data = {
            'AJAXREQUEST': '_viewRoot',
            'j_id6': 'j_id6',
            'javax.faces.ViewState': view_state,
            'ajaxSingle': 'j_id6:j_id37',
            'j_id6:j_id37': page,
            'AJAX:EVENTS_COUNT': '1',
        }
        return self._client.post(self._urls['print'], final_data)

    def _download_pdf(self, guide_number: str) -> Optional[bytes]:
        resp = self._client.post(self._urls['home'], {})
        data = self.get_data(resp, self._actions['download'])
        resp = self._client.post(self._urls['home'], data)
        if guide_number not in resp.text:  # search on last page
            soup = BeautifulSoup(resp.text, features='html.parser')
            view_state = soup.find('input', id='javax.faces.ViewState').attrs[
                'value'
            ]
            pages = len(
                soup.find("div", {"class": "rich-datascr"}).find_all('td')
            )
            resp = self._move_page(view_state, 'last')
            for _ in range(pages):
                if guide_number not in resp.text:  # search previous pages
                    resp = self._move_page(view_state, 'previous')
                else:
                    break
        if guide_number not in resp.text:
            raise DhlmexException(f'Guide {guide_number} not found')
        soup = BeautifulSoup(resp.text, features='html.parser')
        view_state = soup.find('input', id='javax.faces.ViewState').attrs[
            'value'
        ]
        td = soup.find('td', text=guide_number)
        tds = [td for td in td.next_siblings]
        j_pair_id = tds[-1].find('a').attrs['id']

        guide_data = {
            'AJAXREQUEST': '_viewRoot',
            'j_id6': 'j_id6',
            'javax.faces.ViewState': view_state,
            j_pair_id: j_pair_id,
        }
        self._client.post(self._urls['print'], guide_data)
        resp = self._client.get(self._urls['pdf'])
        if resp.ok:
            return resp.content
        else:
            return None
