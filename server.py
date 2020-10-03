import concurrent.futures
import tcp_socket as socket
from contextlib import contextmanager

@contextmanager
def tcp_socket(ip_addres, port):
    try:
        server = socket.createServerConnection(ip_addres, port)
        yield server
    finally:
        server.close()


receiver_nickname = "Client"
with tcp_socket(ip_addres='', port=8080) as tcp_server:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(socket.sendTo, tcp_server)
        executor.submit(socket.receiveFrom, tcp_server, receiver_nickname)

print("client disconnected")