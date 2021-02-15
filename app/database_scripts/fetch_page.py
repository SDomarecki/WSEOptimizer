import time

import requests


def fetch_page(url: str):
    page = ''
    while page == '':
        try:
            print(f'Connecting with: {url}')
            page = requests.get(url).text
            break
        except requests.exceptions.RequestException:
            print('Too fast request, reconnecting...')
            time.sleep(5)
            continue
    print('Success')
    return page
