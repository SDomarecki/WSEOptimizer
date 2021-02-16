import pandas as pd
from bs4 import BeautifulSoup

from app.database_scripts.fetch_page import fetch_page
from database_scripts.company import Company


class BRscraper:
    root_url = 'https://www.biznesradar.pl'
    main_list_url = f'{root_url}/gielda/akcje_gpw'
    company_sector_url_base = f'{root_url}/notowania'
    raw_fundamentals_url_base = f'{root_url}/raporty-finansowe-rachunek-zyskow-i-strat'
    balance_url_base = f'{root_url}/raporty-finansowe-bilans'
    value_url_base = f'{root_url}/wskazniki-wartosci-rynkowej'
    profitability_url_base = f'{root_url}/wskazniki-rentownosci'

    def get_companies(self) -> dict:
        url = BRscraper.main_list_url
        page = self._fetch_and_parse(url)

        companies = {}
        for a in page.find_all('a', class_='s_tt'):
            name = a['title']
            ticker = a.text.split(' ')[0]
            link = '/' + a['href'].split('/')[2]
            companies[ticker] = Company(name, ticker, link)
        return companies

    def get_sector(self, link: str) -> str:
        url = f'{BRscraper.company_sector_url_base}{link}'
        page = self._fetch_and_parse(url)
        sector = page.find(text='Sektor:').parent.parent.findNext('td').contents[1].contents[0]
        return sector

    def get_fundamentals(self, link: str) -> pd.DataFrame:
        df1 = self.get_raw_fundamentals(link)
        df2 = self.get_balance(link)
        df3 = self.get_value_indicators(link)
        df4 = self.get_profitability_indicators(link)

        fundamentals = pd.concat([df1, df2, df3, df4], axis=1, sort=False).sort_index(inplace=False)
        return fundamentals

    def get_raw_fundamentals(self, link: str):
        indicators_name_and_locations = {
            'Sales': 2,
            'Earnings': 6
        }
        url = f'{BRscraper.raw_fundamentals_url_base}{link},Q'
        return self._get_indicators_from_link_and_positions(indicators_name_and_locations, url)

    def get_balance(self, link: str):
        indicators_name_and_locations = {
            'Book value': 17
        }
        url = f'{BRscraper.balance_url_base}{link},Q'
        return self._get_indicators_from_link_and_positions(indicators_name_and_locations, url)

    def get_value_indicators(self, link: str) -> pd.DataFrame:
        indicators_name_and_locations = {
            'P/E': 10,
            'P/BV': 4,
            'P/S': 8,
            'EPS': 9,
            'BVPS': 3,
            'SPS': 7,
        }
        url = f'{BRscraper.value_url_base}{link},Q'
        return self._get_indicators_from_link_and_positions(indicators_name_and_locations, url)

    def get_profitability_indicators(self, link: str) -> pd.DataFrame:
        indicators_name_and_locations = {
            'ROE': 1,
            'ROA': 2,
        }
        url = f'{BRscraper.profitability_url_base}{link},Q'
        return self._get_indicators_from_link_and_positions(indicators_name_and_locations, url)

    def _get_indicators_from_link_and_positions(self, name_and_loc, url) -> pd.DataFrame:
        indicators = pd.DataFrame(columns=list(name_and_loc))

        page = self._fetch_and_parse(url)
        table = page.find('table', class_='report-table')
        if table is None:
            return indicators
        else:
            tr = table.find_all('tr')

        seasons = self._get_seasons_from_first_row(tr[0])
        indicator_rows = [tr[location].find_all('td')[1:-1] for location in name_and_loc.values()]

        for i in range(0, len(seasons) - 1):
            season = seasons[i]
            indicators.loc[season] = [float(self._fetch_one_indicator_from_html(row[i])) for row in indicator_rows]

        return indicators

    def _fetch_one_indicator_from_html(self, html) -> float:
        if html.text == '':
            return 0.0
        ind = html.contents[0].contents[0].contents[0].contents[0].strip().replace(' ', '')
        if '%' in ind:
            return float(ind.strip('%'))
        else:
            return float(ind)

    def _fetch_and_parse(self, url: str) -> BeautifulSoup:
        page = fetch_page(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def _get_seasons_from_first_row(self, row):
        headers = row.find_all('th')[1:-1]
        seasons = []
        for header in headers:
            seasons.append(header.contents[0].strip())
        return seasons
