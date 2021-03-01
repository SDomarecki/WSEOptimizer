import datetime
import statistics

from app.config import Config
from app.economics.fee_counter.normal_counter import NormalCounter
from app.economics.stock_order import StockOrder
from app.genetic.get_closest_value import get_closest_value


class Wallet:
    def __init__(self, config: Config):
        self.config = config
        self.cash: float = config.start_cash
        self.stocksHold: {StockOrder} = {}
        self.ordersLog: [StockOrder] = []
        self.valueHistory: [float] = []
        self.valueTimestamps: [datetime] = []
        self.fee_counter = NormalCounter(
            config.fee_min, config.fee_rate, config.fee_added, config.fee_max
        )

    def get_fee_from_charge(self, charge: float) -> float:
        return self.fee_counter.count(charge)

    def get_total_value(self, database, date) -> float:
        total = self.cash + sum(
            [
                get_closest_value(database[stock.ticker].technicals, date, "Close")
                * stock.amount
                for stock in self.stocksHold.values()
            ]
        )
        return round(total, 2)

    def get_end_total_value(self, database) -> float:
        return self.get_total_value(database, self.config.end_date)

    def get_current_sharpe(self, database, date) -> float:
        risk_free = self.config.start_cash * (self.config.risk_free_return + 1)
        current_return = self.get_total_value(database, date)
        stdev = statistics.stdev(self.valueHistory)
        if stdev == 0:
            return 0
        return (current_return - risk_free) / stdev

    def get_end_sharpe(self, database) -> float:
        return self.get_current_sharpe(database, self.config.end_date)

    def has_stock(self, stock):
        return self.stocksHold.get(stock.ticker) is not None
