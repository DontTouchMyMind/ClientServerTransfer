import socket

from client import Client

server_name = 'server'
HOST, PORT = '127.0.0.1', 8888


def pytest_server():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.sendall('hello\n'.encode('utf8'))
    c = sock.recv(1024).decode('utf-8')
    assert c == 'error\nwrong command\n\n'


def pytest_client_put_one_parameters():
    client = Client(HOST, PORT, timeout=15)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    response = client.get('palm.cpu')
    assert response == {'palm.cpu': [(1150864248, 2.0)]}


def pytest_client_get_one_parameters():
    client = Client(HOST, PORT, timeout=15)
    response = client.get('palm.cpu')
    assert response == {'palm.cpu': [(1150864248, 2.0)]}


def pytest_client_put_few_parameters():
    client = Client(HOST, PORT, timeout=15)
    client.put("palm.cpu", 2.2, timestamp=1150864249)
    client.put("palm.cpu", 5.2, timestamp=1150864249)
    client.put("memory", 43.8, timestamp=1550774249)
    response = client.get('*')
    assert response == {
        'palm.cpu': [(1150864248, 2.0), (1150864249, 5.2)],
        'memory': [(1550774249, 43.8)]
    }


def pytest_several_users():
    client1 = Client(HOST, PORT, timeout=15)
    client2 = Client(HOST, PORT, timeout=15)
    client1.put("temperature", 87.3, timestamp=1614514249)
    response = client2.get('temperature')
    assert response == {'temperature': [(1614514249, 87.3)]}




