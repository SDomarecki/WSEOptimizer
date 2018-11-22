class StockOrder:
    def __init__(self, date, direction, ticker, amount, price, fee, cash_remaining):
        self.date = date
        self.direction = direction
        self.ticker = ticker
        self.amount = amount
        self.price = price
        self.fee = fee
        self.cash_remaining = cash_remaining

    def to_string(self):
        return self.date.strftime('%Y-%m-%d') + " " \
               + self.direction + " " \
               + self.ticker + " " \
               + str(self.amount) + " x " \
               + str(self.price) \
               + "[Fee: " + str(self.fee) \
               + "] [Remains: " + str(self.cash_remaining) + "]"

