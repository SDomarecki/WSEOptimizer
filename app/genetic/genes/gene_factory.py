import random

from config import Config
from genetic.genes import Gene


class GeneFactory:
    def __init__(self, config: Config):
        self.logic_to_all = config.logic_to_all
        self.fundamental_to_all = config.fundamental_to_all

    def create_random_gene(self) -> Gene:
        if random.uniform(0.0, 1.0) <= self.logic_to_all:
            return self.create_logic_gene()
        else:
            return self.create_non_logic_gene()

    def create_logic_gene(self) -> Gene:
        from logical.and_gene import AndGene
        from logical.or_gene import OrGene
        from logical.xor_gene import XorGene
        from logical.impl_gene import ImplGene
        from logical.eq_gene import EqGene

        possible_genes = [AndGene, OrGene, XorGene, ImplGene, EqGene]
        return random.choice(possible_genes)(self)

    def create_non_logic_gene(self) -> Gene:
        if random.uniform(0.0, 1.0) <= self.fundamental_to_all:
            return self.create_fundamental_gene()
        else:
            return self.create_technical_gene()

    def create_fundamental_gene(self) -> Gene:
        from fundamental.pe_gene import PEGene
        from fundamental.pbv_gene import PBVGene
        from fundamental.ps_gene import PSGene
        from fundamental.pe_now_gene import PENowGene
        from fundamental.pbv_now_gene import PBVNowGene
        from fundamental.ps_now_gene import PSNowGene
        from fundamental.roe_gene import ROEGene
        from fundamental.roa_gene import ROAGene
        from fundamental.sector_gene import SectorGene

        from fundamental.pe_qq import PEqq
        from fundamental.pe_yy import PEyy
        from fundamental.pbv_qq import PBVqq
        from fundamental.pbv_yy import PBVyy
        from fundamental.ps_yy import PSyy
        from fundamental.ps_qq import PSqq
        from fundamental.roe_yy import ROEyy
        from fundamental.roe_qq import ROEqq
        from fundamental.roa_qq import ROAqq

        possible_genes = [PEGene, PENowGene, PEqq, PEyy,
                          PBVGene, PBVNowGene, PBVqq, PBVyy,
                          PSGene, PSNowGene, PSqq, PSyy,
                          ROEGene, ROEqq, ROEyy,
                          ROAGene, ROAqq, ROEyy,
                          SectorGene]
        return random.choice(possible_genes)()

    def create_technical_gene(self) -> Gene:
        from technical.macd_gene import MACDGene
        from technical.rsi_gene import RSIGene
        from technical.trix_gene import TrixGene
        from technical.williams_gene import WilliamsGene
        from technical.mfi_gene import MFIGene
        from technical.roc_gene import ROCGene
        from technical.emv_gene import EMVGene
        from technical.sma15_normalized_gene import SMA15NormalizedGene
        from technical.sma40_normalized_gene import SMA40NormalizedGene
        from technical.ema200_normalized_gene import EMA200NormalizedGene

        possible_genes = [SMA15NormalizedGene, SMA40NormalizedGene, EMA200NormalizedGene,
                          RSIGene, MACDGene, TrixGene, WilliamsGene,
                          MFIGene, ROCGene, EMVGene]
        return random.choice(possible_genes)()
