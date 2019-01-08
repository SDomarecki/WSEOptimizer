from database.company_utilities import boost_company_info
from shared.company import Company
from database.br_scraper import BRscraper
import pandas as pd
import io

class DatabaseOperator:

    def __init__(self):
        self.fetched = 0
        self.toFetch = 0

    def create_database(self):
        from multiprocessing.dummy import Pool as ThreadPool

        companies = BRscraper.get_companies()
        self.toFetch = len(companies)
        print('To fetch: ' + str(self.toFetch) + ' companies')
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
        company.fundamentals.to_csv('../res/fundamental/' + company.ticker + '.csv')
        company.technicals.to_csv('../res/technical/' + company.ticker + '.csv')
        with io.open('../res/basic_info/' + company.ticker + '.json', 'w') as f:
            f.write(company.toJSON())
        self.fetched += 1
        print('Fetched already ' + str(self.fetched) + '/' + str(self.toFetch) + ' companies')
        return company

    def get_raw_technicals(self, ticker: str):
        ticker = ticker.lower()
        df = pd.read_csv('../res/stooq_source/' + ticker + '.csv', delimiter=';')
        return df


if __name__ == "__main__":
    dbo = DatabaseOperator()
    dbo.create_database()
