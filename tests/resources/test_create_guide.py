import pytest


@pytest.mark.vcr
def test_get_guide(client, origin, destination, details):
    guide_number, file_path = client.guides.create_guide(
        origin, destination, details, download=True
    )
    assert guide_number is not None
    assert file_path is not None


@pytest.mark.vcr
def test_get_guide_bytes(client, origin, destination, details):
    guide_number, guide_bytes = client.guides.create_guide(
        origin, destination, details, download=False
    )
    assert guide_number is not None
    assert guide_bytes is not None
