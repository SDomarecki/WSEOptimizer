from app.genetic.genes.logical.and_gene import AndGene
from tests.genetic.genes.logic.fake_false_gene import FakeFalseGene
from tests.genetic.genes.logic.fake_true_gene import FakeTrueGene


def test_condition_bothTrue_returnTrue():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    and_gene = AndGene(true_gene_1, true_gene_2)

    condition = and_gene.condition(None, None)

    assert condition


def test_condition_oneFalse_returnFalse():
    true_gene = FakeTrueGene()
    false_gene = FakeFalseGene()
    and_gene = AndGene(true_gene, false_gene)

    condition = and_gene.condition(None, None)

    assert not condition


def test_condition_bothFalse_returnFalse():
    false_gene_1 = FakeFalseGene()
    false_gene_2 = FakeFalseGene()
    and_gene = AndGene(false_gene_1, false_gene_2)

    condition = and_gene.condition(None, None)

    assert not condition


def test_condition_to_string_fakeGenes_returnsValidString():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    and_gene = AndGene(true_gene_1, true_gene_2)
    and_gene.weight = 2.0
    and_gene.result_true = 1
    and_gene.result_false = -1

    condition_str = and_gene.to_string()

    assert condition_str == "2.00 x If(Fake AND Fake) then 1 else -1"
