from app.genetic.agent import Agent
from app.genetic.selection_operators import Roulette


def test_select_validAgents_returnsSelectedAmount(config, gene_factory):
    agents_to_create = 4
    agents_to_save_rate = 0.5
    rating = Roulette(agents_to_save_rate)

    agents = [Agent(i, 0, gene_factory, config) for i in range(agents_to_create)]
    agents[0].fitness = 10.0
    agents[1].fitness = 7.0
    agents[2].fitness = 5.0
    agents[3].fitness = 3.0
    new_agents = rating.select(agents)

    assert len(new_agents) == 2 and rating.fitness_sum == 25.0