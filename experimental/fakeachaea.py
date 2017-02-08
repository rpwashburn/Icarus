# This is the blocking version of the Slow Poetry Server.

import optparse, os, socket, time


def mimic_game(sock):
    while True:
        try:
            # data = sock.recv(1024)
            # if data:
            #     print("data received: " + str(data))
            sock.send("This is a game message\n") # this is a blocking call
        except socket.error:
            sock.close()
            return

        time.sleep(5)


def serve(listen_socket):
    while True:
        sock, addr = listen_socket.accept()

        print 'Somebody at %s wants poetry!' % (addr,)

        mimic_game(sock)


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8901))

    sock.listen(5)

    print 'Serving %s.' % (sock.getsockname()[1])

    serve(sock)


if __name__ == '__main__':
    main()
