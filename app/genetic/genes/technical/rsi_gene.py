import random

from ..gene import Gene


class RSIGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.compared_value = random.uniform(20, 80)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, "RSI_14"]

        if self.comparator == ">":
            return indicator_value > self.compared_value
        return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"RSI {self.comparator} {self.compared_value:.2f}"
