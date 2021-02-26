import random

from ..gene import Gene


class SMA15NormalizedGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.compared_value = random.uniform(0.5, 2)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, "sma15"]
        close_value = company.technicals.at[day, "Close"]
        normalized_value = indicator_value / close_value

        if self.comparator == ">":
            return normalized_value > self.compared_value
        return normalized_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"SMA15Norm {self.comparator} {self.compared_value:.2f}"
