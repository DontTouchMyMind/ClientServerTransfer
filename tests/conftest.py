import multiprocessing
import socket as s
from time import sleep
import pytest

from server import run_server


host, port = '127.0.0.1', 8888


def server():
    run_server(host, port)


@pytest.fixture(autouse=True, scope='module')
def start_server():
    p = multiprocessing.Process(target=server)
    p.start()
    sleep(3)
    yield
    p.terminate()


@pytest.fixture
def socket(request):
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def socket_teardown():
        _socket.close()

    request.addfinalizer(socket_teardown)
    return _socket

