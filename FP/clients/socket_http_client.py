import json
import socket
from mock_VK.mock_vk import MOCK_PORT, MOCK_HOST


class SocketClientHTTP:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = MOCK_PORT
        self.client = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.1)
        self.client.connect((self.host, self.port))

    def data_receive(self):

        total_data = []

        while True:
            data = self.client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                self.client.close()
                break

        data = ''.join(total_data).splitlines()

        return data

    def mock_get(self, params):
        self.connect()
        request = f'GET {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.client.send(request.encode())
        return self.data_receive()

    def mock_post(self, params, jdata):
        self.connect()
        jstr = json.dumps(jdata)
        request = f'POST {params} HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: application/json\r\nContent-Length: {len(jstr)}\r\n\r\n{jstr}'
        self.client.send(request.encode())
        return self.data_receive()
