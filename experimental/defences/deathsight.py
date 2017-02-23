from Parent_Defence import Defence


class Deathsight(Defence):
    def __init__(self):
        self.name = "deathsight"
        self.priority = 1
        Defence.__init__(self, self.name, self.priority)
