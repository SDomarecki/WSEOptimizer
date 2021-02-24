from app.economics.fee_counter.normal_counter import NormalCounter


def test_count_chargeLessThanMinFee_returnsMinFee():
    fee_min = 5.0
    fee_rate = 1.0
    fee_added = 0.0
    fee_max = 10.0
    charge = 1.0
    counter = NormalCounter(fee_min, fee_rate, fee_added, fee_max)

    fee = counter.count(charge)

    assert fee == fee_min


def test_count_chargeBetweenMinAndMaxFee_returnsMinFee():
    fee_min = 5.0
    fee_rate = 1.0
    fee_added = 0.0
    fee_max = 10.0
    charge = 6.0
    counter = NormalCounter(fee_min, fee_rate, fee_added, fee_max)

    fee = counter.count(charge)

    assert fee == charge * fee_rate + fee_added


def test_count_chargeMoreThanMaxFee_returnsMinFee():
    fee_min = 5.0
    fee_rate = 1.0
    fee_added = 0.0
    fee_max = 10.0
    charge = 20.0
    counter = NormalCounter(fee_min, fee_rate, fee_added, fee_max)

    fee = counter.count(charge)

    assert fee == fee_max
