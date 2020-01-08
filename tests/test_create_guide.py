import pytest

from dhlmex import Client, get_guides_data


@pytest.mark.vcr
def test_create_guide():
    client = Client()
    guides = get_guides_data(client)
    assert guides
    client._logout()
