import os
from typing import Any, ClassVar, Dict, Optional

from requests import HTTPError, Response, Session

from .exceptions import DhlmexException
from .resources import Resource
from .resources.helpers import get_data

API_URL = 'https://prepaid.dhl.com.mx/Prepago'
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
)
DHL_CERT = 'prepaid-dhl-com-mx.pem'


class Client:

    base_url: ClassVar[str] = API_URL
    headers: Dict[str, str]
    session: Session
    view_state: int = 1

    # resources
    ...

    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None,
    ):

        username = username or os.environ['DHLMEX_USERNAME']
        password = password or os.environ['DHLMEX_PASSWORD']
        self.session = Session()
        self.session.headers['User-Agent'] = USER_AGENT
        if os.getenv('DEBUG'):
            print(f'Client using Charles certificate')
            self.session.verify = DHL_CERT
        self._login(username, password)

        Resource._client = self

    def _login(self, username: str, password: str) -> Response:
        self.get('/')  # Initialize cookies
        endpoint = '/jsp/app/login/login.xhtml'
        data = {
            'AJAXREQUEST': '_viewRoot',
            'j_id6': 'j_id6',
            'j_id6:j_id20': username,
            'j_id6:j_id22': password,
            'javax.faces.ViewState': 'j_id1',
            'j_id6:j_id29': 'j_id6:j_id29',
        }
        try:
            resp = self.post(endpoint, data)
        except HTTPError as httpe:
            if 'Su sesión ha caducado' in resp.text:
                raise DhlmexException(f'Session for {username} has expired')
                # do something to revive the session
                # self.session.cookies.clear()
                # resp = self.post(endpoint, data)
            else:
                raise httpe
        # DHL always return 200 although the session has expired
        if 'Ya existe una sesión' in resp.text:
            raise DhlmexException(
                f'There is an exisiting session on DHL for {username}'
            )
        return resp

    def _logout(self) -> Response:
        endpoint = '/jsp/app/inicio/inicio.xhtml'
        data = get_data(
            self.post(endpoint, {})
        )  # Obtain headers to end properly the session
        try:
            resp = self.post(endpoint, data)
        except HTTPError as httpe:
            raise httpe
        return resp

    def get(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request('get', endpoint, {}, **kwargs)

    def post(
        self, endpoint: str, data: Dict[str, str], **kwargs: Any
    ) -> Response:
        return self.request('post', endpoint, data, **kwargs)

    def request(
        self, method: str, endpoint: str, data: Dict[str, str], **kwargs: Any,
    ) -> Response:
        url = self.base_url + endpoint
        response = self.session.request(method, url, data=data, **kwargs)
        # if response.status_code != 500:
        self.view_state += 1
        print(f'VIEWSTSATE: {self.view_state}')
        self._check_response(response)
        return response

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            return
        response.raise_for_status()
