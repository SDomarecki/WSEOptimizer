from app.genetic.mutation_operators.normalization import Normalization
from app.genetic.agent import Agent


def test_mutate_validAgent_returnsAgentWithChangedWeights(config, gene_factory):
    one_gene = gene_factory.create_random_gene()
    agent = Agent(1, [one_gene], config)

    old_weght = one_gene.weight
    operator = Normalization(1.0)

    new_agent = operator.mutate([agent])[0]
    new_weight = new_agent.genome[0].weight
    assert new_weight != old_weght


def test_mutate_one_gene_validGene_returnsChangedGene(config, gene_factory):
    gene = gene_factory.create_random_gene()
    old_weght = gene.weight
    operator = Normalization(1.0)

    new_gene = operator.mutate_one_gene(gene)

    new_weight = new_gene.weight
    assert new_weight != old_weght
