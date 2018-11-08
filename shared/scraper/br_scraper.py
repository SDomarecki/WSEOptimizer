import pandas as pd
import requests
from bs4 import BeautifulSoup

from shared.model.company import Company


class BRscraper:

    @staticmethod
    def get_companies():
        url = 'https://www.biznesradar.pl/gielda/akcje_gpw'
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        companies = {}
        for a in soup.find_all("a", class_="s_tt"):
            name = a['title']
            ticker = a.text.split(" ")[0]
            link = '/' + a['href'].split("/")[2]
            companies[ticker] = Company(name, ticker, link)
        return companies

    @staticmethod
    def get_sector(link: str):

        sector = ""
        url = 'https://www.biznesradar.pl/notowania' + link
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        sector = soup.find(text='Sektor:').parent.parent.findNext('td').contents[1].contents[0]
        return sector


    @staticmethod
    def get_fundamentals(link: str):
        df1 = BRscraper.get_raw_fundamentals(link)

        df2 = BRscraper.get_balance(link)

        df3 = BRscraper.get_value_indicators(link)

        df4 = BRscraper.get_profitability_indicators(link)

        fundamentals = pd.concat([df1, df2, df3, df4], axis=1, sort=False).sort_index(inplace=False)

        return fundamentals

    @staticmethod
    def get_raw_fundamentals(link: str):
        columns = ['Sales', 'Earnings']
        raw_fundamentals = pd.DataFrame(columns=columns)

        url = 'https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat' + link + ',Q'
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find("table", class_="report-table") is None:
            return raw_fundamentals
        tr = soup.find("table", class_="report-table").find_all("tr")

        seasons = tr[0].find_all("th")[1:-1]
        dates = []
        for season in seasons:
            dates.append(season.contents[0].strip())

        sales = tr[1].find_all("td")[1:-1]
        earnings = tr[5].findAll("td")[1:-1]

        for i in range(0, len(dates) - 1):
            date = dates[i]
            if sales[i].contents == [] or sales[i].contents[0].name == 'div':
                continue
            if earnings[i].contents == [] or earnings[i].contents[0].name == 'div':
                continue

            sale = sales[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            earning = earnings[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")

            raw_fundamentals.loc[date] = [float(sale), float(earning)]

        return raw_fundamentals

    @staticmethod
    def get_balance(link: str):
        columns = ['Book value']
        balance = pd.DataFrame(columns=columns)

        url = 'https://www.biznesradar.pl/raporty-finansowe-bilans' + link + ',Q,0'
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find("table", class_="report-table") is None:
            return balance
        tr = soup.find("table", class_="report-table").find_all("tr")

        seasons = tr[0].find_all("th")[1:-1]
        dates = []
        for season in seasons:
            dates.append(season.contents[0].strip())

        book_values = tr[16].findAll("td")[1:-1]

        for i in range(0, len(dates) - 1):
            date = dates[i]
            if book_values[i].contents == [] or book_values[i].contents[0].name == 'div':
                continue

            book_value = book_values[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")

            balance.loc[date] = [float(book_value)]

        return balance

    @staticmethod
    def get_value_indicators(link: str):
        columns = ['P/E', 'P/BV', 'P/S']
        indicators = pd.DataFrame(columns=columns)

        url = 'https://www.biznesradar.pl/wskazniki-wartosci-rynkowej' + link + ',Q'
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find("table", class_="report-table") is None:
            return indicators
        tr = soup.find("table", class_="report-table").find_all("tr")

        seasons = tr[0].find_all("th")[1:-1]
        dates = []
        for season in seasons:
            dates.append(season.contents[0].strip())

        p_es = tr[10].findAll("td")[1:-1]
        p_bvs = tr[4].findAll("td")[1:-1]
        p_ss = tr[8].findAll("td")[1:-1]

        for i in range(0, len(dates) - 1):
            date = dates[i]
            if p_es[i].contents == [] or p_es[i].contents[0].name == 'div':
                continue
            if p_bvs[i].contents == [] or p_bvs[i].contents[0].name == 'div':
                continue
            if p_ss[i].contents == [] or p_ss[i].contents[0].name == 'div':
                continue

            p_e = p_es[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            p_bv = p_bvs[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            p_s = p_ss[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")

            indicators.loc[date] = [float(p_e), float(p_bv), float(p_s)]

        return indicators

    @staticmethod
    def get_profitability_indicators(link: str):
        columns = ['ROE', 'ROA']
        indicators = pd.DataFrame(columns=columns)

        url = 'https://www.biznesradar.pl/wskazniki-rentownosci' + link
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find("table", class_="report-table") is None:
            return indicators
        tr = soup.find("table", class_="report-table").find_all("tr")

        seasons = tr[0].find_all("th")[1:-1]
        dates = []
        for season in seasons:
            dates.append(season.contents[0].strip())

        roes = tr[1].findAll("td")[1:-1]
        roas = tr[2].findAll("td")[1:-1]

        for i in range(0, len(dates) - 1):
            date = dates[i]
            if roes[i].contents == [] or roes[i].contents[0].name == 'div':
                continue
            if roas[i].contents == [] or roas[i].contents[0].name == 'div':
                continue

            roe = roes[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            roa = roas[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")

            indicators.loc[date] = [float(roe.strip('%'))/100, float(roa.strip('%'))/100]

        return indicators


def get_page(url):
    import time
    page = ''
    while page == '':
        try:
            print('Connecting with: ' + url)
            page = requests.get(url)
            break
        except:
            print("Za szybki request, ponawiam polaczenie")
            time.sleep(5)
            continue
    print('Success')
    return page
