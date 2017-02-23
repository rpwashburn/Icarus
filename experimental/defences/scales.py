from Parent_Defence import Defence


class Scales(Defence):
    def __init__(self):
        self.name = "scales"
        self.priority = 1
        Defence.__init__(self, self.name, self.priority)
