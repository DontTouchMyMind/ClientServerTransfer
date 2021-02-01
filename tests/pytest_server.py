
HOST, PORT = '127.0.0.1', 8888


def pytest_server_connect(socket):
    socket.connect((HOST, PORT))
    assert socket


def pytest_server_receive_ok(socket):
    socket.connect((HOST, PORT))

    request = 'get *\n'

    socket.send(request.encode('utf-8'))
    response = socket.recv(1024).decode('utf-8')
    assert response == 'ok\n\n'


def pytest_server_receive_error(socket):
    socket.connect((HOST, PORT))

    request = 'wrong_request\n'

    socket.send(request.encode('utf-8'))
    response = socket.recv(1024).decode('utf-8')
    assert response == 'error\nwrong command\n\n'


def pytest_server_send_put(socket):
    socket.connect((HOST, PORT))

    request = 'put palm.cpu 23.7 1150864247\n'

    socket.send(request.encode('utf-8'))
    response = socket.recv(1024).decode('utf-8')
    assert response == 'ok\n\n'


def pytest_server_send_get(socket):
    socket.connect((HOST, PORT))

    request = 'get palm.cpu\n'

    socket.send(request.encode('utf-8'))
    response = socket.recv(1024).decode('utf-8')
    assert response == 'ok\npalm.cpu 23.7 1150864247\n\n'


def pytest_server_send_put_other_metrics(socket):
    socket.connect((HOST, PORT))

    request = 'put temperature 39.2 1420864248\n'
    socket.send(request.encode('utf-8'))

    response = socket.recv(1024).decode('utf-8')
    assert response == 'ok\n\n'


def pytest_server_send_get_all_metrics(socket):
    socket.connect((HOST, PORT))

    request = 'get *\n'

    socket.send(request.encode('utf-8'))
    response = socket.recv(1024).decode('utf-8')

    assert response == 'ok\npalm.cpu 23.7 1150864247\ntemperature 39.2 1420864248\n\n'


