# if(indicator comparator value):
#     return result_true
# else:
#     return result_false
#
# W uogólnieniu value i indicator mogłyby być zamienne oraz result_true/false byłyby kolejnymi genami
import random


class Gene:

    def get_substrength(self, company, day):
        pass


def create_random_gene():
    from backend.genetic.genes.pe_gene import PEGene
    from backend.genetic.genes.pbv_gene import PBVGene
    from backend.genetic.genes.ps_gene import PSGene
    from backend.genetic.genes.roe_gene import ROEGene
    from backend.genetic.genes.roa_gene import ROAGene

    from backend.genetic.genes.macd_gene import MACDGene
    from backend.genetic.genes.rsi_gene import RSIGene
    from backend.genetic.genes.trix_gene import TrixGene
    from backend.genetic.genes.williams_gene import WilliamsGene
    from backend.genetic.genes.mfi_gene import MFIGene
    from backend.genetic.genes.momentum_gene import MomentumGene
    from backend.genetic.genes.emv_gene import EMVGene

    from backend.genetic.genes.sma15_vs_price_gene import SMA15VsPriceGene
    from backend.genetic.genes.sma40_vs_price_gene import SMA40VsPriceGene
    from backend.genetic.genes.ema200_vs_price_gene import EMA200VsPriceGene
    from backend.genetic.genes.sma15_normalized_gene import SMA15NormalizedGene
    from backend.genetic.genes.sma40_normalized_gene import SMA40NormalizedGene
    from backend.genetic.genes.ema200_normalized_gene import EMA200NormalizedGene

    from backend.genetic.genes.sector_gene import SectorGene
    possible_indicators = [PEGene, PBVGene, PSGene, ROEGene, ROAGene,
                           SMA15VsPriceGene, SMA40VsPriceGene, EMA200VsPriceGene,
                           SMA15NormalizedGene, SMA40NormalizedGene, EMA200NormalizedGene,
                           RSIGene, MACDGene, TrixGene, WilliamsGene,
                           MFIGene, MomentumGene, EMVGene, SectorGene]

    return random.choice(possible_indicators)()
