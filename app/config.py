from datetime import datetime, date


class Config:
    def __init__(self):
        self.fetch_mode = ""
        self.min_circulation = 0
        self.max_circulation = 0
        self.sectors = []
        self.companies = []
        self.chunks = 1
        self.timedelta = 1
        self.iterations = 1
        self.initial_population = 1
        self.start_date = None
        self.end_date = None
        self.validations = []
        self.selection_method = ""
        self.agents_to_save = 0.0
        self.constant_length = False
        self.initial_length = 0
        self.max_genes = 0
        self.mutation_method = ""
        self.mutation_rate = 0.0
        self.start_cash = 0
        self.return_method = ""
        self.benchmark = ""
        self.risk_free_return = 0.0
        self.fee_min = 0.0
        self.fee_rate = 0.0
        self.fee_added = 0.0
        self.fee_max = 0.0
        self.stocks_to_buy = 0
        self.stocks_to_hold = 0
        self.fin_statement_lag = 0
        self.logic_to_all = 0.0
        self.fundamental_to_all = 0.0

    def fetch_from_dict(self, dict_config: {}):
        self._fetch_database_config(dict_config.get("database", {}))
        self._fetch_simulation_config(dict_config.get("simulation", {}))
        self._fetch_selection_config(dict_config.get("selection", {}))
        self._fetch_crossover_config(dict_config.get("crossover", {}))
        self._fetch_mutation_config(dict_config.get("mutation", {}))
        self._fetch_wallet_config(dict_config.get("wallet", {}))
        self._fetch_genes_config(dict_config.get("genes", {}))

    def _fetch_database_config(self, db_config: {}):
        self.fetch_mode = db_config.get("fetch_mode", "auto")
        self.min_circulation = int(db_config.get("min_circulation", 0))
        self.max_circulation = int(db_config.get("max_circulation", 0))
        self.sectors = db_config.get("sectors", [])
        self.companies = db_config.get("companies", [])
        self.chunks = db_config.get("chunks", 0)

    def _fetch_simulation_config(self, sim_config: {}):
        default_date = date(2000, 1, 1)
        self.timedelta = int(sim_config.get("timedelta", 0))
        self.iterations = int(sim_config.get("iterations", 0))
        self.initial_population = int(sim_config.get("initial_population", 0))
        if "learning" not in sim_config:
            self.start_date = default_date
            self.end_date = default_date
        else:
            self.start_date = datetime.strptime(
                sim_config.get("learning").get("start_date", default_date), "%Y-%m-%d"
            ).date()
            self.end_date = datetime.strptime(
                sim_config.get("learning").get("end_date", default_date), "%Y-%m-%d"
            ).date()

        self.validations = []
        if "testing" not in sim_config:
            return
        for test in sim_config["testing"]:
            start_date = datetime.strptime(
                test.get("start_date", default_date), "%Y-%m-%d"
            ).date()
            end_date = datetime.strptime(
                test.get("end_date", default_date), "%Y-%m-%d"
            ).date()
            self.validations.append((start_date, end_date))

    def _fetch_selection_config(self, sel_config: {}):
        self.selection_method = sel_config.get("method", "roulette")
        self.agents_to_save = sel_config.get("agents_to_save", 0.0)

    def _fetch_crossover_config(self, cross_config: {}):
        self.constant_length = cross_config.get("constant_length", True)
        self.initial_length = cross_config.get("initial_genes", 0)
        self.max_genes = cross_config.get("max_genes", 0)

    def _fetch_mutation_config(self, mutation_config: {}):
        self.mutation_method = mutation_config.get("method", "normalization")
        self.mutation_rate = mutation_config.get("rate", 0.0)

    def _fetch_wallet_config(self, wallet_config: {}):
        self.start_cash = wallet_config.get("start_cash", 0)
        self.return_method = wallet_config.get("return_method", "total_value")
        self.benchmark = wallet_config.get("benchmark", "")
        self.risk_free_return = wallet_config.get("risk_free_return", 0.0)
        self.fee_min = wallet_config.get("fees", {}).get("min", 0.0)
        self.fee_rate = wallet_config.get("fees", {}).get("rate", 0.0)
        self.fee_added = wallet_config.get("fees", {}).get("added", 0.0)
        self.fee_max = wallet_config.get("fees", {}).get("max", 0.0)
        self.stocks_to_buy = wallet_config.get("stocks_to_buy", 0)
        self.stocks_to_hold = wallet_config.get("stocks_to_hold", 0)

    def _fetch_genes_config(self, genes_config: {}):
        self.fin_statement_lag = genes_config.get("fin_statement_lag", 135)
        self.logic_to_all = genes_config.get("logic_to_all", 0.0)
        self.fundamental_to_all = genes_config.get("fundamental_to_all", 0.0)
