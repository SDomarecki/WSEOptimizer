import random

from app.genetic.genes.fundamental.qq_change.gene_qq_change import GeneQQChange


class ROEqq(GeneQQChange):
    def __init__(self):
        super().__init__()
        self.indicator = "ROE"
        self.compared_value = random.uniform(0.8, 4.0)
