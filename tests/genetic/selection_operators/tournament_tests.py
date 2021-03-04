from app.genetic.agent import Agent
from app.genetic.selection_operators.tournament import Tournament


def test_select_validAgents_returnsSelectedAmount(config):
    agents_to_create = 4
    agents_to_save_rate = 0.5
    rating = Tournament(agents_to_save_rate)

    agents = [Agent(i, [], config) for i in range(agents_to_create)]
    agents[0].learning_fitness = 10.0
    agents[1].learning_fitness = 7.0
    agents[2].learning_fitness = 5.0
    agents[3].learning_fitness = 3.0
    new_agents = rating.select(agents)

    assert len(new_agents) == 2


def test_select_one_aspirant_validAgents_returnsAgentWithGreaterFitness(config):
    agents_to_create = 2
    agents_to_save_rate = 0.0
    rating = Tournament(agents_to_save_rate)

    agents = [Agent(i, [], config) for i in range(agents_to_create)]
    agents[0].learning_fitness = 10.0
    agents[1].learning_fitness = 17.0

    selected_agent = rating.select_one_aspirant(agents, 2)
    assert selected_agent.agent_id == agents[1].agent_id
