import os

import pytest
from bs4 import BeautifulSoup

from dhlmex import Client
from dhlmex.exceptions import DhlmexException

DHLMEX_USERNAME = os.environ['DHLMEX_USERNAME']
DHLMEX_PASSWORD = os.environ['DHLMEX_PASSWORD']


@pytest.mark.vcr
def test_successful_login(site_urls):
    # Just need to make sure it doesn't throw an exception
    client = Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
    resp = client.get(site_urls['home'])
    soup = BeautifulSoup(resp.text, features='html.parser')
    client._logout()
    assert resp.status_code == 200
    assert 'Administrar' in soup.find('title').text


@pytest.mark.vcr
def test_invalid_creds():
    with pytest.raises(DhlmexException) as execinfo:
        client = Client('invalidUsername', 'invalidPassword')
        assert str(execinfo.value) == f'Invalid credentials'
        assert client


def test_debug_login():
    os.environ['DEBUG'] = 'True'
    with pytest.raises(DhlmexException) as execinfo:
        client = Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
        assert (
            str(execinfo.value) == f'Client on debug, but Charles not running'
        )
        assert client.session.cert
        client._logout()
    os.environ['DEBUG'] = ''


@pytest.mark.vcr
def test_client_log_out():
    client = Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
    resp = client._logout()
    soup = BeautifulSoup(resp.text, features='html.parser')
    assert resp.status_code == 200
    assert 'Administrar' not in soup.find('title').text
    assert 'Login' in soup.find('title').text


@pytest.mark.vcr
def test_existing_session(site_urls):
    client = Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
    resp = client.get(site_urls['home'])
    assert resp.status_code == 200

    with pytest.raises(DhlmexException) as execinfo:
        client = Client(DHLMEX_USERNAME, DHLMEX_PASSWORD)
        assert (
            str(execinfo.value)
            == f'There is an exisiting session on DHL for {DHLMEX_USERNAME}'
        )

    client._logout()
