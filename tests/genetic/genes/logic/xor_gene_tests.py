from app.genetic.genes.logical.xor_gene import XorGene
from tests.genetic.genes.fake_false_gene import FakeFalseGene
from tests.genetic.genes.fake_true_gene import FakeTrueGene


def test_condition_bothTrue_returnFalse():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    xor_gene = XorGene(true_gene_1, true_gene_2)

    condition = xor_gene.condition(None, None)

    assert not condition


def test_condition_oneTrue_returnTrue():
    true_gene = FakeTrueGene()
    false_gene = FakeFalseGene()
    xor_gene = XorGene(true_gene, false_gene)

    condition = xor_gene.condition(None, None)

    assert condition


def test_condition_bothFalse_returnFalse():
    false_gene_1 = FakeFalseGene()
    false_gene_2 = FakeFalseGene()
    xor_gene = XorGene(false_gene_1, false_gene_2)

    condition = xor_gene.condition(None, None)

    assert not condition


def test_condition_to_string_fakeGenes_returnsValidString():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    xor_gene = XorGene(true_gene_1, true_gene_2)
    xor_gene.weight = 2.0
    xor_gene.result_true = 1
    xor_gene.result_false = -1

    condition_str = xor_gene.to_string()

    assert condition_str == "2.00 x If(Fake XOR Fake) then 1 else -1"
