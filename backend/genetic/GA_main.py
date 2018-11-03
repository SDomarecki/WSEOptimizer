import collections
import datetime

from backend.genetic.agent import Agent
from backend.model.wallet import Wallet
from database.databaseWrapper import read_database
from shared.model.config import Config
from shared.model.config import read_config


def ga():
    database = read_database()

    agents = init_agents(Config.initial_population, 10)
    generations = Config.iterations
    # TODO filtrowanie bazy danych - np przez minimalny wolumen
    for generation in range(generations):

        print('Generation: ' + str(generation))

        for agent in agents:
            agent.fitness = fitness(agent, database)

        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)

    result_string = ''
    for counter, value in enumerate(agents):
        validated_result = fitness(value, database, validation=True)
        result_string += str(counter) + ") [" + str(validated_result) + "] " + value.__str__()
    save_to_file(result_string)


def init_agents(population, length):
    return [Agent(length) for _ in range(population)]


# funkcja do obliczenia sprawności agenta
def fitness(tested_agent: Agent, database, validation=False) -> float:
    wallet = Wallet()

    if not validation:
        start_date = Config.start_date
        end_date = Config.end_date
    else:
        start_date = Config.validation_start_date
        end_date = Config.validation_end_date

    day = start_date
    delta = datetime.timedelta(days=1)
    while day < end_date:
        stock_strengths = {}
        for stock in database:
            stock_strengths[tested_agent.calculate_strength(stock, day)].append(stock)
        ordered_stock_strengths = collections.OrderedDict(sorted(stock_strengths.items()))
        current_total = wallet.get_total_value(database, day)
        wallet.trade(ordered_stock_strengths, current_total)
        day += delta

    if Config.return_method == "cash":
        return wallet.get_total_value(database, end_date)
    elif Config.return_method == "sharpe":
        return wallet.get_current_sharpe(database)
    else:
        return wallet.get_current_information_ratio()


# fukcja sortująca i niszcząca słabe osobniki
def selection(agents: []):
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    print('\n'.join(map(str, agents)))
    agents = agents[:int(0.2 * len(agents))]

    return agents


# fukcja tworząca nowe osobniki
def crossover(agents: []):
    import random

    offspring = []

    for _ in range((Config.initial_population - len(agents)) / 2):
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        child1 = Agent(1)
        child2 = Agent(1)
        split = random.randint(0, 10)
        child1.genes = parent1.genes[0:split] + parent2.genes[split:10]
        child2.genes = parent2.genes[0:split] + parent1.genes[split:10]

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)

    return agents


# funkcja podmieniająca geny w nowych osobnikach
def mutation(agents: []):
    import random
    for agent in agents:
        for idx, param in enumerate(agent.genes):
            if random.uniform(0.0, 1.0) <= 0.1:
                from backend.genetic.gene import create_random_gene
                agent.genes = agent.genes[0:idx] + create_random_gene() + agent.genes[idx+1:10]
    return agents


def save_to_file(result: str):
    file = open('result.txt', 'w')
    file.write(result)
    file.close()


if __name__ == "__main__":
    read_config()
    ga()
