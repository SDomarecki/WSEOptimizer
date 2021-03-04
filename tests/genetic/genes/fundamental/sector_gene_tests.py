from datetime import date

from app.genetic.genes.fundamental.sector_gene import SectorGene


def test_condition_sectorEqualToCompared_returnsTrue(company):
    day = date(2000, 6, 1)
    gene = SectorGene()
    gene.sector = "sector:test"

    condition = gene.condition(company, day)

    assert condition


def test_condition_sectorNotEqualToCompared_returnsFalse(
    company,
):
    day = date(2001, 6, 1)
    gene = SectorGene()
    gene.sector = "sector:another_test"

    condition = gene.condition(company, day)

    assert not condition


def test_condition_to_string_validValues_returnsConditionString():
    gene = SectorGene()
    gene.sector = "sector:test"
    gene.weight = 2.0
    gene.result_true = 1
    gene.result_false = -1

    condition_str = gene.to_string()

    assert condition_str == "2.00 x If(Sector == sector:test) then 1 else -1"
