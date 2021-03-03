from app.genetic.genes.logical.impl_gene import ImplGene
from tests.genetic.genes.logic.fake_false_gene import FakeFalseGene
from tests.genetic.genes.logic.fake_true_gene import FakeTrueGene


def test_condition_bothTrue_returnTrue():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    impl_gene = ImplGene(true_gene_1, true_gene_2)

    condition = impl_gene.condition(None, None)

    assert condition


def test_condition_firstFalse_secondTrue_returnTrue():
    false_gene = FakeFalseGene()
    true_gene = FakeTrueGene()
    impl_gene = ImplGene(false_gene, true_gene)

    condition = impl_gene.condition(None, None)

    assert condition


def test_condition_firstTrue_secondFalse_returnFalse():
    true_gene = FakeTrueGene()
    false_gene = FakeFalseGene()
    impl_gene = ImplGene(true_gene, false_gene)

    condition = impl_gene.condition(None, None)

    assert not condition


def test_condition_bothFalse_returnTrue():
    false_gene_1 = FakeFalseGene()
    false_gene_2 = FakeFalseGene()
    impl_gene = ImplGene(false_gene_1, false_gene_2)

    condition = impl_gene.condition(None, None)

    assert condition


def test_condition_to_string_fakeGenes_returnsValidString():
    true_gene_1 = FakeTrueGene()
    true_gene_2 = FakeTrueGene()
    impl_gene = ImplGene(true_gene_1, true_gene_2)
    impl_gene.weight = 2.0
    impl_gene.result_true = 1
    impl_gene.result_false = -1

    condition_str = impl_gene.to_string()

    assert condition_str == "2.00 x If(IF Fake THEN Fake) then 1 else -1"
