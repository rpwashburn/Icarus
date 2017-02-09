#!/usr/bin/env python
import binascii
import zlib
import chardet
import re

LISTEN_PORT = 8902
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"

from twisted.internet import protocol, reactor
import gmcp
import json
import telnet_values
import icarus_globals


# Adapted from http://stackoverflow.com/a/15645169/221061
class IcarusProtocol(protocol.Protocol):
    def __init__(self):
        self.full_data = ""
        self.gmcp = gmcp.get_initial_gmcp()
        self.afflictions = {}

    def send_command(self, command):
        self.transport.write(command + "\n")

    def send_to_mudlet(self, data):
        self.transport.write(icarus_globals.icarus_mudlet_key + ": " + data + "\n")

    def process_command(self, icarus_data):
        print("-----PROCESSING COMMAND------")
        icarus_command = icarus_data.strip("\r\n").split(": ")[1]
        print(icarus_command)
        self.send_command(icarus_command)
        print("-----------------------------")

    def process_gmcp(self, gmcp_lines):

        for gmcp_line in gmcp_lines:
            # print("---processing: ")
            # print gmcp_line
            # print("\n\n\n\n")
            if 'Char.Afflictions.Add' in gmcp_line:
                self.gmcp = gmcp.char_afflictions_add(self.gmcp, gmcp_line)
            elif 'Char.Afflictions.Remove' in gmcp_line:
                self.gmcp = gmcp.char_afflictions_remove(self.gmcp, gmcp_line)
            elif 'Char.Afflictions.List' in gmcp_line:
                self.gmcp = gmcp.char_afflictions_list(self.gmcp, gmcp_line)
            elif 'Char.Defences.Add' in gmcp_line:
                self.gmcp = gmcp.char_defences_add(self.gmcp, gmcp_line)
            elif 'Char.Defences.Remove' in gmcp_line:
                self.gmcp = gmcp.char_defences_remove(self.gmcp, gmcp_line)
            elif 'Char.Defences.List' in gmcp_line:
                self.gmcp = gmcp.char_defences_list(self.gmcp, gmcp_line)
            elif 'Char.Items.List' in gmcp_line:
                self.gmcp = gmcp.char_items_list(self.gmcp, gmcp_line)
            elif 'Char.Items.Add' in gmcp_line:
                self.gmcp = gmcp.char_items_add(self.gmcp, gmcp_line)
            elif 'Char.Items.Remove' in gmcp_line:
                self.gmcp = gmcp.char_items_remove(self.gmcp, gmcp_line)
            elif 'Char.Name' in gmcp_line:
                self.gmcp = gmcp.char_name(self.gmcp, gmcp_line)
            elif 'Char.Skills.Groups' in gmcp_line:
                self.gmcp = gmcp.char_skills_groups(self.gmcp, gmcp_line)
            elif 'Char.StatusVars' in gmcp_line:
                self.gmcp = gmcp.char_status_vars(self.gmcp, gmcp_line)
            elif 'Char.Status' in gmcp_line:
                self.gmcp = gmcp.char_status(self.gmcp, gmcp_line)
            elif 'Char.Vitals' in gmcp_line:
                self.gmcp = gmcp.char_vitals(self.gmcp, gmcp_line)
            elif 'Room.Info' in gmcp_line:
                self.gmcp = gmcp.room_info(self.gmcp, gmcp_line)
            elif 'Room.Players' in gmcp_line:
                self.gmcp = gmcp.room_players(self.gmcp, gmcp_line)
            elif 'Room.AddPlayer' in gmcp_line:
                self.gmcp = gmcp.room_add_player(self.gmcp, gmcp_line)
            elif 'Room.RemovePlayer' in gmcp_line:
                self.gmcp = gmcp.room_remove_player(self.gmcp, gmcp_line)
            else:
                print("Unknown GMCP:")
                print telnet_values.sub_telnet_codes(gmcp_line)
                print("\n\n\n\n")

    def process_regex(self, regex_lines):
        if re.search('(\w+) sit yourself down\.', regex_lines):
            self.send_command("stand")


    # Client => Proxy
    def dataReceived(self, data):

        print("----------Processing Data From Achaea----------------")
        if icarus_globals.icarus_command_key in data:
            self.process_command(data)
            return

        if not data.endswith(telnet_values.GA):
            self.full_data += data
            return
        self.full_data += data

        # print("---------------SUBBED DATA------------")
        # subbed_data = telnet_values.sub_telnet_codes(self.full_data)
        # print(subbed_data)
        # print("--------------------------------------")

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
        # print("--------------------------------------------------------")
        self.process_gmcp(gmcp_lines)
        self.process_regex(regex_lines)
        print("----------------CURRENT GMCP--------------------")
        print self.gmcp
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