import asyncio
import time
import threading

import websockets
from websockets import InvalidURI, InvalidHandshake, ConnectionClosedError


class Client:
    """main client class"""
    def __init__(self, uri: str = 'ws://localhost:6969'):
        self.addr = uri
        self.input_queue: list[str] = []
        self.ws = None

    async def connect(self) -> bool:
        """connects to server at self.addr \n
        returns True if successful, False otherwise"""
        try:
            print(f'Connecting to {self.addr}')
            self.ws: websockets.WebSocketClientProtocol = await websockets.connect(self.addr)
        except InvalidURI:
            print(f'Invalid address: {self.addr}')
        except (InvalidHandshake, TimeoutError, ConnectionRefusedError):
            print(f'Connection failed: {self.addr}')
        else:
            print(f'Connected to server: {self.addr}')
            return True
        return False

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
        try:
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
        except UnicodeDecodeError:  # a \xff gets sent to stdin for whatever reason when terminating
            pass

    async def run_async(self):
        """connects to the server, sets up input thread,
        and readily receives and sends messages"""
        if not await self.connect():  # connection failed if False
            return

        input_thread = threading.Thread(target=self.input_loop)
        input_thread.daemon = True
        input_thread.start()

        try:
            await asyncio.gather(self.handle_in(), self.handle_out())  # run both loops concurrently
            print('how did it finish')
        except ConnectionClosedError:
            print('Disconnected from server')

        await self.ws.close()

    def run(self):
        """runs the client"""
        try:
            asyncio.get_event_loop().run_until_complete(self.run_async())
        except (KeyboardInterrupt, EOFError):
            print('Received stopping signal')
        asyncio.get_event_loop().run_until_complete(self.ws.close())
        print('Client closed')
