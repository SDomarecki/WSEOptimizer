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

    databases = filter_database(companies)

    return databases


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


def filter_database(database) -> []:
    database = filter_by_company_name(database)
    database = filter_by_sector(database)

    databases = []
    databases.append(filter_database_with_dates(database, Config.start_date, Config.end_date))
    for validation in Config.validations:
        databases.append(filter_database_with_dates(database, validation[0], validation[1]))
    return databases


def filter_database_with_dates(database, start_date, end_date):
    from copy import deepcopy

    to_delete = []
    new_database = deepcopy(database)
    for company in new_database.values():
        company.technicals = company.technicals.loc[start_date:end_date]

        circulation_mean = float(company.technicals['Circulation'].mean())
        if Config.min_circulation != -1 and circulation_mean < Config.min_circulation:
            to_delete.append(company.ticker)
        if Config.max_circulation != -1 and circulation_mean > Config.max_circulation:
            to_delete.append(company.ticker)

    for ticker in to_delete:
        del new_database[ticker]

    return new_database


def filter_by_company_name(database):
    return database


def filter_by_sector(database):
    sectors = Config.sectors
    to_delete = []

    if not sectors or sectors[0] == 'All':
        return database

    for company in database.values():
        if company.sector not in sectors:
            to_delete.append(company.ticker)

    for ticker in to_delete:
        del database[ticker]
    return database


def get_benchmark(ticker: str, path_to_database):
    ticker = ticker.lower()
    df = pd.read_csv(path_to_database + '/benchmarks/' + ticker + '.csv',
                     delimiter=';',
                     index_col=0)
    df.index = pd.to_datetime(df.index)
    return df


def get_target_ratio(benchmark, start_date, end_date) -> float:
    start_value = get_closest_value(benchmark, start_date)
    end_value = get_closest_value(benchmark, end_date)

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
