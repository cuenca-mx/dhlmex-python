import logging
import os
from typing import Any, ClassVar, Dict, Optional

from requests import HTTPError, Response, Session, codes
from requests.exceptions import SSLError

from .exceptions import DhlmexException
from .resources import Guide, PostCode, Resource

PREPAID_URL = 'https://prepaid.dhl.com.mx/Prepago'
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
)
DHL_CERT = 'prepaid-dhl-com-mx.pem'

logging.basicConfig(level=logging.DEBUG)


class Client:

    base_url: ClassVar[str] = PREPAID_URL
    headers: Dict[str, str]
    session: Session

    # resources
    guides: ClassVar = Guide
    post_codes: ClassVar = PostCode

    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None,
    ):

        username = username or os.environ['DHLMEX_USERNAME']
        password = password or os.environ['DHLMEX_PASSWORD']
        self.session = Session()
        self.session.headers['User-Agent'] = USER_AGENT
        if os.getenv('DEBUG'):
            logging.debug(f'Client using Charles certificate')
            self.session.verify = DHL_CERT
        self._login(username, password)

        Resource._client = self

    def _login(self, username: str, password: str) -> Response:
        try:
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
            resp = self.post(endpoint, data)
        except HTTPError as httpe:
            if 'Su sesión ha caducado' in resp.text:
                raise DhlmexException('Session has expired')
            else:
                raise httpe
        except SSLError:
            raise DhlmexException('Client on debug, but Charles not running')
        # DHL always return 200 although there is an existing session
        if 'Ya existe una sesión' in resp.text:
            raise DhlmexException(
                f'There is an exisiting session on DHL for {username}'
            )
        if 'Verifique su usuario' in resp.text:
            raise DhlmexException('Invalid credentials')
        return resp

    def _logout(self) -> Response:
        endpoint = '/jsp/app/inicio/inicio.xhtml'
        resp = self.post(endpoint, {})
        if 'Login / Admin' in resp.text:
            return resp  # No need to logout
        data = Resource.get_data(
            resp, Resource._actions['close'],
        )  # Obtain headers to end properly the session
        try:
            resp = self.post(endpoint, data)
        except HTTPError as httpe:
            if 'Su sesión ha caducado' in httpe.response.text:
                resp = Response()
                resp.status_code = codes.ok
                return resp
            else:
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
        self._check_response(response)
        return response

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            return
        response.raise_for_status()
