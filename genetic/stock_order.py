class StockOrder:
    def __init__(self, date, direction: str,
                 ticker: str, amount: int, price: float,
                 fee: float, cash_remaining: float):
        self.date = date
        self.direction = direction
        self.ticker = ticker
        self.amount = amount
        self.price = price
        self.fee = fee
        self.cash_remaining = cash_remaining

    def to_string(self) -> str:
        return f'{self.date.strftime("%Y-%m-%d")} {self.direction} ' \
               f'{self.ticker} {self.amount} x {self.price} [Fee: {self.fee}] [Remains: {self.cash_remaining}]'
