from Parent_Defence import Defence


class Alertness(Defence):
    def __init__(self):
        self.name = "alertness"
        self.priority = 1
        Defence.__init__(self, self.name, self.priority)
