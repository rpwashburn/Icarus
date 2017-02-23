from Parent_Class import Class
from defences.scales import Scales
from defences.hiding import Hiding
from defences.deathsight import Deathsight
from defences.alertness import Alertness

class Serpent(Class):
    def __init__(self, icarus):
        self.name = "serpent"
        self.icarus = icarus
        Class.__init__(self)

    def get_bash_command(self):
        return "wield left " + self.icarus.character.inventory['shield'] + \
               "/wield right " + self.icarus.character.inventory['whip'] + "/garrote " + self.icarus.target

    def get_defences(self):
        defences = {
            'scales': Scales(),
            'hiding': Hiding(),
            'deathsight': Deathsight(),
            'alertness': Alertness()
        }
        return defences
