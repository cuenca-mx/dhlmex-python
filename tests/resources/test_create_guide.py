import pytest


@pytest.mark.vcr
def test_get_guide(client, origin, destination, details):
    guide_number, file_path = client.guides.create_guide(
        origin, destination, details
    )
    assert guide_number is not None
    assert file_path is not None
