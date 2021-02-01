import socket
import time

from metrics_structure import Metrics


class ClientError(Exception):
    """Client exception class."""
    pass


class Client:
    """
    The class that encapsulates the connection to the server,
    the client socket, and methods for receiving and sending metrics to the server.
    """
    def __init__(self, host, port, timeout=None):
        self._sock = self.create_connect(host, port, timeout)

    def _read(self) -> list:
        """Read data from socket."""
        try:
            data = self._sock.recv(1024)
        except socket.error as err:
            raise ClientError('Error reading data from socket', err)
        return data.decode('utf-8').split('\n')

    def _send(self, data):
        """Send data to socket."""
        try:
            self._sock.send(data.encode('utf-8'))
        except socket.error as err:
            raise ClientError('Error sending data to server', err)

    def get(self, metrics_name: str) -> dict:
        """
        The method makes a request to the server, receives data and displays it to the user.
        The method returns a dictionary with metrics in case of a successful response from the server
        and throws a ClientError exception if it is not successful.
        :param metrics_name: name of the requested metric or '*' if all metrics are requested; type: str;
        :return: type: dict.
        """
        formatted_request = f'get {metrics_name}\n'
        self._send(formatted_request)

        response = self._read()
        metrics_list = self.parse_response(response)

        if not self.response_is_valid(response) or not self.metrics_is_valid(metrics_list):
            raise ClientError('Server returns invalid data')

        return self._response_display(metrics_name, metrics_list)

    def put(self, metrics_name: str, value: float, timestamp: int = None):
        """
        The method sends data to the server.  The method returns nothing on successful submission
        and throws a custom ClientError exception if not successful.
        :param metrics_name: the name of the stored metric; type:str;
        :param value: the value of the stored metric; type:float;
        :param timestamp: optional named parameter; type:int.
        """
        if timestamp is None:
            timestamp = int(time.time())

        formatted_request = f'put {metrics_name} {value} {timestamp}\n'
        self._send(formatted_request)

        response = self._read()
        if not self.response_is_valid(response):
            raise ClientError('Server returns invalid data')

    def _response_display(self, input_metrics_name, metrics_list) -> dict:
        """The function displays the formatted data."""
        result = {}

        if input_metrics_name == '*':
            for metrics in metrics_list:
                if metrics.name not in result:
                    result[metrics.name] = [(int(metrics.timestamp), float(metrics.value))]
                else:
                    result[metrics.name].append((int(metrics.timestamp), float(metrics.value)))

        else:
            result = {input_metrics_name: []}
            for metrics in metrics_list:
                if metrics.name == input_metrics_name:
                    result[input_metrics_name].append((int(metrics.timestamp), float(metrics.value)))

            if not result[input_metrics_name]:
                result = {}

        return self.sort_by_timestamp(result)

    @staticmethod
    def create_connect(host: str, port: int, timeout: int) -> socket:
        """The function creates a connection and throws a custom ClientError exception on error."""
        try:
            sock = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError('Cannot create connection!', err)
        return sock

    @staticmethod
    def parse_response(input_data: list) -> list:
        """The function parses the response into a list of metrics."""
        input_data = input_data[1:-2]
        return list(Metrics(*data.split()) for data in input_data)

    @staticmethod
    def response_is_valid(data):
        """The function checks the response status."""
        if data == ['ok', '', '']:
            return True
        return True if data[0] == 'ok' else False

    @staticmethod
    def metrics_is_valid(input_metrics: list) -> bool:
        """The function checks the correctness of metrics."""
        for metrics in input_metrics:
            if not metrics.name or not metrics.value or not metrics.timestamp:
                return False
            try:
                float(metrics.value)
                int(metrics.timestamp)
            except ValueError:
                return False
        return True

    @staticmethod
    def sort_by_timestamp(input_data: dict) -> dict:
        """The function sorts data by timestamp."""
        for k, v in input_data.items():
            v.sort(key=lambda i: i[0])
        return input_data


if __name__ == '__main__':
    client = Client('127.0.0.1', 8888, 15)
    # print(client.get('palm.cpu'))
    # client.put("palm.cpu", 2.0, timestamp=1150864248)
    # client.put("palm.cpu", 0.5, timestamp=15086424)
    # client.put("palm.cpu", 1.5, timestamp=1250864248)
    client.put("memory")
    # print(client.get('palm.cpu'))
    # print(client.get('*'))




