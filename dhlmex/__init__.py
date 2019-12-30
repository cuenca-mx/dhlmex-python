__all__ = ['__version__', 'Client']

from bs4 import BeautifulSoup
from requests import HTTPError

from .client import Client
from .version import __version__

from dhlmex.resources.urls import dhl_urls


def get_guides(client: Client) -> int:
    guides = 0
    endpoint = dhl_urls['home']
    data = {
            'j_id9': 'j_id9',
            'j_id9:j_id10': 'j_id9:j_id14',
            'javax.faces.ViewState': 'j_id2',
            'j_id9:j_id16': 'j_id9:j_id16',
        }
    client.post(endpoint, data)
    resp = client.get(dhl_urls['guide'])
    soup = BeautifulSoup(resp.text, features='html.parser')
    table = soup.find('table', id='j_id6:pnlOrdenesEncontradas')
    table_body = table.find('tbody')
    result = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        result.append([ele for ele in cols if ele])
    print(f'RESULT: \n {result}')
    return guides


def create_guide(agent: str, agentPass: str ):
    try:
        client = Client(agent, agentPass)

        if get_guides(client) != 0:
            print(f'Yup!')
        else:
            print(f'No available guides')
    except HTTPError as httpe:
        print(f'ERROR:{dir(httpe)}')
        print(f'ERROR:{httpe}')

    finally:
        client._logout()
