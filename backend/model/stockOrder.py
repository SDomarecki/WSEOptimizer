class StockOrder:
    def __init__(self, date, direction, ticker, amount, price):
        self.date = date
        self.direction = direction
        self.ticker = ticker
        self.amount = amount
        self.price = price

    def print(self):
        print(self.date + " " + self.direction + " " + self.ticker + " " + self.amount + " x " + self.price)

