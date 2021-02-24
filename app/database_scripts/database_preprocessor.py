import io
import json
import os
import shutil

from config import Config
from database_scripts.basic_info.br_basic_info_scraper import BRBasicInfoScraper
from database_scripts.company_details import CompanyDetails
from database_scripts.fundamentals.biznes_radar.br_scraper import BRScraper
from database_scripts.technicals.stooq.stooq_preprocessor import StooqPreprocessor


class DatabasePreprocessor:
    def __init__(self, config: Config):
        self.config = config
        self.fetched = 0
        self.to_fetch = 0
        self.basic_info_fetcher = BRBasicInfoScraper()
        self.technicals_fetcher = StooqPreprocessor()
        self.fundamentals_fetcher = BRScraper()

    def create_database(self):
        self.init_directory_tree()
        self.preprocess_companies(self.config.companies)
        self.preprocess_benchmark(self.config.benchmark)

    def init_directory_tree(self):
        os.makedirs('database/preprocessed', exist_ok=True)
        os.makedirs('database/preprocessed/benchmarks', exist_ok=True)

    def preprocess_companies(self, tickers: [str]):
        companies = self.basic_info_fetcher.get_companies()
        if tickers:
            companies = self.limit_companies_to_fetch(companies, tickers)
        self.to_fetch = len(companies)
        print(f'To fetch: {str(self.to_fetch)} companies')

        for company in companies.values():
            self.collect_company_info(company)

    def limit_companies_to_fetch(self, companies: dict, tickers_to_stay: [str]) -> dict:
        companies_copy = dict(companies)
        for ticker in companies.keys():
            if ticker not in tickers_to_stay:
                del companies_copy[ticker]
        return companies_copy

    def collect_company_info(self, company: CompanyDetails):
        try:
            os.makedirs(f'database/preprocessed/{company.ticker}')
            self.fetch_and_save_company_details(company)
            print('>Basic info fetched.')
            self.fetch_and_save_company_technicals(company)
            print('>Technicals fetched.')
            self.fetch_and_save_company_fundamentals(company)
            print('>Fundamentals fetched.')
        except FileExistsError:
            print(f'{company.ticker} already exists. Skipping.')
        except (FileNotFoundError, AttributeError) as error:
            print(error)
            print(f'Fetching failed for {company.ticker}. Rolling back changes.')
            shutil.rmtree(f'database/preprocessed/{company.ticker}', ignore_errors=True)
        else:
            self.fetched += 1
            print(f'Fetched already {str(self.fetched)}/{str(self.to_fetch)} companies.')

    def fetch_and_save_company_details(self, company: CompanyDetails):
        company.sector = self.basic_info_fetcher.get_sector(company.link)
        with io.open(f'database/preprocessed/{company.ticker}/basic_info.json', 'w') as f:
            f.write(json.dumps(company.__dict__))

    def fetch_and_save_company_technicals(self, company: CompanyDetails):
        technicals = self.technicals_fetcher.fetch_technicals(company)
        technicals.to_csv(f'database/preprocessed/{company.ticker}/technical.csv')

    def fetch_and_save_company_fundamentals(self, company: CompanyDetails):
        fundamentals = self.fundamentals_fetcher.get_fundamentals(company)
        fundamentals.to_csv(f'database/preprocessed/{company.ticker}/fundamental.csv')

    def preprocess_benchmark(self, ticker: str):
        df = self.technicals_fetcher.fetch_raw_history(ticker)
        df = self.technicals_fetcher.change_column_names_from_polish_to_english(df)
        df.to_csv(f'database/preprocessed/benchmarks/{ticker}')
