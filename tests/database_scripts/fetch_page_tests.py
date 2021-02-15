import pytest

from database_scripts.fetch_page import fetch_page


def test_fetch_page_validURL_returnsExistingPage():
    url = 'https://www.biznesradar.pl'
    page = fetch_page(url)
    assert page.startswith('<!DOCTYPE html>')


def test_fetch_page_invalidURL_throwsException():
    url = 'https://randomstringofnonexistentpage.net'

    with pytest.raises(Exception):
        page = fetch_page(url)
