import random

from ..gene import Gene


class MACDGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, "MACD_12_26_9"]
        signal_value = company.technicals.at[day, "MACDs_12_26_9"]

        if self.comparator == ">":
            return indicator_value > signal_value
        return indicator_value < signal_value

    def condition_to_string(self) -> str:
        return f"MACD {self.comparator} MACD Signal"
