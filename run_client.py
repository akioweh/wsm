import sys

from src.client import Client

if __name__ == '__main__':
    try:
        uri = sys.argv[1]
    except IndexError:
        uri = 'ws://localhost:6969'
    client = Client(uri)
    client.run()
