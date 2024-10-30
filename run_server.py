import argparse
import ssl

from src.server import Server

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat Server')
    parser.add_argument('-p', '--port', type=int, help='Port to run server on')
    parser.add_argument('--certfile', type=str, help='SSL certificate file')
    parser.add_argument('--keyfile', type=str, help='SSL key file')
    args = parser.parse_args()
    if (args.keyfile or args.certfile) and not (args.keyfile and args.certfile):
        parser.error('Both --keyfile and --certfile must be provided if either is provided')

    ssl_context = None
    if args.certfile:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(args.certfile, args.keyfile)

    server = Server(args.port, ssl_context)
    server.run()
