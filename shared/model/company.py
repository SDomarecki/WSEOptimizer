from database.indicators import *


class Company:
    def __init__(self, name, ticker, link):
        self.name = name
        self.ticker = ticker
        self.link = link
        self.fundamentals = None  # Pandas DataFrame object!
        self.technicals = None  # Pandas DataFrame object!

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, skipkeys=True, ensure_ascii=False).encode(
            'utf8').decode("utf-8")

    def convert_columns(self):
        self.technicals.rename(columns={'Data': 'Date',
                                        'Otwarcie': 'Open',
                                        'Najwyzszy': 'High',
                                        'Najnizszy': 'Low',
                                        'Zamkniecie': 'Close',
                                        'Wolumen': 'Volume'},
                               inplace=True)

    def convert_date_as_index(self):
        self.technicals.set_index('Date', inplace=True)

    def calculate_all_technicals(self):
        self.calculate_circulation()
        self.calculate_sma15()
        self.calculate_sma40()

        self.technicals = ema(self.technicals, period=200, close_col='Close')
        self.technicals = rsi(self.technicals, periods=14, close_col='Close')
        self.technicals = macd(self.technicals, period_long=26, period_short=12, period_signal=9, close_col='Close')
        self.technicals = trix(self.technicals, periods=14, signal_periods=9, close_col='Close')
        self.technicals = williams_r(self.technicals, periods=10, high_col='High', low_col='Low', close_col='Close')
        self.technicals = money_flow_index(self.technicals,
                                           periods=14,
                                           high_col='High',
                                           low_col='Low',
                                           close_col='Close',
                                           vol_col='Volume')
        self.technicals = momentum(self.technicals, periods=14, close_col='Close')
        self.technicals = ease_of_movement(self.technicals, period=14, high_col='High', low_col='Low', vol_col='Volume')

    def calculate_circulation(self):
        self.technicals['Circulation'] = self.technicals['Close'] * self.technicals['Volume']

    def calculate_sma15(self):
        self.technicals['sma15'] = self.technicals['Close'].rolling(window=15).mean()

    def calculate_sma40(self):
        self.technicals['sma40'] = self.technicals['Close'].rolling(window=40).mean()

    # P/E = current_price * stocks_amount / last_statements_earnings*4
    def get_price_to_earnings(self, date) -> float:
        price = self.technicals[date].close
        current_statement = self.fundamentals[date_to_quarter(date)]
        stocks_amount = current_statement.stocks_amount
        market_capitalization = price * stocks_amount
        pe_ratio = market_capitalization / (current_statement.earnings * 4)
        return pe_ratio

    # P/BV = current_price * stocks_amount / last_statements_book_value*4
    def get_price_to_book_value(self, date) -> float:
        price = self.technicals[date].close
        current_statement = self.fundamentals[date_to_quarter(date)]
        stocks_amount = current_statement.stocks_amount
        market_capitalization = price * stocks_amount
        pbv_ratio = market_capitalization / (current_statement.book_value * 4)
        return pbv_ratio

    # TODO
    def calculate_all_fundamentals(self):
        pass


def date_to_quarter(date):
    return str(date.year) + "/Q" + str(pd.Timestamp(date).quarter)
