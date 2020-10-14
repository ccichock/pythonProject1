import concurrent.futures
import tcp_socket as socket
import threading
import json
from connection import Connection, ConnectionType

class Server(Connection):

    def __init__(self, ip_addres, port):
        super().__init__(ip_addres, port, ConnectionType.Server)
        self.sender_nickname = "Server"
        self.messages_lock = threading.Lock()
        self.received_messages = []
        self.receiver_nickname = socket.receive_nickname(self.socket)
        socket.send_nickname(self.socket, self.sender_nickname)


    def update_json_messages(self, decoded_message):
        with self.messages_lock:
            self.received_messages.append(decoded_message)

        with open(f'{self.sender_nickname}_messages.json', 'w') as json_file:
            json_file.seek(0)
            json_file.truncate()
            json.dump(self.received_messages, json_file)


    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(super().send)
            executor.submit(super().receive, self.update_json_messages)


with Server(ip_addres='', port=8080) as server:
    server.run()
