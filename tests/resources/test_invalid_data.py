import pytest

from dhlmex.exceptions import DhlmexException


@pytest.mark.vcr
def test_invalid_destination(client, origin, invalid_destination, details):
    with pytest.raises(DhlmexException) as execinfo:
        client.guides.create_guide(origin, invalid_destination, details)
        assert str(execinfo) == 'Error while creating guide'


@pytest.mark.vcr
def test_invalid_postal_code(client, origin, invalid_postal_code, details):
    with pytest.raises(DhlmexException) as execinfo:
        client.guides.create_guide(origin, invalid_postal_code, details)
        assert str(execinfo.value) == 'Invalid destiny postal code'


@pytest.mark.vcr
def test_missing_city(client, origin, missing_data, details):
    with pytest.raises(DhlmexException) as execinfo:
        client.guides.create_guide(origin, missing_data, details)
        assert str(execinfo.value) == 'Invalid value'
