from database_scripts.company_utilities import boost_company_info
from shared.company import Company
from database_scripts.br_scraper import BRscraper
import pandas as pd
import io
import os

class DatabaseOperator:

    def __init__(self):
        self.fetched = 0
        self.toFetch = 0

    def create_database(self):
        from multiprocessing.dummy import Pool as ThreadPool

        companies = BRscraper.get_companies()
        self.toFetch = len(companies)
        print(f'To fetch: {str(self.toFetch)} companies')

        if not os.path.exists('database'):
            os.mkdir('database')

        if not os.path.exists('database/preprocessed'):
            os.mkdir('database/preprocessed')

        if not os.path.exists('database/preprocessed/fundamental'):
            os.mkdir('database/preprocessed/fundamental')

        if not os.path.exists('database/preprocessed/technical'):
            os.mkdir('database/preprocessed/technical')

        if not os.path.exists('database/preprocessed/basic_info'):
            os.mkdir('database/preprocessed/basic_info')

        pool = ThreadPool(4)

        pool.map(self.collect_company_info, companies.values())

    def collect_company_info(self, company: Company):
        try:
            company.sector = BRscraper.get_sector(company.link)
        except AttributeError:
            return

        company.fundamentals = BRscraper.get_fundamentals(company.link)
        company.technicals = self.get_raw_technicals(company.ticker)
        company = boost_company_info(company)

        self.save_company(company)

    def save_company(self, company: Company):
        company.fundamentals.to_csv(f'database/preprocessed/fundamental/{company.ticker}.csv')
        company.technicals.to_csv(f'database/preprocessed/technical/{company.ticker}.csv')
        with io.open(f'database/preprocessed/basic_info/{company.ticker}.json', 'w') as f:
            f.write(company.toJSON())
        self.fetched += 1
        print(f'Fetched already {str(self.fetched)}/{str(self.toFetch)} companies')
        return company

    def get_raw_technicals(self, ticker: str):
        ticker = ticker.lower()
        df = pd.read_csv(f'database/stooq/{ticker}_d.csv', delimiter=',')
        return df


if __name__ == "__main__":
    dbo = DatabaseOperator()
    dbo.create_database()
