import requests
from bs4 import BeautifulSoup as BS


def open_url(url, method, payload=None, timeout=10):
    try:
        if method == 'get':
            result = requests.get(url, params=payload, timeout=timeout)
        if method == 'post':
            result = requests.post(url, data=payload, timeout=timeout)
        result.encoding = result.apparent_encoding  #  The apparent encoding, provided by the charset_normalizer or chardet libraries.
        return BS(result.text, 'lxml', multi_valued_attributes=None)
    except requests.exceptions.RequestException as e:
        print(f'Error {e}')
        print(f'Skipping {url}')
        return
    

def create_ad(job, city, date):
    url_name = job.a.text.strip()  # Use ad text to create URL name.
    url = job.a['href']  # Link to the ad
    hyperlink_format = '<a href="{url}" target="_blank">{text}</a>'
    hyperlink = hyperlink_format.format(url=url, text=url_name)
    ads_dict = {'job_description': url_name, 'ad_url': url, 'city': city, 'date': date.today().strftime('%Y-%m-%d')}
    return ads_dict