from decimal import Decimal

import pandas as pd

from shared.company import Company
from shared.config import Config


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

    companies = filter_database(companies)

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


def filter_database(database):
    # TODO
    min_circulation = Config.min_circulation
    max_circulation = Config.max_circulation

    to_delete = []

    import pandas as pd
    for company in database.values():
        company.technicals = pd.concat([company.technicals.loc[Config.start_date:Config.end_date],
                                        company.technicals.loc[
                                        Config.validation_start_date:Config.validation_end_date]])

        circulation_mean = float(company.technicals['Circulation'].mean())
        if min_circulation != -1 and circulation_mean < Config.min_circulation:
            to_delete.append(company.ticker)
        if max_circulation != -1 and circulation_mean > Config.max_circulation:
            to_delete.append(company.ticker)

    for ticker in to_delete:
        del database[ticker]
    database = filter_by_company_name(database)
    database = filter_by_sector(database)
    return database


def filter_by_company_name(database):
    return database


def filter_by_sector(database):
    sectors = Config.sectors
    to_delete = []

    if sectors[0] == 'All':
        return database

    for company in database.values():
        if company.sector not in sectors:
            to_delete.append(company.ticker)

    for ticker in to_delete:
        del database[ticker]
    return database


def get_target_ratio(ticker: str, start_date, end_date, path_to_database):
    ticker = ticker.lower()
    df = pd.read_csv(path_to_database + '/benchmarks/' + ticker + '.csv',
                     delimiter=';',
                     index_col=0)
    df.index = pd.to_datetime(df.index)

    start_value = get_closest_value(df, start_date)
    end_value = get_closest_value(df, end_date)

    return end_value / start_value


def get_closest_value(df, date):
    import datetime
    delta = datetime.timedelta(days=1)

    while True:
        try:
            return df.at[date, 'Zamkniecie']
        except KeyError:
            date -= delta
            continue
