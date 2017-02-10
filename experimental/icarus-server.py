#!/usr/bin/env python

from twisted.internet import protocol, reactor
import gmcp
import telnet_values
import icarus_globals
import icarus_triggers
import icarus_aliases
import time

LISTEN_PORT = 8902
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"


# Adapted from http://stackoverflow.com/a/15645169/221061
class IcarusProtocol(protocol.Protocol):
    def __init__(self):
        self.full_data = ""
        self.gmcp = gmcp.get_initial_gmcp()
        self.afflictions = {}
        self.Login = True

    def send_gmcp(self, data):
        icarus_gmcp = data.strip("\r\n").split(": ")[1]
        self.transport.write(telnet_values.IAC + telnet_values.SB + telnet_values.GMCP + icarus_gmcp +
                             telnet_values.IAC + telnet_values.SE)

    def send_command(self, command):
        self.transport.write(command + "\n")

    def send_user_command(self, command):
        self.transport.write(command + "\n")

    def send_to_mudlet(self, data):
        self.transport.write(icarus_globals.icarus_mudlet_key + ": " + data + "\n")

    def process_command(self, icarus_data):
        print("-----PROCESSING COMMAND------")
        icarus_command = icarus_data.strip("\r\n").split(": ")[1]
        icarus_command = icarus_aliases.process_aliases(self, icarus_command)
        print(icarus_command)
        self.send_user_command(icarus_command)
        print("-----------------------------")

    def process_function(self, icarus_data):
        print("-----PROCESSING FUNCTION------")
        icarus_function = icarus_data.strip("\r\n").split(": ")[1]
        function = 'self.' + icarus_function + '()'
        eval(function)
        print("-----------------------------")

    def display_gmcp(self):
        print(self.gmcp)

    # Client => Proxy
    def dataReceived(self, data):

        print("----------Processing Data From Achaea----------------")
        print("---------------SUBBED DATA------------")
        subbed_data = telnet_values.sub_telnet_codes(data)
        print(subbed_data)
        print("--------------------------------------")

        if self.Login:
            self.send_gmcp(icarus_globals.icarus_gmcp_key + ': Char.Items.Inv ""')
            self.Login = False

        if icarus_globals.icarus_gmcp_key in data:
            self.send_gmcp(data)
            return

        if icarus_globals.icarus_command_key in data:
            self.process_command(data)
            self.full_data += data
            return

        if icarus_globals.icarus_function_key in data:
            self.process_function(data)
            return

        if not data.endswith(telnet_values.GA):
            self.full_data += data
            return
        self.full_data += data

        game_lines = []
        gmcp_lines = []

        line_data = self.full_data.split(telnet_values.NL)
        for line in line_data:
            gmcp_split = line.split(telnet_values.IAC + telnet_values.SB + telnet_values.GMCP)
            for split in gmcp_split:
                if 'Room.' in split or 'Char.' in split:
                    gmcp_lines.append(split)
                else:
                    game_lines.append(split)

        regex_lines = "".join(game_lines)
        # print("---------------------GMCP DATA---------------------------")
        # print("\n\n\n".join(gmcp_lines))
        # print("---------------------------------------------------------")
        gmcp.process_gmcp(self, gmcp_lines)
        icarus_triggers.process_triggers(self, regex_lines)
        # print("----------------CURRENT GMCP--------------------")
        # print self.gmcp
        print("-----------------------------------------------------------------------------------------------------")
        self.full_data = ""


def main():
    print("Starting Icarus Regex Server on port " + str(LISTEN_PORT) + "...")
    factory = protocol.ServerFactory()
    factory.protocol = IcarusProtocol

    # Starting Server for twisted-proxy to connect to
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
