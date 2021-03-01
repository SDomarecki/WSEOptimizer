import pytest

from app.config import Config
from app.genetic.genes.gene_factory import GeneFactory


@pytest.fixture(scope="package")
def config():
    config = Config()
    config.logic_to_all = 0.0
    config.fundamental_to_all = 0.0
    config.validations = []
    return config


@pytest.fixture(scope="package")
def gene_factory(config):
    return GeneFactory(config)
