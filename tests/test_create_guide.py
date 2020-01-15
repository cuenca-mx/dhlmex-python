import pytest

from dhlmex import get_guides_data


@pytest.mark.vcr
def test_get_guide(client):
    guides = get_guides_data(client)
    if guides:
        assert guides
        assert 'AJAXREQUEST' in guides
    else:
        assert guides == {}
