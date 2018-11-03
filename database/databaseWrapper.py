from shared.model.company import Company
from shared.scraper.br_scraper import BRscraper
import pandas as pd
import io


def create_database():
    from multiprocessing.dummy import Pool as ThreadPool

    companies = BRscraper.get_companies()

    pool = ThreadPool(4)

    companies = pool.map(collect_company_info, companies.values())
    return companies


def read_database():
    import json
    import os

    files = os.listdir('./basic_info')

    companies = []
    for file in files:
        with open('basic_info/' + file) as data_file:
            json_str = json.loads(data_file.read())
            company = company_decoder(json_str)

        ticker = file.split('.')[0]

        company.fundamentals = get_fundamentals(ticker)
        company.technicals = get_technicals(ticker)
        companies.append(company)
    return companies


def company_decoder(json) -> Company:
    return Company(json['name'], json['ticker'], json['link'])


def collect_company_info(company) -> Company:
    company.fundamentals = BRscraper.get_fundamentals(company.link)
    company.calculate_all_fundamentals()
    company.technicals = get_raw_technicals(company.ticker)
    company.calculate_all_technicals()
    company.convert_date_as_index()

    company.fundamentals.to_csv('fundamental2/' + company.ticker + '.csv')
    company.technicals.to_csv('technical2/' + company.ticker + '.csv')
    with io.open('basic_info/' + company.ticker + '.json', 'w') as f:
        f.write(company.toJSON())
    return company


def alt_create_database():
    print(BRscraper.get_fundamentals('OTMA'))


def get_raw_technicals(ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv('technical/' + ticker + '.csv', delimiter=',')
    return df


def get_fundamentals(ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv('fundamental2/' + ticker + '.csv', delimiter=',')
    return df


def get_technicals(ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv('technical2/' + ticker + '.csv', delimiter=',')
    return df


if __name__ == "__main__":
    create_database()
