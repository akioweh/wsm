import sys

from src.server import Server

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 6969
    server = Server(port)
    server.run()
