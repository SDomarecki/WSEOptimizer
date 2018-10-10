import requests
from bs4 import BeautifulSoup


class StockDay:
    date = '01-01-2010'
    open = 1.0
    high = 1.0
    low = 1.0
    close = 1.0
    volume = 1.0
    circulation = 1.0

    def __init__(self, date, open, high, low, close, volume, circulation):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.circulation = circulation


class Company:
    name = 'Blank'
    ticker = 'BLK'
    link = '/null'
    stockDays = {}

    def __init__(self, name, ticker, link):
        self.name = name
        self.ticker = ticker
        self.link = link


class BRscraper:

    @staticmethod
    def getCompanies():
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
    def getPrices(company: Company):
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

            company.stockDays[date] = StockDay(date, open, high, low, close, volume, circulation)
            print(tr)
            print('chuj')


# testy
firmy = BRscraper.getCompanies()
for firma in firmy.values():
    print(firma.name + ' (' + firma.ticker + ') ' + firma.link)

BRscraper.getPrices(firmy['11B'])

for day in firmy['11B'].stockDays.values():
    print(day.circulation)
