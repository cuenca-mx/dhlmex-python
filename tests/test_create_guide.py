import pytest

from dhlmex import get_guides_data
from dhlmex.exceptions import DhlmexException


@pytest.mark.vcr
def test_get_guide(client):
    guides = get_guides_data(client)
    client._logout()
    print("guides from test")
    print(guides)
    if guides:
        assert guides
    else:
        with pytest.raises(DhlmexException) as execinfo:
            assert str(execinfo.value) == f"No available guides"
