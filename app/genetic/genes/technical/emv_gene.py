import random

from ..gene import Gene


class EMVGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.close_value = random.uniform(-1, 1)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, "emv"]

        if self.comparator == ">":
            return indicator_value > self.close_value
        return indicator_value < self.close_value

    def condition_to_string(self) -> str:
        return f"EMV {self.comparator} Close"
