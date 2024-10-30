from websockets import WebSocketServerProtocol


class Client:
    """client model class providing data storage and methods for socket communication"""
    def __init__(self, ws: WebSocketServerProtocol, name: str = 'Unknown'):
        self.ws: WebSocketServerProtocol = ws
        self.display_name: str = name
        self.address: tuple[str, int] = self.ws.remote_address

    @property
    def name(self) -> str:
        if self.address is None and isinstance(addr := self.ws.remote_address, tuple):
            self.address = addr
        return f'{self.address[0]}:{self.address[1]}' if self.address else 'Unknown'

    def __getattr__(self, item):
        return getattr(self.ws, item)
