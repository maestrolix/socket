from Socket import Socket
import asyncio
from datetime import datetime
from os import system


class Client(Socket):

    def __init__(self):
        super(Client, self).__init__()
        self.messages = "Chat is starting\n"

    def set_up(self):
        try:
            self.socket.connect(('127.0.0.1', 8012))
        except ConnectionRefusedError:
            print('Sorry, server is offline')
            exit(0)
        self.socket.setblocking(False)

    async def listen_socket(self, *args):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            self.messages += f"{datetime.now().date()}: {data.decode('utf-8')}\n"

            system("clear")
            print(self.messages)

    async def send_data(self):
        while True:
            data = await self.main_loop.run_in_executor(None, input)
            await self.main_loop.sock_sendall(self.socket, data.encode("utf-8"))

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())
        )


if __name__ == '__main__':
    client = Client()
    client.set_up()

    client.start()
