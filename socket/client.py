import concurrent.futures
import tcp_socket as socket
import threading
import json
from connection import Connection, ConnectionType

class Client(Connection):

    def __init__(self, ip_addres, port):
        super().__init__(ip_addres, port, ConnectionType.Client)
        self.sender_nickname = "Client"
        self.messages_lock = threading.Lock()
        self.received_messages = []
        socket.send_nickname(self.socket, self.sender_nickname)
        self.receiver_nickname = socket.receive_nickname(self.socket)


    def update_json_messages(self, decoded_message):
        with self.messages_lock:
            self.received_messages.append(decoded_message)

        with open(f'{self.sender_nickname}_messages.json', 'w') as json_file:
            json_file.seek(0)
            json_file.truncate()
            json.dump(self.received_messages, json_file)


    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(super().receive, self.update_json_messages)
            executor.submit(super().send)


with Client(ip_addres='192.168.1.26', port=8080) as client:
    client.run()
