import socket
import time

def create_server_connection(ip_addres, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_addres, port))
    server.listen(1)
    connection, addres = server.accept()
    print(f'connected with {addres}')
    return connection


def create_client_connection(ip_addres, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_addres, port))
    return client


def send_nickname(connection, nickname):
    connection.send(nickname.encode())


def receive_nickname(connection):
    buffer_size = 1024
    nickname = connection.recv(buffer_size)
    return nickname.decode()


def send_to(connection):
    while True:
        lines = input()
        if lines == "q":
            print("stop sending")
            return;
        connection.send(lines.encode())


def is_timeout_reached(start, timeout):
    if time.time() - start > timeout:
        print("timeout reached")
        return True


def receive_from(connection, receiver_nickname):
    start = time.time()
    buffer_size = 1024

    while not is_timeout_reached(start, 10):
        data = connection.recv(buffer_size)
        print(f'{receiver_nickname}: {data}')
