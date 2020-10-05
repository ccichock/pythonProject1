import concurrent.futures
import tcp_socket as socket

class Client:

    def __init__(self, ip_addres, port):
        self.sender_nickname = "Client"
        self.tcp_client = socket.create_client_connection(ip_addres, port)
        socket.send_nickname(self.tcp_client, self.sender_nickname)
        self.receiver_nickname = socket.receive_nickname(self.tcp_client)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        print("client socket closed")
        self.tcp_client.close()


    def sendReceive(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(socket.receive_from, self.tcp_client, self.receiver_nickname)
            executor.submit(socket.send_to, self.tcp_client)


with Client(ip_addres='192.168.1.26', port=8080) as client:
    client.sendReceive()
