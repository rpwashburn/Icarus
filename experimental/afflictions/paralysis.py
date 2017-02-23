from Parent_Affliction import Affliction


class Paralysis(Affliction):
    def __init__(self):
        self.name = "paralysis"
        self.priority = 1
        Affliction.__init__(self, self.name, self.priority)
