from app.genetic.genes.logical.eq_gene import EqGene
from tests.genetic.genes.logic.fake_false_gene import FakeFalseGene
from tests.genetic.genes.logic.fake_true_gene import FakeTrueGene


def test_condition_bothTrue_returnTrue():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    eq_gene = EqGene(true_gene_1, true_gene_2)

    condition = eq_gene.condition(None, None)

    assert condition


def test_condition_oneFalse_returnFalse():
    true_gene = FakeTrueGene()
    false_gene = FakeFalseGene()
    eq_gene = EqGene(true_gene, false_gene)

    condition = eq_gene.condition(None, None)

    assert not condition


def test_condition_bothFalse_returnTrue():
    false_gene_1 = FakeFalseGene()
    false_gene_2 = FakeFalseGene()
    eq_gene = EqGene(false_gene_1, false_gene_2)

    condition = eq_gene.condition(None, None)

    assert condition


def test_condition_to_string_fakeGenes_returnsValidString():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    eq_gene = EqGene(true_gene_1, true_gene_2)
    eq_gene.weight = 2.0
    eq_gene.result_true = 1
    eq_gene.result_false = -1

    condition_str = eq_gene.to_string()

    assert condition_str == "2.00 x If(Fake EQUALS Fake) then 1 else -1"
