from shared.model.company import Company
from shared.scraper.br_scraper import BRscraper
import pandas as pd
import io

fetched = 0
toFetch = 0


def create_database():
    global fetched
    global toFetch
    from multiprocessing.dummy import Pool as ThreadPool

    companies = BRscraper.get_companies()
    toFetch = len(companies)
    print('To fetch: ' + str(toFetch) + ' companies')
    pool = ThreadPool(4)

    companies = pool.map(collect_company_info, companies.values())
    return companies


def read_database(path_to_database: str):
    import json
    import os

    files = os.listdir(path_to_database + '/basic_info')

    companies = {}
    for file in files:
        with open(path_to_database + '/basic_info/' + file) as data_file:
            json_str = json.loads(data_file.read())
            company = company_decoder(json_str)

        ticker = file.split('.')[0]
        company.fundamentals = get_fundamentals(path_to_database, ticker)
        company.technicals = get_technicals(path_to_database, ticker)
        companies[ticker] = company
    return companies


def company_decoder(json) -> Company:
    return Company(json['name'], json['ticker'], json['link'])


def collect_company_info(company) -> Company:
    global fetched

    company.fundamentals = BRscraper.get_fundamentals(company.link)
    company.calculate_all_fundamentals()
    company.technicals = get_raw_technicals(company.ticker)
    company.convert_columns()
    company.calculate_all_technicals()
    company.convert_date_as_index()

    company.fundamentals.to_csv('fundamental2/' + company.ticker + '.csv')
    company.technicals.to_csv('technical2/' + company.ticker + '.csv')
    with io.open('basic_info/' + company.ticker + '.json', 'w') as f:
        f.write(company.toJSON())
    fetched += 1
    print('Fetched already ' + str(fetched) + '/' + str(toFetch) + ' companies')
    return company


def alt_create_database():
    print(BRscraper.get_fundamentals('OTMA'))


def get_raw_technicals(ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv('technical/' + ticker + '.csv', delimiter=';')
    return df


def get_fundamentals(path: str, ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv(path + '/fundamental2/' + ticker + '.csv', delimiter=',', index_col=0)
    return df


def get_technicals(path: str, ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv(path + '/technical2/' + ticker + '.csv', delimiter=',', index_col='Date')
    df.index = pd.to_datetime(df.index)
    return df


if __name__ == "__main__":
    read_database('basic_info')
