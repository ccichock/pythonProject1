import concurrent.futures
import tcp_socket as socket

class Server:

    def __init__(self, ip_addres, port):
        self.sender_nickname = "Server"
        self.tcp_server = socket.create_server_connection(ip_addres, port)
        self.receiver_nickname = socket.receive_nickname(self.tcp_server)
        socket.send_nickname(self.tcp_server, self.sender_nickname)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        print("server socket closed")
        self.tcp_server.close()


    def sendReceive(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(socket.send_to, self.tcp_server)
            executor.submit(socket.receive_from, self.tcp_server, self.receiver_nickname)


with Server(ip_addres='', port=8080) as server:
    server.sendReceive()