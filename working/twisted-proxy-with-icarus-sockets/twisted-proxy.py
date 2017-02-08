#!/usr/bin/env python

LISTEN_PORT = 8900
SERVER_PORT = 23
SERVER_ADDR = "www.achaea.com"

import socket
from twisted.internet import protocol, reactor


# Adapted from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.mudletClient = None
        self.icarusSocket = None

    def make_icarus_connection(self):
        try:
            print("Attempting Connection to Icarus Server")
            self.icarusSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.icarusSocket.connect(("localhost", 8902))
        except socket.error, exc:
            print "Caught exception socket.error : %s" % exc
            print("Icarus Server Not Running")

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self
        self.make_icarus_connection()
        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)

    # Client => Proxy
    def dataReceived(self, data):
        if self.mudletClient:
            print("------------MUDLET TO PROXY----------------")
            print(data)
            print("-------------------------------------------")
            self.mudletClient.write(data)
        else:
            self.buffer = data

    # Proxy => Client
    def write(self, data):
        print("------------PROXY to MUDLET----------------")
        print(data)
        print("-------------------------------------------")
        self.transport.write(data)


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.mudletClient = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    # Achaea => Proxy
    def dataReceived(self, data):
        print("------------ACHAEA TO PROXY----------------")
        print(data)
        print("--------------------------------------------")
        self.factory.server.write(data)
        try:
            self.factory.server.icarusSocket.send(data)
        except socket.error, exc:
            print("Icarus Server Not Running")
            self.factory.server.make_icarus_connection()

    # Proxy => Achaea
    def write(self, data):
        if data:
            print("------------PROXY TO ACHAEA----------------")
            print(data)
            print("--------------------------------------------")
            self.transport.write(data)

    def connectionLost(self, reason):
        print("Connection to Achaea Lost")
        reactor.stop()


def main():
    print("Starting Icarus Server on port " + str(LISTEN_PORT) + "...")
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    # Starting Server for Mudlet to connect to
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()