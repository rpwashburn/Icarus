#!/usr/bin/env python

LISTEN_PORT = 8902
# SERVER_PORT = 8901
# SERVER_ADDR = "localhost"

from twisted.internet import protocol, reactor


# Adapted from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None
        self.counter = 1

    # Client => Proxy
    def dataReceived(self, data):
        print("----------Processing Data From Achaea----------------")
        print(data)
        print("--------------------------------------------------------")
        if (self.counter % 10) == 0:
            self.transport.write("qsc\n")
        self.counter += 1


def main():
    print("Starting Icarus Regex Server on port " + str(LISTEN_PORT) + "...")
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    # Starting Server for twisted-proxy to connect to
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()