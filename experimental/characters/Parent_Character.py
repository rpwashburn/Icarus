from classes.serpent import Serpent


class Character:
    def __init__(self):
        print("---Initializing Character----")
        self.print_name()
        print("-----------------------------")
        self.afflictions = {
            'prone': False
        }
        self.my_class = self.determine_class()
        self.initiate_curing()

    def determine_class(self):
        if self.icarus.gmcp['Char']['Status']['class'] == 'Serpent':
            return Serpent(self.icarus)

    def print_name(self):
        print(self.name)

    def initiate_curing(self):
        self.icarus.send_command("CURING ON")
        self.icarus.send_command("CURING AFFLICTIONS ON")
        self.icarus.send_command("CURING DEFENCES ON")
        self.icarus.send_command("CURING SIPPING ON")
        self.icarus.send_command("CURING SIPHEALTH 95")
        self.icarus.send_command("CURING SIPMANA 95")
        self.icarus.send_command("CURING MOSSHEALTH 75")
        self.icarus.send_command("CURING MOSSMANA 75")
        self.icarus.send_command("CURING PRIORITY HEALTH")
        self.icarus.send_command("CURING FOCUS OFF")
        self.icarus.send_command("CURING FOCUS FIRST")
        self.icarus.send_command("CURING TREE OFF")
        self.icarus.send_command("CURING CLOTAT 25")
        self.icarus.affliction_manager.reset_affliction_priorities()




