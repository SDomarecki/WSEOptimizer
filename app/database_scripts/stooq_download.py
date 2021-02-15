import os

import wget


class StooqDownloader:
    def __init__(self, tickers: [str], url_base: str, url_end: str, save_dir: str):
        self.tickers = [ticker.lower() for ticker in tickers]
        self.url_base = url_base
        self.url_end = url_end
        self.save_dir = save_dir
        self.fetched = 0

    def fetch_all(self, to_download: int):
        os.makedirs(self.save_dir, exist_ok=True)

        self.delete_ticker_if_data_exists()

        selected_tickers = zip(self.tickers, range(to_download))
        for ticker, i in selected_tickers:
            self.fetch_one(ticker)
            print(f'Downloaded {ticker} [{i}/{to_download}]')

    def fetch_one(self, ticker: str):
        url = f'{self.url_base}{ticker}{self.url_end}'
        wget.download(url, out=self.save_dir)
        self.fetched += 1

    def delete_ticker_if_data_exists(self):
        self.tickers = [ticker for ticker in self.tickers if not os.path.isfile(f'{self.save_dir}/{ticker}_d.csv')]


if __name__ == '__main__':
    stooq_base = 'https://stooq.pl/q/d/l/?s='
    stooq_end = '&i=d'

    # Fetched from BRScraper.get_companies()
    tickers_to_download = [
        'WIG',
        '06N', '08N', '11B', '1AT', '4FM', 'AAT', 'ABE', 'ABS',
        'ACG', 'ACP', 'ACT', 'ADV', 'AGO', 'AGT', 'ALG', 'ALI',
        'ALL', 'ALR', 'AMB', 'AMC', 'AML', 'APE', 'APL', 'APN',
        'APR', 'APT', 'ARH', 'ARR', 'ART', 'ASB', 'ASE', 'ASM',
        'AST', 'ATC', 'ATD', 'ATG', 'ATL', 'ATM', 'ATP', 'ATR',
        'ATS', 'ATT', 'AUG', 'AWB', 'AWM', 'BAH', 'BBD', 'BBT',
        'BCM', 'BDX', 'BDZ', 'BFT', 'BHW', 'BIK', 'BIO', 'BKM',
        'BMC', 'BML', 'BNP', 'BOS', 'BOW', 'BRA', 'BRG', 'BRS',
        'BST', 'CAR', 'CCC', 'CCE', 'CDL', 'CDR', 'CEZ', 'CFI',
        'CIE', 'CIG', 'CLE', 'CLN', 'CMP', 'CMR', 'CNG', 'CNT',
        'COG', 'CPA', 'CPD', 'CPG', 'CPL', 'CPS', 'CRM', 'CTS',
        'CZT', 'DAT', 'DBC', 'DCR', 'DEK', 'DEL', 'DGA', 'DNP',
        'DOM', 'DPL', 'DRE', 'DRP', 'DTR', 'DVL', 'EAH', 'EAT',
        'ECH', 'EDI', 'EEX', 'EFK', 'EHG', 'EKP', 'ELB', 'ELT',
        'ELZ', 'EMC', 'EMT', 'ENA', 'ENE', 'ENG', 'ENI', 'ENP',
        'ENT', 'ERB', 'ERG', 'EST', 'ETL', 'EUC', 'EUR', 'EVE',
        'FEE', 'FER', 'FFI', 'FGT', 'FMF', 'FMG', 'FON', 'FRO',
        'FSG', 'FTE', 'GBK', 'GCN', 'GIF', 'GIFA', 'GKI', 'GLC',
        'GNB', 'GOB', 'GOP', 'GPW', 'GRN', 'GTC', 'GTN', 'HDR',
        'HEL', 'HLD', 'HMI', 'HRP', 'HRS', 'HUB', 'I2D', 'I2D1220',
        'IAG', 'IBS', 'IDA', 'IDG', 'IDM', 'IFC', 'IFI', 'IFR',
        'IIA', 'IMC', 'IMP', 'IMS', 'INC', 'INF', 'ING', 'INK',
        'INL', 'INP', 'INV', 'IPE', 'IPF', 'IPL', 'IPO', 'IRL',
        'ITB', 'ITM', 'IZB', 'IZO', 'IZS', 'JJO', 'JSW', 'JWC',
        'JWW', 'K2I', 'KAN', 'KBD', 'KCH', 'KCI', 'KDM', 'KER',
        'KGH', 'KGL', 'KGN', 'KMP', 'KOM', 'KPD', 'KPL', 'KRC',
        'KRI', 'KRK', 'KRU', 'KSG', 'KSW', 'KTY', 'KVT', 'KZS',
        'LAB', 'LBT', 'LBW', 'LEN', 'LKD', 'LPP', 'LRK', 'LRQ',
        'LSI', 'LTS', 'LTX', 'LVC', 'LWB', 'MAB', 'MAK', 'MBK',
        'MBR', 'MBW', 'MCI', 'MCP', 'MCR', 'MDG', 'MDI', 'MEG',
        'MEX', 'MFO', 'MGT', 'MIL', 'MIR', 'MLG', 'MLK', 'MLS',
        'MNC', 'MOJ', 'MOL', 'MON', 'MPH', 'MRB', 'MRC', 'MSP',
        'MSW', 'MSZ', 'MTL', 'MVP', 'MWT', 'MXC', 'MZA', 'NCT',
        'NET', 'NEU', 'NNG', 'NTT', 'NTU', 'NVA', 'NVG', 'NVT',
        'NWG', 'OAT', 'OBL', 'ODL', 'OEX', 'OPF', 'OPG', 'OPL',
        'OPM', 'OPN', 'OTM', 'OTS', 'OVO', 'PAT', 'PBF', 'PBG',
        'PBX', 'PCE', 'PCG', 'PCR', 'PCX', 'PDZ', 'PEM', 'PEO',
        'PEP', 'PEX', 'PGE', 'PGM', 'PGN', 'PGO', 'PHN', 'PHR',
        'PIW', 'PJP', 'PKN', 'PKO', 'PKP', 'PLW', 'PLX', 'PLY',
        'PLZ', 'PMA', 'PMP', 'PND', 'POZ', 'PPS', 'PRD', 'PRF',
        'PRI', 'PRM', 'PRT', 'PSW', 'PTH', 'PUE', 'PUN', 'PWX',
        'PXM', 'PZU', 'QNT', 'QRS', 'R22', 'RAF', 'RBW', 'RDL',
        'RDN', 'REG', 'RES', 'RFK', 'RHD', 'RLP', 'RMK', 'RNC',
        'RNK', 'RON', 'RPC', 'RVU', 'RWL', 'SAN', 'SCO', 'SEK',
        'SEL', 'SEN', 'SES', 'SFG', 'SFS', 'SGN', 'SGR', 'SHD',
        'SHG', 'SKA', 'SKH', 'SKL', 'SKT', 'SLV', 'SLZ', 'SME',
        'SNK', 'SNT', 'SNW', 'SNX', 'SOL', 'SON', 'SPH', 'SPL',
        'STF', 'STL', 'STP', 'STX', 'SUW', 'SVRS', 'SWD', 'SWG',
        'TAR', 'TBL', 'TEN', 'TIM', 'TLX', 'TMR', 'TNX', 'TOA',
        'TOR', 'TOW', 'TPE', 'TRI', 'TRK', 'TRN', 'TRR', 'TSG',
        'TXM', 'U2K', 'UCG', 'ULG', 'ULM', 'UNI', 'UNT', 'URS',
        'VGO', 'VIN', 'VOT', 'VOX', 'VRG', 'VTI', 'VTL', 'VVD',
        'WAS', 'WAX', 'WIK', 'WIS', 'WLT', 'WOJ', 'WPL', 'WSE',
        'WTN', 'WWL', 'WXF', 'XTB', 'XTP', 'YOL', 'ZAP', 'ZEP',
        'ZMT', 'ZRE', 'ZST', 'ZUE', 'ZUK', 'ZWC'
    ]

    database_dir = 'database/stooq'

    downloader = StooqDownloader(tickers_to_download, stooq_base, stooq_end, database_dir)

    # Stooq locks itself after ~200 downloads to prevent request floods.
    # If script returns blank files (blad.csv) then wait 24h and rerun.
    companies_to_download = 200

    downloader.fetch_all(companies_to_download)
