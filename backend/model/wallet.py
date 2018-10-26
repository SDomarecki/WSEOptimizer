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
from shared.model.config import Config


class Wallet:
    # cash = 0.0
    # stocksHold = []
    # ordersLog = None
    def __init__(self):
        self.cash = Config.start_cash
        self.stocksHold = []
        self.ordersLog = []

    def trade(self, stock_strengths, day):
        #1. realizuj sprzedaż
        for i in range(stock_strengths.length()-1, 10, -1):
            loc = self.stocksHold.index(stock_strengths[i].name)
            if loc != ValueError:
                self.sell(loc, day)

        # 2. realizuj kupno
        for i in range(0,4):
            loc = self.stocksHold.index(stock_strengths[i].name)
            if loc == ValueError:
                self.buy(stock_strengths[i])


    # TODO
    def sell(self,location):
        pass

    # TODO
    def buy(self, stock):
        pass
