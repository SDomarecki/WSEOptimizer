from app.genetic.genes.logical.or_gene import OrGene
from tests.genetic.genes.fake_false_gene import FakeFalseGene
from tests.genetic.genes.fake_true_gene import FakeTrueGene


def test_condition_bothTrue_returnTrue():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    or_gene = OrGene(true_gene_1, true_gene_2)

    condition = or_gene.condition(None, None)

    assert condition


def test_condition_oneTrue_returnTrue():
    true_gene = FakeTrueGene()
    false_gene = FakeFalseGene()
    or_gene = OrGene(true_gene, false_gene)

    condition = or_gene.condition(None, None)

    assert condition


def test_condition_bothFalse_returnFalse():
    false_gene_1 = FakeFalseGene()
    false_gene_2 = FakeFalseGene()
    or_gene = OrGene(false_gene_1, false_gene_2)

    condition = or_gene.condition(None, None)

    assert not condition


def test_condition_to_string_fakeGenes_returnsValidString():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    or_gene = OrGene(true_gene_1, true_gene_2)
    or_gene.weight = 2.0
    or_gene.result_true = 1
    or_gene.result_false = -1

    condition_str = or_gene.to_string()

    assert condition_str == "2.00 x If(Fake OR Fake) then 1 else -1"
