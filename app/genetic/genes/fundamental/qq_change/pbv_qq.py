import random

from app.genetic.genes.fundamental.qq_change.gene_qq_change import GeneQQChange


class PBVqq(GeneQQChange):
    def __init__(self):
        super().__init__()
        self.indicator = "P/BV"
        self.compared_value = random.uniform(0.5, 1.5)
