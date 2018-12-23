class Company:
    def __init__(self, name, ticker, link):
        self.name = name
        self.ticker = ticker
        self.link = link
        self.sector = ""
        self.fundamentals = None  # Pandas DataFrame object!
        self.technicals = None  # Pandas DataFrame object!

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__, indent=4, skipkeys=True, ensure_ascii=False)\
            .encode('utf8')\
            .decode('utf-8')
