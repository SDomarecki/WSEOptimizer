from datetime import date

from genetic.config import Config


def test_init_validData_createsValidConfig():
    test__fetch_database_config_validData_fetchesValidVariables()
    test__fetch_simulation_config_validData_fetchesValidVariables()
    test__fetch_selection_config_validData_fetchesValidVariables()
    test__fetch_crossover_config_validData_fetchesValidVariables()
    test__fetch_wallet_config_validData_fetchesValidVariables()
    test__fetch_genes_config_validData_fetchesValidVariables()


def test_init_emptyData_createsDefaultConfig():
    test__fetch_database_config_emptyDict_returnsDefaultSettings()
    test__fetch_simulation_config_emptyDict_returnsDefaultSettings()
    test__fetch_selection_config_emptyDict_returnsDefaultSettings()
    test__fetch_crossover_config_emptyDict_returnsDefaultSettings()
    test__fetch_wallet_config_emptyDict_returnsDefaultSettings()
    test__fetch_genes_config_emptyDict_returnsDefaultSettings()


def test__fetch_database_config_validData_fetchesValidVariables():
    db_config = {
        "min_circulation": 1,
        "max_circulation": 1,
        "sectors": ['sector'],
        "companies": ['company'],
        "chunks": 1
    }
    config = Config()

    config._fetch_database_config(db_config)

    assert config.min_circulation == 1 \
           and config.max_circulation == 1 \
           and config.sectors == ['sector'] \
           and config.companies == ['company'] \
           and config.chunks == 1


def test__fetch_database_config_emptyDict_returnsDefaultSettings():
    db_config = {}
    config = Config()

    config._fetch_database_config(db_config)

    assert config.min_circulation == 0 \
           and config.max_circulation == 0 \
           and config.sectors == [] \
           and config.companies == [] \
           and config.chunks == 0


def test__fetch_simulation_config_validData_fetchesValidVariables():
    sim_config = {
        "timedelta": 1,
        "iterations": 1,
        "initial_population": 1,
        "learning": {
            "start_date": "2010-01-01",
            "end_date": "2020-01-01"
        },
        "testing": [
            {
                "start_date": "2010-01-01",
                "end_date": "2020-01-01"
            }
        ]
    }
    config = Config()

    config._fetch_simulation_config(sim_config)

    assert config.timedelta == 1 \
           and config.iterations == 1 \
           and config.initial_population == 1 \
           and config.start_date == date(2010, 1, 1) \
           and config.end_date == date(2020, 1, 1) \
           and config.validations[0][0] == date(2010, 1, 1) \
           and config.validations[0][1] == date(2020, 1, 1)


def test__fetch_simulation_config_emptyDict_returnsDefaultSettings():
    sim_config = {}
    config = Config()

    config._fetch_simulation_config(sim_config)

    assert config.timedelta == 0 \
           and config.iterations == 0 \
           and config.initial_population == 0 \
           and config.start_date == date(2000, 1, 1) \
           and config.end_date == date(2000, 1, 1) \
           and config.validations == []


def test__fetch_selection_config_validData_fetchesValidVariables():
    sel_config = {
        "method": "roulette",
        "agents_to_save": 1.0
    }
    config = Config()

    config._fetch_selection_config(sel_config)

    assert config.selection_method == 'roulette' \
           and config.agents_to_save == 1.0


def test__fetch_selection_config_emptyDict_returnsDefaultSettings():
    sel_config = {}
    config = Config()

    config._fetch_selection_config(sel_config)

    assert config.selection_method == 'roulette' \
           and config.agents_to_save == 0.0


def test__fetch_crossover_config_validData_fetchesValidVariables():
    cross_config = {
        "constant_length": False,
        "initial_genes": 1,
        "max_genes": 1,
        "mutation_rate": 1.0
    }
    config = Config()

    config._fetch_crossover_config(cross_config)

    assert config.constant_length is False \
           and config.initial_length == 1 \
           and config.max_genes == 1 \
           and config.mutation_rate == 1.0


def test__fetch_crossover_config_emptyDict_returnsDefaultSettings():
    cross_config = {}
    config = Config()

    config._fetch_crossover_config(cross_config)

    assert config.constant_length is True \
           and config.initial_length == 0 \
           and config.max_genes == 0 \
           and config.mutation_rate == 0.0


def test__fetch_wallet_config_validData_fetchesValidVariables():
    wallet_config = {
        "start_cash": 1,
        "return_method": "sharpe",
        "benchmark": "wig",
        "risk_free_return": 1.0,
        "fees": {
            "min": 1.0,
            "rate": 1.0,
            "added": 1.0,
            "max": 1.0
        }
    }
    config = Config()

    config._fetch_wallet_config(wallet_config)

    assert config.start_cash == 1 \
           and config.return_method == 'sharpe' \
           and config.benchmark == 'wig' \
           and config.risk_free_return == 1.0 \
           and config.fee_min == 1.0 \
           and config.fee_rate == 1.0 \
           and config.fee_added == 1.0 \
           and config.fee_max == 1.0


def test__fetch_wallet_config_emptyDict_returnsDefaultSettings():
    wallet_config = {}
    config = Config()

    config._fetch_wallet_config(wallet_config)

    assert config.start_cash == 0 \
           and config.return_method == 'total_value' \
           and config.benchmark == '' \
           and config.risk_free_return == 0.0 \
           and config.fee_min == 0.0 \
           and config.fee_rate == 0.0 \
           and config.fee_added == 0.0 \
           and config.fee_max == 0.0


def test__fetch_genes_config_validData_fetchesValidVariables():
    genes_config = {
        'fin_statement_lag': 123,
        'logic_to_all': 1.0,
        'fundamental_to_all': 1.0
    }
    config = Config()

    config._fetch_genes_config(genes_config)

    assert config.fin_statement_lag == 123 \
           and config.logic_to_all == 1.0 \
           and config.fundamental_to_all == 1.0


def test__fetch_genes_config_emptyDict_returnsDefaultSettings():
    genes_config = {}
    config = Config()

    config._fetch_genes_config(genes_config)

    assert config.fin_statement_lag == 135 \
           and config.logic_to_all == 0.0 \
           and config.fundamental_to_all == 0.0
