import sys
from src.webserver import run

if __name__ == '__main__':
    try:
        websocket_ip = sys.argv[1]
        websocket_port = int(sys.argv[2])
        webserver_port = int(sys.argv[3])
        if websocket_ip == 'this':
            websocket_ip = None
    except (IndexError, ValueError):
        websocket_ip = None
        websocket_port = 6969
        webserver_port = 8080
    run(websocket_ip, websocket_port, webserver_port)
