import pytest

from database_scripts.page_fetcher import PageFetcher


def test_fetch_page_validURL_returnsExistingPage():
    url = 'https://www.biznesradar.pl'
    fetcher = PageFetcher()
    page = fetcher.fetch_page(url)

    assert page.startswith('<!DOCTYPE html>')


def test_fetch_page_invalidURL_throwsException():
    url = 'https://randomstringofnonexistentpage.net'
    fetcher = PageFetcher()

    with pytest.raises(Exception):
        page = fetcher.fetch_page(url)
    assert False