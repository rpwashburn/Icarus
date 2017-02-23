from Parent_Character import Character


class Sventis(Character):
    def __init__(self, icarus):
        self.name = "Sventis"
        self.icarus = icarus
        self.inventory = {
            'shield': 'shield482181',
            'whip': 'whip229254',
            'pack': 'backpack422896'
        }
        self.tutor = "Damaris"
        Character.__init__(self)


