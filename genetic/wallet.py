from genetic.stock_order import StockOrder
from shared.company import Company
from shared.config import Config


class Wallet:
    def __init__(self):
        self.cash = Config.start_cash # float
        self.stocksHold = {} # {ticker:StockOrder}
        self.ordersLog = [] # [StockOrder]
        self.valueHistory = [] # [float]
        self.valueTimestamps = [] # [Datetime]

    def trade(self, stock_strengths, day, database):
        current_total = self.get_total_value(database, date=day)
        self.valueHistory.append(current_total)
        self.valueTimestamps.append(day)

        # 1. realizuj sprzedaż
        for i in range(len(stock_strengths)-1, Config.stocks_to_hold, -1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is not None:
                self.sell(stock_strengths[i], day)

        if len(self.stocksHold) < Config.stocks_to_buy:
            # 2. realizuj kupno
            for i in range(0, Config.stocks_to_buy-1):
                loc = self.stocksHold.get(stock_strengths[i].ticker)
                if loc is None:
                    self.buy(stock_strengths[i], day, current_total)

    def sell(self, stock: Company, day):
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

    def buy(self, stock: Company, day, total_value: float):
        import math

        direction = 'BUY'
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, 'Close']
        except KeyError:
            return

        order_value = min(self.cash, total_value / Config.stocks_to_buy)
        amount = int(math.floor(order_value/price))
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
        import statistics as s
        return round(s.median([Config.fee_min, round(charge * Config.fee_rate/100 + Config.fee_added, 2), Config.fee_max]), 2)

    def get_total_value(self, database, date) -> float:
        total = self.cash
        for stock in self.stocksHold.values():
            company = database[stock.ticker]
            today_price = self.get_closest_day_price(company.technicals, date)
            total += today_price * stock.amount
        return round(total, 2)

    def get_closest_day_price(self, technicals, day) -> float:
        import datetime

        price = -1
        delta = datetime.timedelta(days=1)
        while price == -1:
            try:
                price = technicals.at[day, 'Close']
            except KeyError:
                day -= delta
                continue

        return price

    def get_current_sharpe(self, database, date) -> float:
        import statistics

        risk_free = Config.start_cash * (Config.risk_free_return + 1)
        current_return = self.get_total_value(database, date)
        stdev = statistics.stdev(self.valueHistory)
        if stdev == 0:
            return 0
        return (current_return - risk_free) / stdev

    # TODO
    def get_current_information_ratio(self):
        pass

    def print_order_log(self):
        for order in self.stocksHold.values():
            print(order.to_string())
