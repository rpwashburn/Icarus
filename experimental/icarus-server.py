#!/usr/bin/env python

from twisted.internet import protocol, reactor
import gmcp
import telnet_values
import icarus_globals
import icarus_triggers
import icarus_aliases
import events.icarus_events
import re
import time
from afflictions.affliction_manager import AfflictionManager
from defences.defence_manager import DefenceManager

LISTEN_PORT = 8902
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"


# Adapted from http://stackoverflow.com/a/15645169/221061
class IcarusProtocol(protocol.Protocol):
    def __init__(self):
        self.full_data = ""
        self.gmcp = gmcp.get_initial_gmcp()
        self.afflictions = {}
        self.defences = {}
        self.Login = True
        self.character = False
        self.target = ""
        self.affliction_manager = AfflictionManager(self)
        self.defence_manager = False

    def send_gmcp(self, data):
        icarus_gmcp = data.strip("\r\n").split(": ")[1]
        self.transport.write(telnet_values.IAC + telnet_values.SB + telnet_values.GMCP + icarus_gmcp +
                             telnet_values.IAC + telnet_values.SE)

    def send_command(self, command):
        self.transport.write("setalias icarus " + command + "\n")
        self.transport.write("icarus\n")

    def send_attack(self, command):
        self.transport.write("clearqueue all\n")
        self.send_command(command)

    def send_to_mudlet(self, data):
        self.transport.write(icarus_globals.icarus_mudlet_key + ": " + data + "\n")

    def reset_prompt_variables(self):
        return

    def process_command(self, icarus_data):
        print("-----PROCESSING COMMAND------")
        match_objects = re.finditer(r'(.*)icarus-command\: (\w(?:[-\w]*\w)?)(.*)', icarus_data)
        for match_obj in match_objects:
            icarus_command = match_obj.group(2).strip()
            icarus_aliases.process_aliases(self, icarus_command)
            return icarus_data.replace(match_obj.group(0), "")
        else:
            print "No match on icarus command for: "
            print(telnet_values.sub_telnet_codes(icarus_data))
        print("-----------------------------")
        return icarus_data

    def process_event(self, icarus_data):
        print("-----PROCESSING EVENT------")
        match_objects = re.finditer(r'(.*)icarus-event\: (\w(?:[-\w]*\w)?)(.*)', icarus_data)
        for match_obj in match_objects:
            icarus_event = match_obj.group(2).strip()
            events.icarus_events.process_events(self, icarus_event)
            return icarus_data.replace(match_obj.group(0), "")
        else:
            print "No match on icarus event for: "
            print(telnet_values.sub_telnet_codes(icarus_data))
        print("-----------------------------")
        return icarus_data

    def process_function(self, icarus_data):
        print("-----PROCESSING FUNCTION------")
        icarus_function = icarus_data.strip("\r\n").split(": ")[1]
        function = 'self.' + icarus_function + '()'
        eval(function)
        print("-----------------------------")

    def display_gmcp(self):
        print(self.gmcp)

    def display_defences(self):
        print(self.defences)

    def set_target(self, target):
        print("Setting target to: " + target)
        self.target = target

    # Client => Proxy
    def dataReceived(self, data):

        if self.Login:
            self.send_gmcp(icarus_globals.icarus_gmcp_key + ': Char.Items.Inv ""')
            self.send_command("score")
            self.send_command("qsc")
            print("----------------GMCP AT LOGIN---------------------")
            print(self.gmcp)
            print("--------------------------------------------------")
            self.Login = False

        if self.gmcp['Char']['Status'] and not self.character:
            print self.gmcp['Char']['Status']
            if self.gmcp['Char']['Status']['name'] == 'Sventis':
                from characters.sventis import Sventis
                self.character = Sventis(self)
                print self.character.my_class.name
            self.character.print_name()
            self.defence_manager = DefenceManager(self)

        print("----------Processing Data From Achaea----------------")
        # print("---------------SUBBED DATA------------")
        # subbed_data = telnet_values.sub_telnet_codes(data)
        # print(subbed_data)
        # print("--------------------------------------")

        self.full_data += data
        if icarus_globals.icarus_command_key in self.full_data:
            self.full_data = self.process_command(self.full_data)

        if icarus_globals.icarus_event_key in self.full_data:
            self.full_data = self.process_event(self.full_data)

        game_lines = []
        gmcp_lines = []

        line_data = self.full_data.split(telnet_values.NL)
        for line in line_data:
            # print("-------------------------LINE DATA-------------------------")
            # print telnet_values.sub_telnet_codes(line)
            # print("-----------------------------------------------------------")
            gmcp_split = line.split(telnet_values.IAC + telnet_values.SB + telnet_values.GMCP)
            for split in gmcp_split:
                # icarus_triggers.process_triggers(self, split)
                if 'Room.' in split or 'Char.' in split:
                    gmcp_lines.append(split)
                else:
                    game_lines.append(split)

        if self.full_data.endswith(telnet_values.GA):
            gmcp.process_gmcp(self, gmcp_lines=gmcp_lines)
            self.full_data = ""

        # regex_lines = "".join(game_lines)
        # print("---------------------GMCP DATA---------------------------")
        # print("\n\n\n".join(gmcp_lines))
        # print("---------------------------------------------------------")
        # print("----------------CURRENT GMCP--------------------")
        # print self.gmcp
        print("----------------CURRENT DEFENCES--------------------")
        print self.defences
        print("----------------CURRENT Afflictions--------------------")
        print self.afflictions
        print("-----------------------------------------------------------------------------------------------------")


def main():
    print("Starting Icarus Regex Server on port " + str(LISTEN_PORT) + "...")
    factory = protocol.ServerFactory()
    factory.protocol = IcarusProtocol

    # Starting Server for twisted-proxy to connect to
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
