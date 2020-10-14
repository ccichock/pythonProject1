import socket
import time

def create_server_connection(ip_addres, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(5)
    server.bind((ip_addres, port))
    server.listen(1)
    connection, addres = server.accept()
    print(f'connected with {addres}')
    return connection


def create_client_connection(ip_addres, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    client.connect((ip_addres, port))
    client.setblocking(False)
    return client


def send_nickname(connection, nickname):
    connection.send(nickname.encode())


def receive_nickname(connection):
    buffer_size = 1024
    try:
        nickname = connection.recv(buffer_size)
        return nickname.decode()
    except:
        receive_nickname(connection)
