from app.genetic.agent import Agent
from app.genetic.selection_operators.rating import Rating


def test_select_validAgents_returnsSelectedAmount(config, gene_factory):
    agents_to_create = 4
    agents_to_save_rate = 0.5
    rating = Rating(agents_to_save_rate)

    agents = [Agent(i, 0, gene_factory, config) for i in range(agents_to_create)]
    agents[0].learning_fitness = 10.0
    agents[1].learning_fitness = 7.0
    agents[2].learning_fitness = 5.0
    agents[3].learning_fitness = 3.0
    new_agents = rating.select(agents)

    assert (
        new_agents[0].learning_fitness == 10.0
        and new_agents[1].learning_fitness == 7.0
        and len(new_agents) == 2
    )
