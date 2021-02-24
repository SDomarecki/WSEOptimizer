from statistics import median


class NormalCounter:
    def __init__(self, fee_min: float, fee_rate: float, fee_added: float, fee_max: float):
        self.fee_min = fee_min
        self.fee_rate = fee_rate
        self.fee_added = fee_added
        self.fee_max = fee_max

    def count(self, charge: float):
        normal_fee = round(charge * self.fee_rate + self.fee_added, 2)
        return round(median([self.fee_min, normal_fee, self.fee_max]), 2)
