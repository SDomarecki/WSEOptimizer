import io
import os
from multiprocessing import Pool as ThreadPool

import pandas as pd

from app.database_scripts.br_scraper import BRscraper
from app.database_scripts.company_utilities import boost_company_info
from app.shared.company import Company


class DatabaseOperator:
    def __init__(self):
        self.fetched = 0
        self.to_fetch = 0

    def create_database(self):
        companies = BRscraper.get_companies()
        self.to_fetch = len(companies)
        print(f'To fetch: {str(self.to_fetch)} companies')
        self.init_directory_tree()

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
        print(f'Fetched already {str(self.fetched)}/{str(self.to_fetch)} companies')
        return company

    def get_raw_technicals(self, ticker: str):
        ticker = ticker.lower()
        df = pd.read_csv(f'database/stooq/{ticker}_d.csv', delimiter=',')
        return df

    def init_directory_tree(self):
        os.makedirs('database/preprocessed/fundamental', exist_ok=True)
        os.makedirs('database/preprocessed/technical', exist_ok=True)
        os.makedirs('database/preprocessed/basic_info', exist_ok=True)


if __name__ == "__main__":
    dbo = DatabaseOperator()
    dbo.create_database()
