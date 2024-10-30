import argparse
import ssl
import sys

from src.server import Server

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat Server')
    parser.add_argument('-p', '--port', type=int, help='Port to run server on')
    parser.add_argument('--certfile', type=str, help='SSL certificate file')
    args = parser.parse_args()

    ssl_context = None
    if args.certfile:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(args.certfile)

    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 6969
    server = Server(port, ssl_context)
    server.run()
