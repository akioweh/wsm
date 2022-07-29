from websockets import WebSocketServerProtocol


class Client:
    """client model class providing data storage and methods for socket communication"""
    def __init__(self, ws: WebSocketServerProtocol, name: str = 'Unknown'):
        self.ws: WebSocketServerProtocol = ws
        self.display_name: str = name

    @property
    def name(self):
        return self.ws.remote_address

    async def send(self, data) -> None:
        await self.ws.send(data)

    def __getattr__(self, item):
        return getattr(self.ws, item)
