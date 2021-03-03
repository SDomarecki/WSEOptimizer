import random

from ..gene import Gene


class EOMGene(Gene):
    def __init__(self):
        super().__init__()
        self.comparator = random.choice([">", "<"])
        self.compared_value = random.uniform(-1, 1)

    def condition(self, company, day):
        indicator_value = company.technicals.at[day, "EOM_14_100000000"]

        if self.comparator == ">":
            return indicator_value > self.compared_value
        return indicator_value < self.compared_value

    def condition_to_string(self) -> str:
        return f"EOM {self.comparator} {self.compared_value}"
