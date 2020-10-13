import concurrent.futures
import tcp_socket as socket
import threading
import json


class Server:

    def __init__(self, ip_addres, port):
        self.continue_receive = True
        self.lock = threading.Lock()
        self.sender_nickname = "Server"
        self.received_messages = []
        self.tcp_server = socket.create_server_connection(ip_addres, port)
        self.receiver_nickname = socket.receive_nickname(self.tcp_server)
        socket.send_nickname(self.tcp_server, self.sender_nickname)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        print("server socket closed")
        self.tcp_server.close()


    def send(self):
        while True:
            lines = input()
            if lines == "q":
                with self.lock:
                    self.continue_receive = False
                print("stop sending")
                return;
            self.tcp_server.send(lines.encode())


    def receive(self):
        buffer_size = 1024

        while self.continue_receive:
            data = self.tcp_server.recv(buffer_size)
            if not data:
                continue
            self.update_json_messages(data.decode())


    def update_json_messages(self, message):
        with self.lock:
            self.received_messages.append(message)

        with open(f'{self.sender_nickname}_messages.json', 'w') as json_file:
            json_file.seek(0)
            json_file.truncate()
            json.dump(self.received_messages, json_file)


    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send)
            executor.submit(self.receive)


with Server(ip_addres='', port=8080) as server:
    server.run()
