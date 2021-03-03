from datetime import date

from app.genetic.genes.technical.sma15_normalized_gene import SMA15NormalizedGene


def test_condition_isLowerCheckAndIndicatorLowerThanComparedValue_returnsTrue(company):
    day = date(2000, 6, 1)
    gene = SMA15NormalizedGene()
    gene.comparator = "<"
    gene.compared_value = 1.5

    condition = gene.condition(company, day)

    assert condition


def test_condition_isLowerCheckAndIndicatorGreaterThanComparedValue_returnsFalse(
    company,
):
    day = date(2001, 6, 1)
    gene = SMA15NormalizedGene()
    gene.comparator = "<"
    gene.compared_value = 1.5

    condition = gene.condition(company, day)

    assert not condition


def test_condition_isGreaterCheckAndIndicatorGreaterThanComparedValue_returnsTrue(
    company,
):
    day = date(2001, 6, 1)
    gene = SMA15NormalizedGene()
    gene.comparator = ">"
    gene.compared_value = 1.5

    condition = gene.condition(company, day)

    assert condition


def test_condition_isGreaterCheckAndIndicatorLowerThanComparedValue_returnsFalse(
    company,
):
    day = date(2000, 6, 1)
    gene = SMA15NormalizedGene()
    gene.comparator = ">"
    gene.compared_value = 1.5

    condition = gene.condition(company, day)

    assert not condition


def test_condition_to_string_validValues_returnsConditionString():
    gene = SMA15NormalizedGene()
    gene.comparator = ">"
    gene.compared_value = 1.5
    gene.weight = 2.0
    gene.result_true = 1
    gene.result_false = -1

    condition_str = gene.to_string()

    assert condition_str == "2.00 x If(SMA15Norm > 1.50) then 1 else -1"
