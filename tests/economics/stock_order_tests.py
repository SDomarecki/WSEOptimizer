from datetime import date

from app.economics.stock_order import StockOrder


def test_to_string_validData_returnsFormattedString():
    day = date(2000, 1, 1)
    direction = "DIR"
    ticker = "TCK"
    amount = 1.0
    price = 1.0
    fee = 1.0
    cash_remaining = 1.0
    order = StockOrder(day, direction, ticker, amount, price, fee, cash_remaining)

    order_string = order.to_string()

    assert order_string == "2000-01-01 DIR TCK 1.0 x 1.0 [Fee: 1.0] [Remains: 1.0]"
