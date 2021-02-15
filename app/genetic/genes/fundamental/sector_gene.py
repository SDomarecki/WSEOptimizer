import random

from app.genetic.genes.gene import Gene


class SectorGene(Gene):
    possible_sectors = ['GPW: Finanse inne', 'GPW: Deweloperzy',
                        'GPW: Informatyka', 'GPW: Media',
                        'GPW: Handel hurtowy', 'GPW: Budownictwo',
                        'GPW: Przemysł motoryzacyjny', 'GPW: Przemysł farmaceutyczny',
                        'GPW: Przemysł spożywczy', 'GPW: Przemysł metalowy',
                        'GPW: Rynek kapitałowy', 'GPW: Banki', 'GPW: Przemysł elektromaszynowy',
                        'GPW: Usługi inne', 'GPW: Przemysł chemiczny',
                        'GPW: Handel detaliczny', 'GPW: Energetyka',
                        'GPW: Przemysł surowcowy', 'GPW: Przemysł materiałów budowlanych',
                        'GPW: Przemysł drzewny', 'GPW: Hotele i restauracje',
                        'GPW: Przemysł inne', 'GPW: Przemysł tworzyw sztucznych',
                        'GPW: Telekomunikacja', 'GPW: Konglomeraty',
                        'GPW: Przemysł lekki', 'GPW: Przemysł paliwowy',
                        'NewConnect: Usługi inne', 'GPW: Ubezpieczenia',
                        'NewConnect: Informatyka', 'NewConnect: Inwestycje']

    def __init__(self):
        super().__init__()
        self.sector = random.choice(self.possible_sectors)

    def condition(self, company, day):
        return company.sector == self.sector

    def condition_to_string(self):
        return "Sector == " + self.sector
