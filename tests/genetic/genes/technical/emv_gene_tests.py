from datetime import date

from app.genetic.genes.technical.emv_gene import EMVGene


def test_condition_isLowerCheckAndIndicatorLowerThanComparedValue_returnsTrue(company):
    day = date(2000, 6, 1)
    gene = EMVGene()
    gene.compared_value = 0.0
    gene.comparator = "<"

    condition = gene.condition(company, day)

    assert condition


def test_condition_isLowerCheckAndIndicatorGreaterThanComparedValue_returnsFalse(
    company,
):
    day = date(2001, 6, 1)
    gene = EMVGene()
    gene.compared_value = 0.0
    gene.comparator = "<"

    condition = gene.condition(company, day)

    assert not condition


def test_condition_isGreaterCheckAndIndicatorGreaterThanComparedValue_returnsTrue(
    company,
):
    day = date(2001, 6, 1)
    gene = EMVGene()
    gene.compared_value = 0.0
    gene.comparator = ">"

    condition = gene.condition(company, day)

    assert condition


def test_condition_isGreaterCheckAndIndicatorLowerThanComparedValue_returnsFalse(
    company,
):
    day = date(2000, 6, 1)
    gene = EMVGene()
    gene.compared_value = 0.0
    gene.comparator = ">"

    condition = gene.condition(company, day)

    assert not condition


def test_condition_to_string_validValues_returnsConditionString():
    gene = EMVGene()
    gene.compared_value = 0.0
    gene.comparator = ">"
    gene.weight = 2.0
    gene.result_true = 1
    gene.result_false = -1

    condition_str = gene.to_string()

    assert condition_str == "2.00 x If(EMV > 0.0) then 1 else -1"
