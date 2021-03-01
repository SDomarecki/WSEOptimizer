import random

from app.config import Config
from app.genetic.genes.gene import Gene
from app.genetic.genes.logical.and_gene import AndGene
from app.genetic.genes.logical.or_gene import OrGene
from app.genetic.genes.logical.xor_gene import XorGene
from app.genetic.genes.logical.impl_gene import ImplGene
from app.genetic.genes.logical.eq_gene import EqGene
from app.genetic.genes.fundamental.pe_gene import PEGene
from app.genetic.genes.fundamental.pbv_gene import PBVGene
from app.genetic.genes.fundamental.ps_gene import PSGene
from app.genetic.genes.fundamental.pe_now_gene import PENowGene
from app.genetic.genes.fundamental.pbv_now_gene import PBVNowGene
from app.genetic.genes.fundamental.ps_now_gene import PSNowGene
from app.genetic.genes.fundamental.roe_gene import ROEGene
from app.genetic.genes.fundamental.roa_gene import ROAGene
from app.genetic.genes.fundamental.sector_gene import SectorGene

from app.genetic.genes.fundamental.pe_qq import PEqq
from app.genetic.genes.fundamental.pe_yy import PEyy
from app.genetic.genes.fundamental.pbv_qq import PBVqq
from app.genetic.genes.fundamental.pbv_yy import PBVyy
from app.genetic.genes.fundamental.ps_yy import PSyy
from app.genetic.genes.fundamental.ps_qq import PSqq
from app.genetic.genes.fundamental.roe_yy import ROEyy
from app.genetic.genes.fundamental.roe_qq import ROEqq
from app.genetic.genes.fundamental.roa_qq import ROAqq

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


class GeneFactory:
    logic_genes = [AndGene, OrGene, XorGene, ImplGene, EqGene]

    fundamental_genes = [
        PEGene,
        PENowGene,
        PEqq,
        PEyy,
        PBVGene,
        PBVNowGene,
        PBVqq,
        PBVyy,
        PSGene,
        PSNowGene,
        PSqq,
        PSyy,
        ROEGene,
        ROEqq,
        ROEyy,
        ROAGene,
        ROAqq,
        ROEyy,
        SectorGene,
    ]

    technical_genes = [
        SMA15NormalizedGene,
        SMA40NormalizedGene,
        EMA200NormalizedGene,
        RSIGene,
        MACDGene,
        TrixGene,
        WilliamsGene,
        MFIGene,
        ROCGene,
        EMVGene,
    ]

    def __init__(self, config: Config):
        self.logic_to_all = config.logic_to_all
        self.fundamental_to_all = config.fundamental_to_all

    def create_random_gene(self) -> Gene:
        if random.uniform(0.0, 1.0) <= self.logic_to_all:
            return self.create_logic_gene()
        return self.create_non_logic_gene()

    def create_logic_gene(self) -> Gene:
        return random.choice(GeneFactory.logic_genes)(self)

    def create_non_logic_gene(self) -> Gene:
        if random.uniform(0.0, 1.0) <= self.fundamental_to_all:
            return self.create_fundamental_gene()
        return GeneFactory.create_technical_gene()

    @classmethod
    def create_fundamental_gene(cls) -> Gene:
        return random.choice(cls.fundamental_genes)()

    @classmethod
    def create_technical_gene(cls) -> Gene:
        return random.choice(cls.technical_genes)()
