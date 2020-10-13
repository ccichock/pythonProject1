import concurrent.futures
import tcp_socket as socket
import threading
import json


class Client:

    def __init__(self, ip_addres, port):
        self.continue_receive = True
        self.sender_nickname = "Client"
        self.lock = threading.Lock()
        self.received_messages = []
        self.tcp_client = socket.create_client_connection(ip_addres, port)
        socket.send_nickname(self.tcp_client, self.sender_nickname)
        self.receiver_nickname = socket.receive_nickname(self.tcp_client)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        print("client socket closed")
        self.tcp_client.close()


    def send(self):
        while True:
            lines = input()
            if lines == "q":
                with self.lock:
                    self.continue_receive = False
                print("stop sending")
                return;
            self.tcp_client.send(lines.encode())


    def receive(self):
        buffer_size = 1024

        while self.continue_receive:
            try:
                data = self.tcp_client.recv(buffer_size)
                if not data:
                    continue
                self.update_json_messages(data.decode())
            except:
                pass


    def update_json_messages(self, message):
        with self.lock:
            self.received_messages.append(message)

        with open(f'{self.sender_nickname}_messages.json', 'w') as json_file:
            json_file.seek(0)
            json_file.truncate()
            json.dump(self.received_messages, json_file)


    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.receive)
            executor.submit(self.send)


with Client(ip_addres='192.168.1.26', port=8080) as client:
    client.run()
