from Socket import Socket
import asyncio


class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()
        self.users = []

    async def send_data(self, data):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, socket_user):
        if not socket_user:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(socket_user, 2048)
                await self.send_data(data)
            except ConnectionResetError:
                print(f"Client <{socket_user}> removed")
                self.users.remove(socket_user)
                return
            except KeyboardInterrupt:
                print(f"Client <{socket_user}> removed")
                self.users.remove(socket_user)
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"User <{address[0]}> connected!")
            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    def set_up(self):
        self.socket.bind(('127.0.0.1', 8012))
        self.socket.listen()
        self.socket.setblocking(False)
        print("Server listen")

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()
