from app.genetic.agent import Agent
from app.genetic.mutation_operators.gene_creation import GeneCreation


def test_mutate_validAgent_returnsAgentWithDifferentGene(config, gene_factory):
    one_gene = gene_factory.create_random_gene()
    agent = Agent(1, [one_gene], config)

    old_gene_str = one_gene.to_string()
    operator = GeneCreation(1.0, gene_factory)

    new_agent = operator.mutate([agent])[0]
    new_gene_str = new_agent.genome[0].to_string()
    assert old_gene_str != new_gene_str


def test_mutate_one_gene_validGene_returnsNewGene(config, gene_factory):
    gene = gene_factory.create_random_gene()
    gene_str = gene.to_string()
    operator = GeneCreation(1.0, gene_factory)

    new_gene_str = operator.mutate_one_gene(gene).to_string()

    assert gene_str != new_gene_str
