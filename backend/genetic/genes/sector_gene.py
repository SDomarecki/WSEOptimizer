from backend.genetic.gene import Gene
import random


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
        self.result_true = random.uniform(-10, 10)
        self.result_false = random.uniform(-10, 10)
        self.sector = random.choice(self.possible_sectors)

    def get_substrength(self, company, day):
        company_sector = company.sector

        if company_sector == self.sector:
            return self.result_true
        else:
            return self.result_false
