import random

from app.genetic.agent import Agent
from app.config import Config
from app.genetic.crossover_operators.operator import Operator


class Constant(Operator):
    def __init__(
        self,
        agent_len: int,
        to_create: int,
        validations: [],
        config: Config,
    ):
        super().__init__()
        self.agent_len = agent_len
        self.to_create = to_create
        self.validations = len(validations)
        self.config = config

    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        agent_id = last_agent_id
        offspring = []
        for _ in range(self.to_create):
            parent1 = random.choice(agents)
            parent2 = random.choice(agents)

            split = random.randint(0, self.agent_len)
            child1_genes = parent1.genes[:split] + parent2.genes[split:]
            child2_genes = parent2.genes[:split] + parent1.genes[split:]

            child1 = Agent(agent_id, child1_genes, self.config)
            child2 = Agent(agent_id + 1, child2_genes, self.config)

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
