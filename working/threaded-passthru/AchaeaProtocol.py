import socket
import time
import threading
import sys
import re
# import chardet
from twisted.internet.protocol import Protocol

achaea_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
achaea_connection.connect(("www.achaea.com", 23))


class AchaeaProtocol(Protocol):

    def __init__(self):
        threading.Thread(target=self.send_to_mudlet).start()

    def send_to_mudlet(self):
        while True:
            try:
                data = achaea_connection.recv(1024)
                if not data:
                    sys.exit()
                while not self.transport:
                    time.sleep(0.01)

                print("----------------")
                # encoding = chardet.detect(data)['encoding']
                print(data)
                print("----------------")

                if re.search(r'(.*)yourself down(.*)', data):
                    print("matched")
                    achaea_connection.send("stand")
                self.transport.write(data)
            except Exception as e:
                print e

    def dataReceived(self, data):
        try:
            if achaea_connection:
                achaea_connection.send("{0}".format(data))
            else:
                sys.exit()
        except Exception as e:
            print e
            sys.exit()