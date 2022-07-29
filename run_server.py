import sys

from src.server import Server

if __name__ == '__main__':
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        host = 'all'
        port = 6969
    server = Server(host, port)
    server.run()
