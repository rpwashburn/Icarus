#!/usr/bin/env python
import binascii
import zlib
import chardet
import re

LISTEN_PORT = 8902
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"

from twisted.internet import protocol, reactor

""" TELNET VALUES """
NULL = chr(0)       # NULL
ECHO = chr(1)       # Telnet Echo
SGA = chr(3)        # Suppress Go-Ahead
BEL = chr(7)        # Produces an audible or visible signal (which does NOT move the print head).
BS = chr(8)         # Moves the print head one character position towards the left margin.
HT = chr(9)         # Moves the printer to the next horizontal tab stop.
LF = chr(10)        # Moves the printer to the next print line, keeping the same horizontal position.
NL = chr(10)        # Newline
VT = chr(11)        # Moves the printer to the next vertical tab stop.
FF = chr(12)        # Moves the printer to the top of the next page, keeping the same horizontal position.
CR = chr(13)        # Carriage Return
EOR = chr(25)       # End of record
ESC = chr(27)       # Escape byte
NAWS = chr(31)      # Negotiate About Window Size
LINEMODE = chr(34)
COMPRESS = chr(85)   # MCCP Version 1
COMPRESS2 = chr(86)  # MCCP Version 2
ATCP = chr(200)     # ATCP
GMCP = chr(201)     # GMCP
EORD = chr(239)     # End of Record indicator
SE = chr(240)       # End of subnegotiation parameters
NOP = chr(241)      # No operation
DM = chr(242)       # "Data Mark": The data stream portion of a Synch.  This should always be accompanied by a TCP Urgent notification.
BRK = chr(243)      # NVT character Break.
IP = chr(244)       # The function Interrupt Process.
AO = chr(245)       # The function Abort Output
AYT = chr(246)      # The function Are You There.
EC = chr(247)       # The function Erase Character.
EL = chr(248)       # The function Erase Line
GA = chr(249)       # Go ahead
SB = chr(250)       # Subnegotiation of the indicated option follows.
WILL = chr(251)     # Indicates the desire to begin performing, or confirmation that you are now performing, the indicated option.
WONT = chr(252)     # Indicates the refusal to perform, or continue performing, the indicated option.
DO = chr(253)       # Indicates the request that the other party perform, or confirmation that you are expecting the other party to perform, the indicated option.
DONT = chr(254)     # Indicates the demand that the other party stop performing, or confirmation that you are no longer expecting the other party to perform, the indicated option.
IAC = chr(255)      # Interpret as a command


# Adapted from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None
        self.file = open("output.txt", "w")
        self.file.truncate()
        self.file.close()
        self.color_newline = re.compile('^' + ESC + '\[[0-9;]*[m]' + NL)

    # Client => Proxy
    def dataReceived(self, data):
        self.file = open("output.txt", "a")
        output = []
        print("----------Processing Data From Achaea----------------")
        if data[0] == NL:
            data = data[1:]

        # Fix color-only leading line
        color_newline = self.color_newline.match(data)
        if color_newline:
            color = data[0:color_newline.end() - 1]
            data = color + data[color_newline.end():]

        for b in data:
            if b == IAC:
                print('escaped')
            elif b == '\r':
                print('newline')
            elif b == SB:
                print('subnegotiation')
            elif b in (GA, EORD, NOP, DM, BRK, IP, AO, AYT, EC, EL):
                print("idk yet")
            elif b in (WILL, WONT, DO, DONT):
                print("Not Sure")
            elif b == '\0':
                print("\0 ???")
            elif b == SE:
                print("SE")
            else:
                output.append(b)

        print("".join(output))
        self.file.write(data)
        print("--------------------------------------------------------")
        if re.search('(\w+) sit yourself down\.', data):
            print("Got it")
            self.transport.write("stand\n")
        self.file.close()



def main():
    print("Starting Icarus Regex Server on port " + str(LISTEN_PORT) + "...")
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    # Starting Server for twisted-proxy to connect to
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()