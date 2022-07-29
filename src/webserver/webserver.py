import os
import urllib.request
import http.server
import socketserver


def run(websocket_ip: str = None, websocket_port: int = 6969, webserver_port: int = 8080):
    if websocket_ip is None:
        websocket_ip = urllib.request.urlopen('https://api.ipify.org/').read().decode('utf8')

    with open(f'{os.path.dirname(__file__)}/index.html', 'r') as f:
        template_html = f.read().replace("'ws://localhost:6969'", f"'ws://{websocket_ip}:{websocket_port}'")

    class Handler(http.server.BaseHTTPRequestHandler):
        # noinspection PyPep8Naming
        def do_GET(self):
            if self.path != '/':
                self.send_response(404)
                self.end_headers()
                return
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(template_html.encode('utf-8'))

    with socketserver.TCPServer(('', webserver_port), Handler) as server:
        print('Webserver serving at port', webserver_port)
        server.serve_forever()


if __name__ == '__main__':
    run()
