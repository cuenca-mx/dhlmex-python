import pytest

from dhlmex import get_guides_data
from dhlmex.exceptions import DhlmexException


@pytest.mark.vcr
def test_get_guide(client):
    guides = get_guides_data(client)
    if guides:
        assert guides
        assert 'AJAXREQUEST' in guides
    else:
        assert guides == {}


#@pytest.mark.vcr
# def test_create_guide(client):
#     pass
#     else:
#         with pytest.raises(DhlmexException) as execinfo:
#             assert str(execinfo.value) == f"No available guides"