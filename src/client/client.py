import asyncio
import time
import threading

import websockets
from websockets import InvalidURI, InvalidHandshake


class Client:
    """main client class"""
    def __init__(self, uri: str = 'ws://localhost:6969'):
        self.addr = uri
        self.input_queue: list[str] = []
        self.ws = None

    async def connect(self) -> bool:
        try:
            self.ws: websockets.WebSocketClientProtocol = await websockets.connect(self.addr)
        except InvalidURI:
            print(f'Invalid address: {self.addr}')
            return False
        except (InvalidHandshake, TimeoutError):
            print(f'Connection failed: {self.addr}')
            return False
        print(f'Connected to server: {self.addr}')
        return True

    async def handle_in(self):
        """handles incoming traffic from server
        and sends reply traffic if necessary"""
        async for data in self.ws:
            op, msg = data[:3], data[3:]

            if op == 'MSG':  # Message
                print(f'[{time.strftime("%H:%M:%S")}] {msg}')
            elif op == 'INV':  # Invalid opcode sent
                print(f'>>> Invalid command: {msg}')
            elif op == 'ACK':  # good
                pass
            else:
                print(f'Unknown opcode [{op}] from server')

    async def handle_out(self):
        """handles outgoing traffic to server"""
        while self.ws.open:
            if self.input_queue:
                msg = self.input_queue.pop(0)
                await self.ws.send(msg)
                await asyncio.sleep(0)
            else:
                await asyncio.sleep(0.25)

    def input_loop(self):
        """runs threaded \n
        takes input from stdin as user messages"""
        while True:
            data = input()
            try:
                if data and data[0] == '/':  # Command
                    if data[1] == '/':  # Message with escaped backslash
                        op = 'MSG'
                        msg = data[1:]
                    else:  # Actual command
                        op = data[1:4].upper()
                        msg = data[5:]
                        if len(data) >= 5 and data[4] != ' ':
                            raise ValueError
                else:  # Message
                    op = 'MSG'
                    msg = data

                self.input_queue.append(f'{op}{msg}')

            except ValueError:
                print('>>> Invalid command syntax')

    async def run(self):
        if not await self.connect():
            return

        input_thread = threading.Thread(target=self.input_loop)
        input_thread.daemon = True
        input_thread.start()
        t_in = asyncio.create_task(self.handle_in())
        t_out = asyncio.create_task(self.handle_out())
        await asyncio.gather(t_in, t_out)
