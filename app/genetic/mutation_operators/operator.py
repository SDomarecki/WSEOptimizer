import random

from abc import ABC, abstractmethod

from app.genetic.agent import Agent
from app.genetic.genes.gene import Gene


class Operator(ABC):
    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def get_mutation_flag(self) -> bool:
        return random.uniform(0.0, 1.0) <= self.mutation_rate

    def mutate(self, agents: [Agent]) -> [Agent]:
        for agent in agents:
            agent.genes = [
                self.mutate_one_gene(gene) if self.get_mutation_flag() else gene
                for gene in agent.genes
            ]
        return agents

    @abstractmethod
    def mutate_one_gene(self, gene: Gene) -> Gene:
        pass
