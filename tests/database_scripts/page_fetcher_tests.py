import pytest
from bs4 import BeautifulSoup
from requests import RequestException

from app.database_scripts.page_fetcher import PageFetcher


def test_fetch_and_parse_validURL_returnsSoup():
    url = "https://www.biznesradar.pl"
    fetcher = PageFetcher()
    soup = fetcher.fetch_and_parse(url)

    assert isinstance(soup, BeautifulSoup)


def test_fetch_page_validURL_returnsExistingPage():
    url = "https://www.biznesradar.pl"
    fetcher = PageFetcher()
    page = fetcher.fetch_page(url)

    assert page.startswith("<!DOCTYPE html>")


def test_fetch_page_invalidURL_throwsException():
    url = "https://randomstringofnonexistentpage.net"
    fetcher = PageFetcher()

    with pytest.raises(RequestException):
        fetcher.fetch_page(url)
