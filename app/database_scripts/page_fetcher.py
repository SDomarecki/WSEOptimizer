import time

import requests
from bs4 import BeautifulSoup


class PageFetcher:
    def __init__(self):
        self.page = ""

    def fetch_and_parse(self, url: str) -> BeautifulSoup:
        self.fetch_page(url)
        soup = BeautifulSoup(self.page, "html.parser")
        return soup

    def fetch_page(self, url: str):
        self.page = ""
        tries = 0
        while self.page == "" and tries < 3:
            try:
                print(f"Connecting with: {url}")
                self.page = requests.get(url).text
            except requests.exceptions.RequestException:
                print("Request failed, reconnecting...")
                time.sleep(2)
                tries += 1
        if self.page == "":
            raise requests.exceptions.RequestException("Connection failed")
        print("Success")
