import os
import time
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingTCPServer
from threading import Thread

websocket_uri = 'ws://localhost:6969'

with open(f'{os.path.dirname(__file__)}/index.html', 'r') as f:
    template_html = f.read().replace("'ws://localhost:6969'", f'\'{websocket_uri}\'')


class Handler(BaseHTTPRequestHandler):
    """handler that serves a static page when accessed from the root url,
    and sends 404 otherwise"""
    # noinspection PyPep8Naming
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-length', str(len(template_html)))
            self.end_headers()
            self.wfile.write(template_html.encode('utf-8'))
        else:
            self.send_error(404)


class WebServer(ThreadingTCPServer):
    """same as socketserver.ThreadingTCPServer but with a timeout"""
    def finish_request(self, request, client_address):
        request.settimeout(60)
        super().finish_request(request, client_address)
        # super().finish_request() handles any TimeoutError's


def run(websocket_ip: str = None, websocket_port: int = 6969, webserver_port: int = 8080):
    global websocket_uri
    print('Starting Web Server')

    if websocket_ip is None:
        websocket_ip = urlopen('https://api.ipify.org/').read().decode('utf8')
    websocket_uri = f'ws://{websocket_ip}:{websocket_port}'

    server = WebServer(('', webserver_port), Handler)
    server_thread = Thread(target=server.serve_forever)
    server_thread.start()
    print(f'Web Server running at port {webserver_port} \n'
          f'HTML pointing to websocket at {websocket_uri}')
    try:
        while 1:
            time.sleep(60)  # wait indefinitely
    except (KeyboardInterrupt, EOFError):
        print('Received stopping signal')
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(10)

    print('Web Server closed')


if __name__ == '__main__':
    run()
