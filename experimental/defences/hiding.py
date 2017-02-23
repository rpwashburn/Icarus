from Parent_Defence import Defence


class Hiding(Defence):
    def __init__(self):
        self.name = "hiding"
        self.priority = 0
        Defence.__init__(self, self.name, self.priority)
