#!/usr/bin/env python

LISTEN_PORT = 8900
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"
SERVER_PORT = 23
SERVER_ADDR = "www.achaea.com"


from twisted.internet import protocol, reactor
import icarus_globals
import telnet_values


def print_outputs(title, data):
    use_prints = True
    if use_prints:
        print("-----------" + title + "---------------------")
        print(telnet_values.sub_telnet_codes(data))
        print("---------------------------------------------")


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
            print_outputs("Mudlet to Proxy", data)
            # Mudlet to Proxy
            self.client.write(data)
        else:
            self.buffer = data

    def write(self, data):
        print_outputs("Proxy to Mudlet", data)
        # proxy to mudlet
        self.transport.write(data)


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    def dataReceived(self, data):
        print_outputs("Achaea to Proxy", data)
        # Achaea to Proxy
        self.factory.server.write(data)

        if self.factory.server.icarus_client:
            print_outputs("Proxy to Server", data)
            # Proxy to Server
            self.factory.server.icarus_client.write(data)

    def write(self, data):
        if icarus_globals.icarus_command_key not in data \
                and icarus_globals.icarus_gmcp_key not in data and icarus_globals.icarus_function_key not in data:
            print_outputs("Proxy to Achaea", data)
            # Proxy to Achaea
            self.transport.write(data)
        elif self.factory.server.icarus_client:
            print_outputs("Mudlet to Icarus", data)
            # Mudlet to Icarus
            self.factory.server.icarus_client.write(data)

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
        # Icarus to Proxy
        try:
            if icarus_globals.icarus_mudlet_key in data:
                self.factory.server.write(data)
            else:
                self.factory.server.client.write(data)
        except Exception as e:
            print e

    def write(self, data):
        if data:
            # Achaea to Icarus
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
