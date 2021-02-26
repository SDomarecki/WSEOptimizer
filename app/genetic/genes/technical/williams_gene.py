import random

from ..gene import Gene


class WilliamsGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.compared_value = random.uniform(-80, -20)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, "williams_r"]

        if self.comparator == ">":
            return indicator_value > self.compared_value
        return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"Williams %R {self.comparator} {self.compared_value:.2f}"
