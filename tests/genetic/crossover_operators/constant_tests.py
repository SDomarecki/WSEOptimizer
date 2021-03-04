from app.config import Config
from app.genetic.agent import Agent
from app.genetic.crossover_operators.constant import Constant
from tests.genetic.genes.fake_false_gene import FakeFalseGene
from tests.genetic.genes.fake_true_gene import FakeTrueGene


def test_crossover_validAgents_createsNewMixedGenomeAgents():
    config = Config()
    genome1 = [FakeTrueGene(), FakeTrueGene()]
    agent1 = Agent(1, genome1, config)

    genome2 = [FakeFalseGene(), FakeFalseGene()]
    agent2 = Agent(2, genome2, config)

    crossover_op = Constant(2, 2, config)
    new_agents = crossover_op.crossover([agent1, agent2], 3)

    assert (
        new_agents[0].agent_id == 3
        and new_agents[1].agent_id == 4
        and len(new_agents[0].genome) == 2
        and len(new_agents[1].genome) == 2
    )
