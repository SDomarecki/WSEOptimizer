# if(indicator comparator value):
#     return result_true
# else:
#     return result_false
#
# W uogólnieniu value i indicator mogłyby być zamienne oraz result_true/false byłyby kolejnymi genami
import random
import pandas as pd

class Gene:

    def get_substrength(self, company, day):
        pass

    @staticmethod
    def date_to_quarter(date):
        return str(date.year) + "/Q" + str(pd.Timestamp(date).quarter)


def create_random_gene():
    from genetic.genes.pe_gene import PEGene
    from genetic.genes.pbv_gene import PBVGene
    from genetic.genes.ps_gene import PSGene
    from genetic.genes.roe_gene import ROEGene
    from genetic.genes.roa_gene import ROAGene

    from genetic.genes.macd_gene import MACDGene
    from genetic.genes.rsi_gene import RSIGene
    from genetic.genes.trix_gene import TrixGene
    from genetic.genes.williams_gene import WilliamsGene
    from genetic.genes.mfi_gene import MFIGene
    from genetic.genes.momentum_gene import MomentumGene
    from genetic.genes.emv_gene import EMVGene

    from genetic.genes.sma15_normalized_gene import SMA15NormalizedGene
    from genetic.genes.sma40_normalized_gene import SMA40NormalizedGene
    from genetic.genes.ema200_normalized_gene import EMA200NormalizedGene

    from genetic.genes.sector_gene import SectorGene
    possible_indicators = [PEGene, PBVGene, PSGene, ROEGene, ROAGene, SectorGene,
                           SMA15NormalizedGene, SMA40NormalizedGene, EMA200NormalizedGene,
                           RSIGene, MACDGene, TrixGene, WilliamsGene,
                           MFIGene, MomentumGene, EMVGene]

    return random.choice(possible_indicators)()
