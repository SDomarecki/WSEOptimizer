from app.economics.wallet import Wallet


class FakeTrader:
    def __init__(self, config):
        self.config = config

        self.training_wallets = [Wallet(config)] * (config.chunks + 1)
        self.testing_wallets = [Wallet(config)] * len(config.validations)

        self.trade_hits = 0

    def trade_on_training(self, ordered_stocks, day, database, chunk):
        self.trade_hits += 1

    def get_final_training_fitness(self, database, chunk):
        return self.trade_hits

    def trade_on_testing(self, ordered_stocks, day, database, chunk):
        self.trade_hits += 1

    def get_final_testing_fitness(self, database, chunk):
        return self.trade_hits
