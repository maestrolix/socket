import socket
from abc import abstractmethod
import asyncio


class Socket:
    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.main_loop = asyncio.new_event_loop()

    @abstractmethod
    async def send_data(self, *args):
        pass

    @abstractmethod
    async def listen_socket(self, *args):
        pass

    @abstractmethod
    async def main(self):
        pass

    def start(self):
        self.main_loop.run_until_complete(self.main())

    @abstractmethod
    def set_up(self):
        pass
