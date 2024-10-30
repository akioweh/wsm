import asyncio
from ssl import SSLContext

import websockets
from websockets import ConnectionClosedError
from websockets.legacy.server import WebSocketServerProtocol

from .client_model import Client


class Server:
    def __init__(self, port: int = 6969, ssl_context: SSLContext = None):
        self.port: int = port
        self.clients: list[Client] = []
        self.ws: WebSocketServerProtocol | None = None
        self.ssl_context: SSLContext = ssl_context

    async def serve(self):
        """start websocket, listens for and accepts new clients indefinitely"""
        print('Starting Chat Server')
        self.ws = await websockets.serve(self.handle, '', self.port, ssl=self.ssl_context)
        print(f'Chat Server running at port {self.port}')
        await self.ws.serve_forever()
        print('Chat Server closed')

    async def broadcast(self, msg: str | bytes):
        await asyncio.gather(*(client.ws.send(msg) for client in self.clients))

    async def handle(self, ws: WebSocketServerProtocol):
        client = Client(ws)
        print(f'[{client.name}] connected')
        self.clients.append(client)
        await self.broadcast(f'MSG[{client.name}] connected')

        try:
            async for data in ws:
                op, msg = data[:3], data[3:]

                if op == 'MSG':  # Message
                    await ws.send('ACK')
                    await self.broadcast(f'MSG{client.display_name}: {msg}')
                elif op == 'SDN':  # Set Display Name
                    print(f'[{client.name}] changed display name from [{client.display_name}] to [{msg}]')
                    client.display_name = msg
                    await ws.send('ACK')
                else:  # Unknown opcode
                    print(f'Unknown opcode [{op}] from [{client.name}] aka [{client.display_name}]')
                    await ws.send(f'INV{op}-{msg}')
        except ConnectionClosedError:
            pass
        print(f'[{client.name}] disconnected')
        self.clients.remove(client)
        await self.broadcast(f'MSG[{client.name}] aka [{client.display_name}] has disconnected')

    def run(self):
        """runs server from sync blocking call"""
        try:
            asyncio.get_event_loop().run_until_complete(self.serve())
        except (KeyboardInterrupt, EOFError):
            print('Received stopping signal')
        self.ws.close()
        print('Chat Server closed')
