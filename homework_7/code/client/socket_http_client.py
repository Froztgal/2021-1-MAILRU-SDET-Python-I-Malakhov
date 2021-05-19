import socket
import settings


class SocketClientHTTP:

    def __init__(self):
        self.host = settings.App.HOST
        self.port = int(settings.App.PORT)
        self.client = None

    def run_client(self):
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
        request = f'GET {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.client.send(request.encode())
        return self.data_receive()

    def mock_post(self, params, jdata):
        request = f'POST {params} HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: application/json\r\nContent-Length: {len(jdata)}\r\n\r\n{jdata}'
        self.client.send(request.encode())
        return self.data_receive()
