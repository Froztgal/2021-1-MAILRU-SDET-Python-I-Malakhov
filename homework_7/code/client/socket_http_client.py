import json
import socket
import settings


class SocketClientHTTP:

    def __init__(self):
        self.host = settings.Mock.HOST
        self.port = int(settings.Mock.PORT)
        self.client = None
        self._avalible_methods = {'GET': False, 'DELETE': False, 'POST': True,'PUT': True}

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

    def mock_request(self, params, jdata=None, method='GET'):
        self.connect()
        if method.upper() not in self._avalible_methods:
            method = 'GET'
        if self._avalible_methods[method.upper()]:
            jstr = json.dumps(jdata)
            request = f'{method} {params} HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: application/json\r\nContent-Length: {len(jstr)}\r\n\r\n{jstr}'
        else:
            request = f'{method} {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.client.send(request.encode())
        return self.data_receive()
