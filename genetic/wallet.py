# Klasa do obsługi wirtualnego portfela
# Powinna posiadać w sobie pole na:
#  - gotówkę,
#  - posiadane akcje (co, ile, za ile kupione)
#  - ograniczenia takie jak prowizja, procent portfela na 1 walor (albo ilość spółek?)
#  - oraz log aktywności (01.01.2018 BUY CDR 100 105.0zł aka data, kierunek, ticker, ilość, cena poj.)
# Z interfejsu udostępnia (chyba!)
#  - metody kupna (zbiera każdy sygnał kupna z fitnessu)
#  - metody sprzedaży (zbiera każdy sygnał sprzedażowy z fitnessu)
#  - metody getowe - łączna wartość portfela, Sharpe, IR i takie tam
from genetic.stockOrder import StockOrder
from shared.company import Company
from shared.config import Config


class Wallet:
    def __init__(self):
        self.cash = Config.start_cash
        self.stocksHold = {} # {ticker:StockOrder}
        self.ordersLog = [] # [StockOrder]

    def trade(self, stock_strengths, day, database):
        current_total = self.get_total_value(database, end_date=day)

        # 1. realizuj sprzedaż
        for i in range(len(stock_strengths)-1, Config.stocks_to_hold, -1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is not None:
                self.sell(stock_strengths[i], day)

        # 2. realizuj kupno
        for i in range(0, Config.stocks_to_buy-1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is None:
                self.buy(stock_strengths[i], day, current_total)

    def sell(self, stock, day):
        direction = 'SELL'
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, 'Close']
        except KeyError:
            return
        amount = self.stocksHold[stock.ticker].amount

        order_value = price * amount
        fee = self.get_fee_from_charge(order_value)
        stock_order = StockOrder(day, direction, ticker, amount, price)
        del self.stocksHold[ticker]
        self.ordersLog.append(stock_order)
        self.cash += order_value
        self.cash -= fee

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
        stock_order = StockOrder(day, direction, ticker, amount, price)
        self.stocksHold[ticker] = stock_order
        self.ordersLog.append(stock_order)
        self.cash -= order_value
        self.cash -= fee

    def get_fee_from_charge(self, charge):
        import statistics as s
        return s.median([Config.fee_min, charge * Config.fee_rate/100 + Config.fee_added, Config.fee_max])

    def get_total_value(self, database, end_date):
        total = self.cash
        for stock in self.stocksHold.values():
            company = database[stock.ticker]
            today_price = self.get_closest_day_price(company.technicals, end_date)
            total += today_price * stock.amount
        return total

    def get_closest_day_price(self, technicals, day):
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

    # TODO
    def get_current_sharpe(self, database):
        pass

    # TODO
    def get_current_information_ratio(self):
        pass
