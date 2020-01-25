import pytest

from dhlmex.exceptions import DhlmexException


@pytest.mark.vcr
def test_invalid_destination(client, origin, invalid_destination, details):

    with pytest.raises(DhlmexException) as execinfo:
        client.guides.create_guide(origin, invalid_destination, details, False)
        assert str(execinfo) == 'Error while creating guide'


@pytest.mark.vcr
def test_invalid_postal_code(client, origin, invalid_postal_code, details):

    with pytest.raises(DhlmexException) as execinfo:
        client.guides.create_guide(origin, invalid_postal_code, details, False)
        assert str(execinfo.value) == 'Invalid destiny postal code'
