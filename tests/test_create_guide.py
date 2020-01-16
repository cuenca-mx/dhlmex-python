import pytest

from dhlmex import Client


@pytest.mark.vcr
def test_get_guide():
    client = Client()
    guides = get_guides_data(client)
    if guides:
        assert guides
        assert 'AJAXREQUEST' in guides
    else:
        assert guides == {}
