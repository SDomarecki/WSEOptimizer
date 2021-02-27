import datetime
import math
import statistics

from app.config import Config
from app.economics.company import Company
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

    def trade(self, stock_strengths, day, database):
        current_total = self.get_total_value(database, date=day)
        self.valueHistory.append(current_total)
        self.valueTimestamps.append(day)

        self.sell_some(stock_strengths, day)
        self.buy_some(stock_strengths, day, current_total)

    def sell_some(self, stock_strengths, day):
        for i in range(len(stock_strengths) - 1, self.config.stocks_to_hold, -1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is not None:
                self.sell_one(stock_strengths[i], day)

    def sell_one(self, stock: Company, day):
        direction = "SELL"
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, "Close"]
        except KeyError:
            return
        amount = self.stocksHold[stock.ticker].amount

        order_value = price * amount
        fee = self.get_fee_from_charge(order_value)
        self.cash += order_value
        self.cash -= fee
        self.cash = round(self.cash, 2)
        stock_order = StockOrder(day, direction, ticker, amount, price, fee, self.cash)
        del self.stocksHold[ticker]
        self.ordersLog.append(stock_order)

    def buy_some(self, stock_strengths, day, current_total):
        if len(self.stocksHold) >= self.config.stocks_to_buy:
            return
        for i in range(0, self.config.stocks_to_buy - 1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is None:
                self.buy_one(stock_strengths[i], day, current_total)

    def buy_one(self, stock: Company, day, total_value: float):
        direction = "BUY"
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, "Close"]
        except KeyError:
            return

        order_value = min(self.cash, total_value / self.config.stocks_to_buy)
        amount = int(math.floor(order_value / price))
        if amount < 1:
            return

        order_value = price * amount
        fee = self.get_fee_from_charge(order_value)
        self.cash -= order_value
        self.cash -= fee
        self.cash = round(self.cash, 2)
        stock_order = StockOrder(day, direction, ticker, amount, price, fee, self.cash)
        self.stocksHold[ticker] = stock_order
        self.ordersLog.append(stock_order)

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
