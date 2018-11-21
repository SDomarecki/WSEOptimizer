from genetic.genes.gene import Gene
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
        super().__init__()
        self.sector = random.choice(self.possible_sectors)

    def condition(self, company, day):
        company_sector = company.sector

        if company_sector == self.sector:
            return True
        else:
            return False

    def to_string(self):
        return "If(Sector == " \
               + self.sector \
               + ") then " \
               + str(self.result_true) \
               + " else " \
               + str(self.result_false)