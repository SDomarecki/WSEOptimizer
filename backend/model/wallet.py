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
from backend.model.stockOrder import StockOrder
from shared.model.company import Company
from shared.model.config import Config


class Wallet:
    def __init__(self):
        self.cash = Config.start_cash
        self.stocksHold = {} # {ticker:StockOrder}
        self.ordersLog = [] # [StockOrder]

    def trade(self, stock_strengths, day, current_total):
        # 1. realizuj sprzedaż
        for i in range(len(stock_strengths)-1, 10, -1):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is not None:
                self.sell(stock_strengths[i], day)

        # 2. realizuj kupno
        for i in range(0, 4):
            loc = self.stocksHold.get(stock_strengths[i].ticker)
            if loc is None:
                self.buy(stock_strengths[i], day, current_total)

    def sell(self, stock, day):
        direction = 'SELL'
        ticker = stock.ticker
        amount = self.stocksHold[stock.ticker].amount
        try:
            price = stock.technicals.at[day, 'Close']
        except KeyError:
            return

        del self.stocksHold[ticker]
        # TODO jeszcze dowalic opłaty maklera
        self.cash += amount*price
        self.ordersLog.append(StockOrder(day, direction, ticker, amount, price))

    def buy(self, stock: Company, day, total_value: float):
        import math

        order_value = min(self.cash, total_value/5)
        direction = 'BUY'
        ticker = stock.ticker
        try:
            price = stock.technicals.at[day, 'Close']
        except KeyError:
            return

        amount = int(math.floor(order_value/price))
        if amount < 1:
            return
        order_value = price * amount
        # TODO jeszcze dowalic opłaty maklera
        stock_order = StockOrder(day, direction, ticker, amount, price)
        self.ordersLog.append(stock_order)
        self.stocksHold[ticker] = stock_order
        self.cash -= order_value

    def get_total_value(self, database, end_date):
        sum = self.cash
        for stock in self.stocksHold.values():
            company = database[stock.ticker]
            today_price = self.get_closest_day_price(company.technicals, end_date)
            sum += today_price * stock.amount
        return sum

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
