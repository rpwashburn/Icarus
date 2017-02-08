from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from AchaeaProtocol import AchaeaProtocol


def main():
    print("Starting Icarus Server on port 8900 ...")
    factory = Factory()
    factory.protocol = AchaeaProtocol

    from twisted.internet import reactor
    endpoint = TCP4ServerEndpoint(reactor, 8900)
    endpoint.listen(factory)
    reactor.run()

if __name__ == '__main__':
    main()

