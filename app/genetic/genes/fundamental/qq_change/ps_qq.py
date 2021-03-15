import random

from app.genetic.genes.fundamental.qq_change.gene_qq_change import GeneQQChange
from app.genetic.genes.gene import Gene


class PSqq(GeneQQChange):
    def __init__(self):
        super().__init__()
        self.indicator = "P/S"
        self.compared_value = random.uniform(0.5, 1.5)
