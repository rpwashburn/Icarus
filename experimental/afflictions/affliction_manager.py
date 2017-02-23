from paralysis import Paralysis


class AfflictionManager(object):
    def __init__(self, icarus):
        self.icarus = icarus
        self.affliction_list = self.get_afflictions()
        print("Affliction Manager Initialized")

    def reset_afflictions(self):
        for key, affliction in self.affliction_list.items():
            self.icarus.send_command("CURING PRIORITY " + affliction.name + " " + str(affliction.priority))
            print(key + " " + affliction.name)

    def get_afflictions(self):
        afflictions = {
            'paralysis': Paralysis()
        }
        return afflictions

    def affliction_added(self):
        self.icarus.afflictions[self.icarus.gmcp['Char']['Afflictions']['Add']['name']] = True

    def affliction_removed(self):
        for affliction in self.icarus.gmcp['Char']['Afflictions']['Remove']:
            self.icarus.afflictions[affliction] = False

    def change_priority(self, affliction, new_priority):
        if affliction in self.affliction_list:
            self.affliction_list[affliction].set_priority(new_priority)
            self.icarus.send_command("CURING PRIORITY " + affliction + " " + str(new_priority))
        else:
            print("UNKNOWN AFFLICTION PRIORITY: " + affliction)
