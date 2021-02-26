import random

import app.genetic.crossover_operators as op
from app.genetic.agent import Agent
from app.config import Config
from app.genetic.genes import GeneFactory


class Constant(op.Operator):
    def __init__(
        self,
        agent_len: int,
        to_create: int,
        validations: [],
        gene_factory: GeneFactory,
        config: Config,
    ):
        super().__init__()
        self.agent_len = agent_len
        self.to_create = to_create
        self.validations = len(validations)
        self.gene_factory = gene_factory
        self.config = config

    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        agent_id = last_agent_id
        offspring = []
        for _ in range(self.to_create):
            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            child1 = Agent(agent_id, 0, self.gene_factory, self.config)
            child2 = Agent(agent_id + 1, 0, self.gene_factory, self.config)

            split = random.randint(0, self.agent_len)
            child1.genes = parent1.genes[:split] + parent2.genes[split:]
            child2.genes = parent2.genes[:split] + parent1.genes[split:]

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
