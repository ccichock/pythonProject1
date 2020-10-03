import socket
import time

def createServerConnection(ip_addres, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_addres, port))
    server.listen(1)
    connection, addres = server.accept()
    print(f'connected with {addres}')
    return connection


def createClientConnection(ip_addres, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_addres, port))
    return client


def sendTo(connection):
    while True:
        lines = input()
        if lines == "q":
            print("stop sending")
            return;
        connection.send(lines.encode())


def isTimeoutReached(start, timeout):
    if time.time() - start > timeout:
        print("timeout reached")
        return True


def receiveFrom(connection, receiver_nickname):
    start = time.time()
    buffer_size = 1024

    while not isTimeoutReached(start, 10):
        data = connection.recv(buffer_size)
        print(f'{receiver_nickname}: {data}')
