import time

import requests
from bs4 import BeautifulSoup


class PageFetcher:
    def fetch_and_parse(self, url: str) -> BeautifulSoup:
        page = self.fetch_page(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def fetch_page(self, url: str) -> str:
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
