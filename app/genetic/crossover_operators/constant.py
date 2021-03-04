import random

from app.genetic.agent import Agent
from app.config import Config
from app.genetic.crossover_operators.operator import Operator


class Constant(Operator):
    def __init__(
        self,
        agent_len: int,
        to_create: int,
        config: Config,
    ):
        super().__init__()
        self.agent_len = agent_len
        self.to_create = to_create
        self.config = config

    def crossover(self, agents: [Agent], last_agent_id: int) -> [Agent]:
        agent_id = last_agent_id
        offspring = []
        for _ in range(self.to_create):
            [parent1, parent2] = random.sample(agents, 2)

            split = random.randint(0, self.agent_len)
            child1_genome = parent1.genome[:split] + parent2.genome[split:]
            child2_genome = parent2.genome[:split] + parent1.genome[split:]

            child1 = Agent(agent_id, child1_genome, self.config)
            child2 = Agent(agent_id + 1, child2_genome, self.config)

            offspring.append(child1)
            offspring.append(child2)

            agent_id += 2
        return offspring
