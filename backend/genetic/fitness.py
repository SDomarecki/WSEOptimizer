# Do fitness bierze wszelkie ograniczenia, sprawdzany genom oraz database
# Ograniczenia zawierają w sobie informacje o
# - Czasie trwania symulacji
# - Rodzaju funkcji celu
# - i innych (powinno być przefiltrowane PRZED rozpoczęciem symulacji
import datetime
import collections

from backend.model.wallet import Wallet
from shared.model.config import Config


def fitness(tested_agent, database):
    wallet = Wallet()

    start_date = Config.start_date
    end_date = Config.end_date

    day = start_date
    delta = datetime.timedelta(days=1)
    while day < end_date:
        stock_strengths = {}
        for stock in database:
            stock_strengths[tested_agent.calculateStrength(stock, day)].append(stock)
        ordered_stock_strengths = collections.OrderedDict(sorted(stock_strengths.items()))
        wallet.trade(ordered_stock_strengths)
        day += delta

    if constraints["target"] == "cash":
        return wallet.getCurrentValue(database, end_date)
    elif constraints["target"] == "sharpe":
        return wallet.getCurrentSharpe(database)
    else:
        return wallet.getCurrentInformationRatio()
