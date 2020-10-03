import concurrent.futures
import tcp_socket as socket
from contextlib import contextmanager

@contextmanager
def tcp_socket(ip_addres, port):
    try:
        client = socket.createClientConnection(ip_addres, port)
        yield client
    finally:
        client.close()


receiver_nickname = "Server"
with tcp_socket(ip_addres='192.168.1.26', port=8080) as tcp_client:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(socket.receiveFrom, tcp_client, receiver_nickname)
        executor.submit(socket.sendTo, tcp_client)

print("client disconnected")
