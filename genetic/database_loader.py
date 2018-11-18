import pandas as pd

from shared.company import Company


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

    sectors = []
    for company in companies.values():
        if company.sector not in sectors:
            sectors.append(company.sector)
    print(sectors)

    return companies


def company_decoder(json) -> Company:
    company = Company(json['name'], json['ticker'], json['link'])
    company.sector = json['sector']
    return company


def get_fundamentals(path: str, ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv(path + '/fundamental/' + ticker + '.csv', delimiter=',', index_col=0)
    return df


def get_technicals(path: str, ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv(path + '/technical/' + ticker + '.csv', delimiter=',', index_col='Date')
    df.index = pd.to_datetime(df.index)
    return df
