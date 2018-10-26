from backend.genetic.agent import Agent
from backend.genetic.fitness import fitness
from database.databaseWrapper import create_database
from shared.model.config import read_config, Config


def ga():
    read_config()

    agents = init_agents(Config.initial_population, 10)
    generations = Config.iterations

    for generation in range(generations):

        print('Generation: ' + str(generation))

        results = {}
        for agent in agents:
            results[fitness(agent, database)] = agent

        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)


def init_agents(population, length):

    return [Agent(length) for _ in range(population)]


if __name__ == "__main__":
    # ga()
    create_database()