import math

from app.config import Config
from app.economics.company import Company
from app.economics.stock_order import StockOrder
from app.economics.wallet import Wallet
from genetic.get_closest_value import convert_date_to_datetime


class Trader:
    def __init__(self, config: Config):
        self.config = config

        self.training_wallets = [Wallet(config)] * (config.chunks + 1)
        self.testing_wallets = [Wallet(config)] * len(config.validations)

    def trade_on_training(self, stock_strengths, day, database, chunk):
        self.trade(stock_strengths, day, database, self.training_wallets[chunk])

    def trade_on_testing(self, stock_strengths, day, database, test_number):
        self.trade(stock_strengths, day, database, self.testing_wallets[test_number])

    def trade(self, stock_strengths, day, database, wallet):
        current_total = wallet.get_total_value(database, date=day)
        wallet.valueHistory.append(current_total)
        wallet.valueTimestamps.append(day)

        buy_recommendations = stock_strengths[: self.config.stocks_to_buy]
        sell_recommendations = stock_strengths[self.config.stocks_to_hold :]
        self.sell_some(sell_recommendations, day, wallet)
        self.buy_some(buy_recommendations, day, current_total, wallet)

    def sell_some(self, recommendations, day, wallet):
        for recommendation in recommendations:
            if wallet.has_stock(recommendation):
                self.sell_one(recommendation, day, wallet)

    def sell_one(self, stock: Company, day, wallet):
        price = self.today_price(stock, day)
        if price is None:
            return

        direction = "SELL"
        ticker = stock.ticker
        amount = wallet.stocksHold[stock.ticker].amount
        order_value = price * amount
        fee = wallet.get_fee_from_charge(order_value)

        wallet.cash += order_value
        wallet.cash -= fee
        wallet.cash = round(wallet.cash, 2)
        stock_order = StockOrder(
            day, direction, ticker, amount, price, fee, wallet.cash
        )
        del wallet.stocksHold[ticker]
        wallet.ordersLog.append(stock_order)

    def buy_some(self, recommendations, day, current_total, wallet):
        if len(wallet.stocksHold) >= self.config.stocks_to_buy:
            return
        for recommendation in recommendations:
            if not wallet.has_stock(recommendation):
                self.buy_one(recommendation, day, current_total, wallet)

    def buy_one(self, stock: Company, day, total_value: float, wallet):
        price = self.today_price(stock, day)
        if price is None:
            return

        direction = "BUY"
        ticker = stock.ticker
        order_value = min(wallet.cash, total_value / self.config.stocks_to_buy)
        amount = int(math.floor(order_value / price))
        if amount < 1:  # can't trade fractional stocks
            return
        order_value = price * amount
        fee = wallet.get_fee_from_charge(order_value)

        wallet.cash -= order_value
        wallet.cash -= fee
        wallet.cash = round(wallet.cash, 2)
        stock_order = StockOrder(
            day, direction, ticker, amount, price, fee, wallet.cash
        )
        wallet.stocksHold[ticker] = stock_order
        wallet.ordersLog.append(stock_order)

    def get_final_training_fitness(self, database, chunk) -> float:
        if self.config.return_method == "total_value":
            return self.training_wallets[chunk].get_end_total_value(database)
        return self.training_wallets[chunk].get_end_sharpe(database)

    def get_final_testing_fitness(self, database, case) -> float:
        if self.config.return_method == "total_value":
            return self.testing_wallets[case].get_end_total_value(database)
        return self.testing_wallets[case].get_end_sharpe(database)

    def today_price(self, stock, day):
        lookup = convert_date_to_datetime(day)
        try:
            return stock.technicals.at[lookup, "Close"]
        except KeyError:
            return None
