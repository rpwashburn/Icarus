#!/usr/bin/env python

LISTEN_PORT = 8900
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"
SERVER_PORT = 23
SERVER_ADDR = "www.achaea.com"

from twisted.internet import protocol, reactor


class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None
        self.icarus_client = None

    def make_icarus_connection(self, factory):
        try:
            print("Attempting Connection to Icarus Server")
            reactor.connectTCP("localhost", 8902, factory, 1)
        except Exception as e:
            print "Caught exception " + str(e)
            print("Icarus Server Not Running")

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self

        icarus_factory = IcarusFactory()
        icarus_factory.protocol = IcarusClientProtocol
        icarus_factory.server = self
        self.make_icarus_connection(icarus_factory)

        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)

    def dataReceived(self, data):
        if self.client:
            print("------------MUDLET TO PROXY----------------")
            print(data)
            print("-------------------------------------------")
            self.client.write(data)
        else:
            self.buffer = data

    def write(self, data):
        print("------------PROXY to MUDLET----------------")
        print(data)
        print("-------------------------------------------")
        self.transport.write(data)


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    def dataReceived(self, data):
        print("------------ACHAEA TO PROXY----------------")
        print(data)
        print("--------------------------------------------")
        self.factory.server.write(data)

        if self.factory.server.icarus_client:
            self.factory.server.icarus_client.write(data)

    def write(self, data):
        if data:
            print("------------PROXY TO ACHAEA----------------")
            print(data)
            print("--------------------------------------------")
            self.transport.write(data)

    def connectionLost(self, reason):
        print("Connection to Achaea Lost")
        reactor.stop()


class IcarusFactory(protocol.ClientFactory):

    def clientConnectionFailed(self, connector, reason):
        self.server.icarus_client = None
        connector.connect()

    def clientConnectionLost(self, connector, reason):
        self.server.icarus_client = None
        connector.connect()


class IcarusClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.icarus_client = self

    def dataReceived(self, data):
        print("------------Icarus to Proxy----------------")
        print(data)
        print("--------------------------------------------")
        try:
            self.factory.server.client.write(data)
        except Exception as e:
            print e

    def write(self, data):
        if data:
            print("------------Achaea to Icarus----------------")
            print(data)
            print("--------------------------------------------")
            self.transport.write(data)

    def connectionLost(self, reason):
        print("Connection to Icarus Lost")


def main():
    print("Starting Icarus Proxy Server on port " + str(LISTEN_PORT) + "...")
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    # Starting Server for Mudlet to connect to
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
