import pytest

from app.config import Config
from app.genetic.genes import GeneFactory


@pytest.fixture(scope="package")
def config() -> Config:
    agents_to_save_rate = 0.5
    config = Config()
    config.logic_to_all = 0.0
    config.fundamental_to_all = 0.0
    config.agents_to_save = agents_to_save_rate
    config.validations = []
    return config


@pytest.fixture(scope="package")
def gene_factory(config) -> GeneFactory:
    return GeneFactory(config)
