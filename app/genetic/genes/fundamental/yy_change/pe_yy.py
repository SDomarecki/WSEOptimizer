import random

from app.genetic.genes.fundamental.yy_change.gene_yy_change import GeneYYChange


class PEyy(GeneYYChange):
    def __init__(self):
        super().__init__()
        self.indicator = "P/E"
        self.compared_value = random.uniform(0.8, 1.8)
