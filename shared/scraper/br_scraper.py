import requests
from bs4 import BeautifulSoup

from shared.model.company import Company
from shared.model.technical import Technical
from shared.model.fundamental import Fundamental


class BRscraper:

    @staticmethod
    def get_companies():
        page = requests.get('https://www.biznesradar.pl/gielda/akcje_gpw')
        soup = BeautifulSoup(page.text, 'html.parser')
        companies = {}
        for a in soup.find_all("a", class_="s_tt"):
            name = a['title']
            ticker = a.text.split(" ")[0]
            link = '/' + a['href'].split("/")[2]
            companies[ticker] = Company(name, ticker, link)
        return companies

    @staticmethod
    def get_prices(company: Company):
        url = 'https://www.biznesradar.pl/notowania-historyczne' + company.link
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for tr in soup.find("table", class_="qTableFull").find_all("tr")[1:]:
            date = tr.contents[1].contents[0]
            open = tr.contents[3].contents[0]
            high = tr.contents[5].contents[0]
            low = tr.contents[7].contents[0]
            close = tr.contents[9].contents[0]
            volume = tr.contents[11].contents[0]
            circulation = tr.contents[13].contents[0]

            company.append_base_technical(date, Technical(date, open, high, low, close, volume, circulation))

    @staticmethod
    def get_fundamentals(link: str):
        url = 'https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat' + link + ',Q'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        tr = soup.find("table", class_="report-table").find_all("tr")

        url2 = 'https://www.biznesradar.pl/raporty-finansowe-bilans/' + link + ',Q,0'
        page2 = requests.get(url2)
        soup2 = BeautifulSoup(page2.text, 'html.parser')
        tr2 = soup2.find("table", class_="report-table").find_all("tr")

        seasons = tr[0].find_all("th")[1:-1]
        dates = []
        for season in seasons:
            dates.append(get_date_from_season(season.contents[0].strip()))

        sales = tr[1].find_all("td")[1:-1]
        earnings = tr[5].findAll("td")[1:-1]
        book_values = tr2[16].findAll("td")[1:-1]

        fundamentals = {}
        for i in range(0, len(dates)-1):
            date = dates[i]
            print(sales[i].contents)
            if sales[i].contents == [] or sales[i].contents[0].name == 'div':
                continue
            if book_values[i].contents == [] or book_values[i].contents[0].name == 'div':
                continue

            sale = sales[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            earning = earnings[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            book_value = book_values[i].contents[0].contents[0].contents[0].contents[0].strip().replace(" ", "")
            fundamentals[date] = Fundamental(date, float(sale), float(earning), float(book_value))

        return fundamentals


def get_date_from_season(season: str):
    year_and_season = season.split("/")
    if year_and_season[1] == "Q1":
        return year_and_season[0] + "-05-31"
    elif year_and_season[1] == "Q2":
        return year_and_season[0] + "-08-31"
    elif year_and_season[1] == "Q3":
        return year_and_season[0] + "-11-30"
    else:
        return year_and_season[0] + "-02-28"


# testy
firmy = BRscraper.get_companies()
for firma in firmy.values():
    print('[' + firma.ticker + '] ' + firma.name + ' @ ' + firma.link)

BRscraper.get_prices(firmy['11B'])
#
# for day in firmy['11B'].stockDays.values():
#     print(day.circulation)
