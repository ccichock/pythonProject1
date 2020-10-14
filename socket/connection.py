import tcp_socket as socket
import threading
from enum import Enum

class ConnectionType(Enum):
    Server = 0
    Client = 1


class Connection:

    def __init__(self, ip_addres, port, connectionType):
        if connectionType == ConnectionType.Server:
            self.socket = socket.create_server_connection(ip_addres, port)
        elif connectionType == ConnectionType.Client:
            self.socket = socket.create_client_connection(ip_addres, port)
        self.continue_receive = True
        self.lock = threading.Lock()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        print("server socket closed")
        self.socket.close()


    def send(self):
        while True:
            lines = input()
            if lines == "q":
                with self.lock:
                    self.continue_receive = False
                print("stop sending")
                return;
            self.socket.send(lines.encode())


    def receive(self, on_receive_action):
        buffer_size = 1024

        while self.continue_receive:
            try:
                data = self.socket.recv(buffer_size)
                if not data:
                    continue
                on_receive_action(data.decode())
            except:
                pass