class Company:
    def __init__(self, name, ticker, link):
        self.name = name
        self.ticker = ticker
        self.link = link
        self.fundamentals = {}
        self.technicals = {}

    def append_base_fundamental(self, date, fundamental):
        self.fundamentals[date] = fundamental

    def append_base_technical(self, date, technical):
        self.technicals[date] = technical

    #TODO
    def calculate_all_technicals(self):
        pass

    #TODO calculate_all_fundamentals