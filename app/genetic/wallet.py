import datetime
import math
import statistics

from app.genetic.config import Config
from app.genetic.stock_order import StockOrder
from app.shared.company import Company


class Wallet:
    def __init__(self):
        self.cash: float = Config.start_cash
        self.stocksHold: {StockOrder} = {}
        self.ordersLog: [StockOrder] = []
        self.valueHistory: [float] = []
        self.valueTimestamps: [datetime] = []

    def trade(self, stock_strengths, day, database):
        current_total = self.get_total_value(database, date=day)
        self.valueHistory.append(current_total)
        self.valueTimestamps.append(day)

        # 1. realizuj sprzedaż
        for i in range(len(stock_strengths) - 1, Config.stocks_to_hold, -1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is not None:
                self.sell_one(stock_strengths[i], day)

        if len(self.stocksHold) < Config.stocks_to_buy:
            # 2. realizuj kupno
            for i in range(0, Config.stocks_to_buy - 1):
                loc = self.stocksHold.get(stock_strengths[i].ticker)
                if loc is None:
                    self.buy_one(stock_strengths[i], day, current_total)

    def sell_one(self, stock: Company, day):
        direction = 'SELL'
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, 'Close']
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

    def buy_one(self, stock: Company, day, total_value: float):
        direction = 'BUY'
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, 'Close']
        except KeyError:
            return

        order_value = min(self.cash, total_value / Config.stocks_to_buy)
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
        return round(
            statistics.median(
                [Config.fee_min, round(charge * Config.fee_rate / 100 + Config.fee_added, 2), Config.fee_max]), 2)

    def get_total_value(self, database, date) -> float:
        total = self.cash + \
                sum([self.get_closest_day_price(database[stock.ticker].technicals, date) * stock.amount
                     for stock
                     in self.stocksHold.values()])
        return round(total, 2)

    def get_closest_day_price(self, technicals, day) -> float:
        delta = datetime.timedelta(days=1)
        while True:
            try:
                return technicals.at[day, 'Close']
            except KeyError:
                day -= delta
                continue

    def get_current_sharpe(self, database, date) -> float:
        risk_free = Config.start_cash * (Config.risk_free_return + 1)
        current_return = self.get_total_value(database, date)
        stdev = statistics.stdev(self.valueHistory)
        if stdev == 0:
            return 0
        return (current_return - risk_free) / stdev

    def print_order_log(self):
        for order in self.stocksHold.values():
            print(order.to_string())
