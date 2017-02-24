
class DefenceManager(object):
    def __init__(self, icarus):
        self.icarus = icarus
        self.defence_list = self.icarus.character.my_class.get_defences()
        self.reset_defence_priorities()
        print("Defence Manager Initialized")

    def reset_defence_priorities(self):
        for key, defence in self.defence_list.items():
            if defence.priority == 0:
                self.icarus.send_command("CURING PRIORITY DEFENCE " + defence.name + " RESET")
            else:
                self.icarus.send_command("CURING PRIORITY DEFENCE " + defence.name + " " + str(defence.priority))
            print(key + " " + defence.name)

    def defence_added(self):
        self.icarus.defences[self.icarus.gmcp['Char']['Defences']['Add']['name']] = True

    def defence_removed(self):
        for defence in self.icarus.gmcp['Char']['Defences']['Remove']:
            self.icarus.defences[defence] = False

    def reset_defences(self):
        for defence in self.icarus.gmcp['Char']['Defences']['List']:
            self.icarus.defences[defence['name']] = True


