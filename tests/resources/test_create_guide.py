import pytest

from dhlmex.exceptions import DhlmexException


@pytest.mark.vcr
def test_get_guide_bytes(client, origin, destination, details):
    guide_number, guide_bytes = client.guides.create_guide(
        origin, destination, details
    )
    assert guide_number is not None
    assert guide_bytes is not None


@pytest.mark.vcr
def test_get_invalid_guide(client, origin, fake_destination, details):
    with pytest.raises(DhlmexException) as execinfo:
        guide_number, guide_bytes = client.guides.create_guide(
            origin, fake_destination, details
        )
        assert str(execinfo.value) == f' Error while capturing guide data'
        assert guide_number is None
        assert guide_bytes is None
