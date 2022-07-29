import asyncio

from src.server import Server

if __name__ == '__main__':
    client = Server()
    asyncio.run(client.run())
