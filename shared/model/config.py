import configparser
import datetime
import json


class Config:

    appName = ""
    version = ""
    geometry = ""

    last_used_ticker = ""

    timedelta = 0
    initial_population = 0
    initial_length = 0
    agents_to_drop = 0
    max_genes = 0
    iterations = 0

    start_cash = 0
    start_date = None
    end_date = None
    validation_start_date = None
    validation_end_date = None
    return_method = ""
    benchmark = ""
    risk_free_return = 0.0
    fee_min = 0
    fee_rate = 0
    fee_added = 0
    fee_max = 0

    stocks_to_buy = 0
    stocks_to_hold = 0

    min_circulation = 0
    max_circulation = 0
    sectors = []
    companies = []

def read_config():
    config = configparser.ConfigParser()
    config.read('../../config.ini')

    Config.appName = config['ROOT']['APP_NAME']
    Config.version = config['ROOT']['VERSION']
    Config.geometry = config['ROOT']['GEOMETRY']

    Config.last_used_ticker = config['LAST_USED']['TICKER']

    Config.timedelta = int(config['GA']['TIMEDELTA'])
    Config.initial_population = int(config['GA']['INITIAL_POPULATION'])
    Config.initial_length = int(config['GA']['INITIAL_LENGTH'])
    Config.agents_to_drop = float(config['GA']['AGENTS_TO_DROP'])
    Config.max_genes = int(config['GA']['MAX_GENES'])
    Config.iterations = int(config['GA']['ITERATIONS'])

    Config.start_cash = float(config['WALLET']['START_CASH'])
    Config.start_date = datetime.datetime.strptime(config['WALLET']['START_DATE'], '%Y-%m-%d')
    Config.end_date = datetime.datetime.strptime(config['WALLET']['END_DATE'], '%Y-%m-%d')
    Config.validation_start_date = datetime.datetime.strptime(config['WALLET']['VALID_START_DATE'], '%Y-%m-%d')
    Config.validation_end_date = datetime.datetime.strptime(config['WALLET']['VALID_END_DATE'], '%Y-%m-%d')
    Config.return_method = config['WALLET']['RETURN_METHOD']
    Config.benchmark = config['WALLET']['BENCHMARK']
    Config.risk_free_return = float(config['WALLET']['RISK_FREE_RETURN'])
    Config.fee_min = float(config['WALLET']['FEE_MIN'])
    Config.fee_rate = float(config['WALLET']['FEE_RATE'])
    Config.fee_added = float(config['WALLET']['FEE_ADDED'])
    Config.fee_max = float(config['WALLET']['FEE_MAX'])

    Config.stocks_to_buy = int(config['WALLET']['STOCKS_TO_BUY'])
    Config.stocks_to_hold = int(config['WALLET']['STOCKS_TO_HOLD'])

    Config.min_circulation = int(config['FILTER']['MIN_CIRCULATION'])
    Config.max_circulation = int(config['FILTER']['MAX_CIRCULATION'])

    Config.sectors = config['FILTER']['SECTORS'].split(', ')
    Config.companies = config['FILTER']['COMPANIES'].split(', ')

# TODO update 2018-10-24
def reset():
    last_used = 'CDR'
    return_method = 'TotalCash'
    benchmark = 'WIG'
    risk_free_return = 0.025


# TODO save_config
