import requests
from bs4 import BeautifulSoup as BS


def test_web_connection(url, timeout=10):
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.exceptions.RequestException as e:
        print(f'Error {e}')
        print(f'Skipping {url}')
        return False
    

def open_url(url, method, payload=None):
    if not test_web_connection(url):
        return

    if method == 'get':
        result = requests.get(url, params=payload)
    if method == 'post':
        result = requests.post(url, data=payload)
    result.encoding = result.apparent_encoding  #  The apparent encoding, provided by the charset_normalizer or chardet libraries.
    return BS(result.text, 'lxml', multi_valued_attributes=None)