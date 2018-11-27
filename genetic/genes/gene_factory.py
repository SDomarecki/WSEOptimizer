import random

from config import Config
from genetic.genes.gene import Gene


class GeneFactory:

    @staticmethod
    def create_random_gene() -> Gene:
        if random.uniform(0.0, 1.0) <= Config.fundamental_to_all:
            return GeneFactory.create_fundamental_gene()
        else:
            return GeneFactory.create_technical_gene()

    @staticmethod
    def create_fundamental_gene() -> Gene:
        from genetic.genes.fundamental.pe_gene import PEGene
        from genetic.genes.fundamental.pbv_gene import PBVGene
        from genetic.genes.fundamental.ps_gene import PSGene
        from genes.fundamental.pe_now_gene import PENowGene
        from genes.fundamental.pbv_now_gene import PBVNowGene
        from genes.fundamental.ps_now_gene import PSNowGene
        from genetic.genes.fundamental.roe_gene import ROEGene
        from genetic.genes.fundamental.roa_gene import ROAGene
        from genetic.genes.fundamental.sector_gene import SectorGene

        possible_genes = [PEGene, PBVGene, PSGene,
                          PENowGene, PBVNowGene, PSNowGene,
                          ROEGene, ROAGene, SectorGene]
        return random.choice(possible_genes)()

    @staticmethod
    def create_technical_gene() -> Gene:
        from genetic.genes.technical.macd_gene import MACDGene
        from genetic.genes.technical.rsi_gene import RSIGene
        from genetic.genes.technical.trix_gene import TrixGene
        from genetic.genes.technical.williams_gene import WilliamsGene
        from genetic.genes.technical.mfi_gene import MFIGene
        from genetic.genes.technical.momentum_gene import MomentumGene
        from genetic.genes.technical.emv_gene import EMVGene
        from genetic.genes.technical.sma15_normalized_gene import SMA15NormalizedGene
        from genetic.genes.technical.sma40_normalized_gene import SMA40NormalizedGene
        from genetic.genes.technical.ema200_normalized_gene import EMA200NormalizedGene

        possible_genes = [SMA15NormalizedGene, SMA40NormalizedGene, EMA200NormalizedGene,
                          RSIGene, MACDGene, TrixGene, WilliamsGene,
                          MFIGene, MomentumGene, EMVGene]
        return random.choice(possible_genes)()
