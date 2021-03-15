import random

from app.genetic.genes.fundamental.yy_change.gene_yy_change import GeneYYChange
from app.genetic.genes.gene import Gene


class ROEyy(GeneYYChange):
    def __init__(self):
        super().__init__()
        self.indicator = "ROE"
        self.compared_value = random.uniform(0.8, 4.0)
