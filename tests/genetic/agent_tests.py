from datetime import date

import pytest

from app.config import Config
from app.economics.company import Company
from app.genetic.agent import Agent
from tests.genetic.fake_trader import FakeTrader
from tests.genetic.genes.fake_true_gene import FakeTrueGene


@pytest.fixture
def config() -> Config:
    config = Config()
    config.timedelta = 1
    config.start_date = date(2001, 1, 1)
    config.end_date = date(2001, 1, 30)
    config.validations = [(date(2000, 1, 1), date(2001, 1, 1))]
    return config


def test_calculate_learning_fitness_validDatabase_returnsFitness(config):
    genome = [FakeTrueGene]
    agent = Agent(1, genome, config)
    agent.trader = FakeTrader(config)

    database = []

    agent.calculate_learning_fitness(database, 1)

    assert agent.learning_fitness == 20


def test_calculate_testing_fitness_validDatabase_returnsFitness(config):
    genome = [FakeTrueGene]
    agent = Agent(1, genome, config)
    agent.trader = FakeTrader(config)

    database = []

    agent.calculate_testing_fitness(database, 0)

    assert agent.testing_fitnesses[0] == 260


def test_learning_simulate_validDatabase_returnsFitness(config):
    genome = [FakeTrueGene]
    agent = Agent(1, genome, config)
    agent.trader = FakeTrader(config)

    database = []

    fitness = agent.learning_simulate(database, 1)

    # Iterations (trade days) between date(2000,1,1) and date(2000,1,30)
    assert fitness == 20


def test_testing_simulate_validDatabase_returnsFitness(config):
    genome = [FakeTrueGene]
    agent = Agent(1, genome, config)
    agent.trader = FakeTrader(config)

    database = []

    fitness = agent.testing_simulate(database, 0)

    # Iterations (trade days) between date(2000,1,1) and date(2001,1,1)
    assert fitness == 260


def test_calculateStrength_validStock_returnsStockStrength(config):
    stock = Company("test", "TEST", "/test", "sector:test")
    day = date(2000, 1, 1)
    genome = [FakeTrueGene(), FakeTrueGene()]
    agent = Agent(1, genome, config)

    strength = agent.calculate_strength(stock, day)

    assert strength == 2


def test_to_json_ready_validAgent_returnsValidDict(config):
    genome = [FakeTrueGene()]
    agent = Agent(1, genome, config)

    agent_dict = agent.to_json_ready()

    assert agent_dict == {
        "id": 1,
        "strategy": ["1.00 x If(Fake) then 1 else -1"],
        "fitness": "0.00",
        "validations": ["0.00"],
    }


@pytest.mark.parametrize(
    "day",
    [
        date(2010, 7, 12),
        date(2010, 7, 13),
        date(2010, 7, 14),
        date(2010, 7, 15),
        date(2010, 7, 16),
    ],
)
def test_next_business_day_weekday_returnsSameDay(config, day):
    agent = Agent(1, [], config)

    same_day = agent.shift_to_weekday(day)

    assert same_day == day


@pytest.mark.parametrize("day", [date(2010, 1, 2), date(2010, 1, 3)])
def test_next_business_day_weekend_returnsNextMonday(config, day):
    agent = Agent(1, [], config)

    next_monday_from_weekend = agent.shift_to_weekday(day)

    assert next_monday_from_weekend.weekday() == 0
