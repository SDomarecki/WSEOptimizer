import random

from genetic.gene import create_random_gene
from genetic.wallet import Wallet


class Agent:

    def __init__(self, length):
        self.genes = [create_random_gene() for _ in range(length)]
        self.weights = [random.uniform(0.0,  1.0) for _ in range(length)]
        self.fitness = None
        self.wallet = Wallet()

    def calculate_strength(self, stock, day) -> float:
        strength = 0
        for i in range(len(self.genes)):
            try:
                strength += self.genes[i].get_substrength(stock, day) * self.weights[i]
            except KeyError:
                continue
        return strength

    def reset(self):
        self.fitness = None
        self.wallet = Wallet()

    def to_string(self) -> str:
        genotype = ""
        for gene in self.genes:
            genotype += gene.__class__.__name__ + " "
        return genotype


