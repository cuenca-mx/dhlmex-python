import pytest


@pytest.mark.vcr
def test_get_guide_bytes(client, origin, destination, details):
    guide_number, guide_bytes = client.guides.create_guide(
        origin, destination, details
    )
    assert guide_number is not None
    assert guide_bytes is not None
