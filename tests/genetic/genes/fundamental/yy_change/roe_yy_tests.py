from datetime import date

from app.genetic.genes.fundamental.yy_change.roe_yy import ROEyy


def test_condition_isLowerCheckAndRatioLowerThanComparedValue_returnsTrue(company):
    day = date(2001, 6, 1)  # 2001/Q1
    gene = ROEyy()
    gene.comparator = "<"
    gene.compared_value = 8.0

    condition = gene.condition(company, day)

    assert condition


def test_condition_isLowerCheckAndRatioGreaterThanComparedValue_returnsFalse(
    company,
):
    day = date(2001, 6, 1)
    gene = ROEyy()
    gene.comparator = "<"
    gene.compared_value = 2.0

    condition = gene.condition(company, day)

    assert not condition


def test_condition_isGreaterCheckAndRatioGreaterThanComparedValue_returnsTrue(
    company,
):
    day = date(2001, 6, 1)
    gene = ROEyy()
    gene.comparator = ">"
    gene.compared_value = 2.5

    condition = gene.condition(company, day)

    assert condition


def test_condition_isGreaterCheckAndRatioLowerThanComparedValue_returnsFalse(
    company,
):
    day = date(2001, 6, 1)
    gene = ROEyy()
    gene.comparator = ">"
    gene.compared_value = 6.0

    condition = gene.condition(company, day)

    assert not condition


def test_condition_to_string_validValues_returnsConditionString():
    gene = ROEyy()
    gene.comparator = ">"
    gene.compared_value = 1.5
    gene.weight = 2.0
    gene.result_true = 1
    gene.result_false = -1

    condition_str = gene.to_string()

    assert condition_str == "2.00 x If(ROE / PrevY ROE > 1.50) then 1 else -1"
