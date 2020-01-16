import pytest


@pytest.mark.vcr
def test_get_guide(client):
    resp = client.guides.create_guide()
    # TODO Agregar asserts aquí
