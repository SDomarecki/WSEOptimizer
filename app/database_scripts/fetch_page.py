import time

import requests


def fetch_page(url: str) -> str:
    page = ''
    tries = 0
    while page == '' and tries < 3:
        try:
            print(f'Connecting with: {url}')
            page = requests.get(url).text
        except requests.exceptions.RequestException:
            print('Request failed, reconnecting...')
            time.sleep(2)
            tries += 1
    if page == '':
        raise Exception('Connection failed')
    print('Success')
    return page
