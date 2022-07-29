import asyncio

import websockets

from .client_model import Client


class Server:
    def __init__(self, interface: str = '', port: int = 6969):
        self.addr = (interface, port)
        self.clients: list[Client] = []

    async def broadcast(self, msg):
        await asyncio.gather(*(client.send(msg) for client in self.clients))

    async def handle(self, ws):
        client = Client(ws)
        self.clients.append(client)

        async for data in ws:
            op, msg = data[:3], data[3:]

            if op == 'MSG':  # Message
                await client.send('ACK')
                await self.broadcast(f'MSG{client.display_name}: {msg}')
            elif op == 'SDN':  # Set Display Name
                print(f'Client [{client.name}] changed name from [{client.display_name}] to [{msg}]')
                client.display_name = msg
                await client.send('ACK')
            else:  # Unknown opcode
                print(f'Unknown opcode [{op}] from client [{client.name}]')
                await client.send(f'INV{op}-{msg}')

    async def run(self):
        async with websockets.serve(self.handle, self.addr[0], self.addr[1]):
            await asyncio.Future()  # run forever
