import datetime
import json


class Config:

    # database
    min_circulation = 0
    max_circulation = 0
    sectors = []
    companies = []
    chunks = 0

    # simulation
    timedelta = 0
    iterations = 0
    initial_population = 0
    start_date = None
    end_date = None
    validations = []

    # selection
    selection_method = ""
    agents_to_save = 0

    # crossover
    constant_length = True
    initial_length = 0
    max_genes = 0
    mutation_rate = 0.0

    # wallet
    start_cash = 0
    return_method = ""
    benchmark = ""
    risk_free_return = 0.0
    fee_min = 0.0
    fee_rate = 0.0
    fee_added = 0.0
    fee_max = 0.0
    stocks_to_buy = 0
    stocks_to_hold = 0

    # genes
    fin_statement_lag = 135
    fundamental_to_all = 0.0

    def __init__(self):
        with open('../config_ga.json') as f:
            dict_config = json.load(f)

        database = dict_config['database']
        Config.min_circulation = int(database['min_circulation'])
        Config.max_circulation = int(database['max_circulation'])
        Config.sectors = database['sectors']
        Config.companies = database['companies']
        Config.chunks = database['chunks']

        simulation = dict_config['simulation']
        Config.timedelta = int(simulation['timedelta'])
        Config.iterations = int(simulation['iterations'])
        Config.initial_population = int(simulation['initial_population'])
        Config.start_date = datetime.datetime.strptime(simulation['learning']['start_date'], '%Y-%m-%d')
        Config.end_date = datetime.datetime.strptime(simulation['learning']['end_date'], '%Y-%m-%d')

        for test in simulation['testing']:
            start_date = datetime.datetime.strptime(test['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(test['end_date'], '%Y-%m-%d')
            Config.validations.append( (start_date, end_date) )

        selection = dict_config['selection']
        Config.selection_method = selection['method']
        Config.agents_to_save = selection['agents_to_save']

        crossover = dict_config['crossover']
        Config.constant_length = crossover['constant_length']
        Config.initial_length = crossover['initial_genes']
        Config.max_genes = crossover['max_genes']
        Config.mutation_rate = crossover['mutation_rate']

        wallet = dict_config['wallet']
        Config.start_cash = wallet['start_cash']
        Config.return_method = wallet['return_method']
        Config.benchmark = wallet['benchmark']
        Config.risk_free_return = wallet['risk_free_return']
        Config.fee_min = wallet['fees']['min']
        Config.fee_rate = wallet['fees']['rate']
        Config.fee_added = wallet['fees']['added']
        Config.fee_max = wallet['fees']['max']
        Config.stocks_to_buy = wallet['stocks_to_buy']
        Config.stocks_to_hold = wallet['stocks_to_hold']

        genes = dict_config['genes']
        Config.fin_statement_lag = genes['fin_statement_lag']
        Config.fundamental_to_all = genes['fundamental_to_all']
