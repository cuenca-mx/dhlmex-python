import pytest

from dhlmex.exceptions import DhlmexException


@pytest.mark.vcr
def test_invalid_postal_code(client, origin, invalid_destination, details):

    with pytest.raises(DhlmexException) as execinfo:
        client.guides.create_guide(origin, invalid_destination, details)
        assert str(execinfo.value) == f'Invalid destiny postal code'
