from shared.scraper.br_scraper import BRscraper
import pandas as pd


def create_database():
    companies = BRscraper.get_companies()

    for company in companies.values():
        companies[company.ticker].fundamentals = BRscraper.get_fundamentals(company.link)
        companies[company.ticker].technicals = get_technicals(company.ticker)


def get_technicals(ticker):
    df = pd.read_csv('../../database/technical/' + ticker + '.csv', delimiter=';')
    # print(df)
    df['Data'] = pd.to_datetime(df['Data'])
    #TODO countTechnicals
    return df
