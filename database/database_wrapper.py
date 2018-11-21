from database.company_utilities import boost_company_info
from shared.company import Company
from database.br_scraper import BRscraper
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


def collect_company_info(company) -> Company:
    global fetched

    try:
        company.sector = BRscraper.get_sector(company.link)
    except AttributeError:
        return

    company.fundamentals = BRscraper.get_fundamentals(company.link)
    company.technicals = get_raw_technicals(company.ticker)
    company = boost_company_info(company)

    company.fundamentals.to_csv('../res/fundamental/' + company.ticker + '.csv')
    company.technicals.to_csv('../res/technical/' + company.ticker + '.csv')
    with io.open('../res/basic_info/' + company.ticker + '.json', 'w') as f:
        f.write(company.toJSON())
    fetched += 1
    print('Fetched already ' + str(fetched) + '/' + str(toFetch) + ' companies')
    return company


def get_raw_technicals(ticker: str):
    ticker = ticker.lower()
    df = pd.read_csv('../res/stooq_source/' + ticker + '.csv', delimiter=';')
    return df


if __name__ == "__main__":
    create_database()
