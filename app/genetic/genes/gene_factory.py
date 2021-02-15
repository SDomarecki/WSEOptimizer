import random

from app.genetic.genes.gene import Gene


class GeneFactory:

    @staticmethod
    def create_random_gene() -> Gene:
        if random.uniform(0.0, 1.0) <= 0.1:
            return GeneFactory.create_logic_gene()
        else:
            return GeneFactory.create_non_logic_gene()

    @staticmethod
    def create_logic_gene() -> Gene:
        from genes.logical.and_gene import AndGene
        from genes.logical.or_gene import OrGene
        from genes.logical.xor_gene import XorGene
        from genes.logical.impl_gene import ImplGene
        from genes.logical.eq_gene import EqGene

        possible_genes = [AndGene, OrGene, XorGene, ImplGene, EqGene]
        return random.choice(possible_genes)()

    @staticmethod
    def create_non_logic_gene() -> Gene:
        if random.uniform(0.0, 1.0) <= 0.7:
            return GeneFactory.create_fundamental_gene()
        else:
            return GeneFactory.create_technical_gene()

    @staticmethod
    def create_fundamental_gene() -> Gene:
        from app.genetic.genes.fundamental.pe_gene import PEGene
        from app.genetic.genes.fundamental.pbv_gene import PBVGene
        from app.genetic.genes.fundamental.ps_gene import PSGene
        from genes.fundamental.pe_now_gene import PENowGene
        from genes.fundamental.pbv_now_gene import PBVNowGene
        from genes.fundamental.ps_now_gene import PSNowGene
        from app.genetic.genes.fundamental.roe_gene import ROEGene
        from app.genetic.genes.fundamental.roa_gene import ROAGene
        from app.genetic.genes.fundamental.sector_gene import SectorGene

        from genes.fundamental.pe_qq import PEqq
        from genes.fundamental.pe_yy import PEyy
        from genes.fundamental.pbv_qq import PBVqq
        from genes.fundamental.pbv_yy import PBVyy
        from genes.fundamental.ps_yy import PSyy
        from genes.fundamental.ps_qq import PSqq
        from genes.fundamental.roe_yy import ROEyy
        from genes.fundamental.roe_qq import ROEqq
        from genes.fundamental.roa_qq import ROAqq

        possible_genes = [PEGene, PENowGene, PEqq, PEyy,
                          PBVGene, PBVNowGene, PBVqq, PBVyy,
                          PSGene, PSNowGene, PSqq, PSyy,
                          ROEGene, ROEqq, ROEyy,
                          ROAGene, ROAqq, ROEyy,
                          SectorGene]
        return random.choice(possible_genes)()

    @staticmethod
    def create_technical_gene() -> Gene:
        from app.genetic.genes.technical.macd_gene import MACDGene
        from app.genetic.genes.technical.rsi_gene import RSIGene
        from app.genetic.genes.technical.trix_gene import TrixGene
        from app.genetic.genes.technical.williams_gene import WilliamsGene
        from app.genetic.genes.technical.mfi_gene import MFIGene
        from app.genetic.genes.technical.roc_gene import ROCGene
        from app.genetic.genes.technical.emv_gene import EMVGene
        from app.genetic.genes.technical.sma15_normalized_gene import SMA15NormalizedGene
        from app.genetic.genes.technical.sma40_normalized_gene import SMA40NormalizedGene
        from app.genetic.genes.technical.ema200_normalized_gene import EMA200NormalizedGene

        possible_genes = [SMA15NormalizedGene, SMA40NormalizedGene, EMA200NormalizedGene,
                          RSIGene, MACDGene, TrixGene, WilliamsGene,
                          MFIGene, ROCGene, EMVGene]
        return random.choice(possible_genes)()
