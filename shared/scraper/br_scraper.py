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
    def get_fundamentals(link: str):
        columns = ['Sale', 'Earnings', 'Book value']
        fundamentals = pd.DataFrame(columns=columns)

        url = 'https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat' + link + ',Q'
        page = get_page(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find("table", class_="report-table") is None:
            return fundamentals
        tr = soup.find("table", class_="report-table").find_all("tr")

        url2 = 'https://www.biznesradar.pl/raporty-finansowe-bilans' + link + ',Q,0'
        page2 = get_page(url2)
        soup2 = BeautifulSoup(page2.text, 'html.parser')
        if soup2.find("table", class_="report-table") is None:
            return fundamentals
        tr2 = soup2.find("table", class_="report-table").find_all("tr")

        seasons = tr[0].find_all("th")[1:-1]
        dates = []
        for season in seasons:
            dates.append(season.contents[0].strip())

        sales = tr[1].find_all("td")[1:-1]
        earnings = tr[5].findAll("td")[1:-1]
        book_values = tr2[16].findAll("td")[1:-1]

        for i in range(0, len(dates) - 1):
            date = dates[i]
            if sales[i].contents == [] or sales[i].contents[0].name == 'div':
                continue
            if book_values[i].contents == [] or book_values[i].contents[0].name == 'div':
                continue
            if earnings[i].contents == [] or earnings[i].contents[0].name == 'div':
                continue

            sale = sales[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            earning = earnings[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            book_value = book_values[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            fundamentals.loc[date] = [float(sale), float(earning), float(book_value)]

        return fundamentals


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
