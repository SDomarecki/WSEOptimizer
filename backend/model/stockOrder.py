class StockOrder:
    def __init__(self, date, direction, ticker, amount, price):
        self.date = date
        self.direction = direction
        self.ticker = ticker
        self.amount = amount
        self.price = price

    def to_string(self):
        return self.date.strftime('%Y-%m-%d') + " " \
               + self.direction + " " \
               + self.ticker + " " \
               + str(self.amount) + " x " \
               + str(self.price)

