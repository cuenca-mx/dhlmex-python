import os
from typing import Any, ClassVar, Dict, Optional, Tuple, Union

from requests import Response, Session

API_URL = 'https://api.getmati.com'


class Client:

    base_url: ClassVar[str] = API_URL
    basic_auth_creds: Tuple[str, str]
    bearer_tokens: Dict[Union[None, str], AccessToken]
    headers: Dict[str, str]
    session: Session

    # resources
    access_tokens: ClassVar = AccessToken
    identities: ClassVar = Identity
    user_validation_data: ClassVar = UserValidationData
    verifications: ClassVar = Verification

    def __init__(
        self, api_key: Optional[str] = None, secret_key: Optional[str] = None
    ):
        self.session = Session()
        self.headers = {'User-Agent': f'mati-python/{client_version}'}
        api_key = api_key or os.environ['MATI_API_KEY']
        secret_key = secret_key or os.environ['MATI_SECRET_KEY']
        self.basic_auth_creds = (api_key, secret_key)
        self.bearer_tokens = {}
        Resource._client = self

    def get_valid_bearer_token(
        self, score: Optional[str] = None
    ) -> AccessToken:
        try:
            expired = self.bearer_tokens[score].expired
        except KeyError:
            expired = True
        if expired:  # renew token
            self.bearer_tokens[score] = self.access_tokens.create(score)
        return self.bearer_tokens[score]

    def get(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('get', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('post', endpoint, **kwargs)

    def request(
        self,
        method: str,
        endpoint: str,
        auth: Union[str, AccessToken, None] = None,
        token_score: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        url = self.base_url + endpoint
        auth = auth or self.get_valid_bearer_token(token_score)
        headers = {**self.headers, **dict(Authorization=str(auth))}
        response = self.session.request(method, url, headers=headers, **kwargs)
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            return
        response.raise_for_status()
