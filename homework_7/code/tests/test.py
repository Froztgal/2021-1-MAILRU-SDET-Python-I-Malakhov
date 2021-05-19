import json
import requests
import settings
from client import socket_http_client
from mock.flask_mock import SURNAME_DATA


url = f'http://{settings.App.HOST}:{settings.App.PORT}'


def test_by_socket_get():
    SURNAME_DATA['Egor'] = 'Krasnogolovikov'
    requests.post(f'{url}/add_user', json={'name': 'Egor'})

    s_client = socket_http_client.SocketClientHTTP()
    s_client.run_client()
    res = s_client.mock_get('/get_user/Egor')

    assert json.loads(res[-1])['surname'] == 'Krasnogolovikov'


def test_by_socket_put():
    SURNAME_DATA['Egor'] = 'Krasnogolovikov'
    requests.get(f'{url}/put_user/Egor')

    s_client = socket_http_client.SocketClientHTTP()
    s_client.run_client()
    res = s_client.mock_get('/get_user/Egor')

    assert json.loads(res[-1])['surname'] == 'new_surname'


def test_by_socket_del():
    SURNAME_DATA['Egor'] = 'Krasnogolovikov'
    requests.get(f'{url}/del_user/Egor')

    s_client = socket_http_client.SocketClientHTTP()
    s_client.run_client()
    res = s_client.mock_get('/get_user/Egor')

    assert json.loads(res[-1])['surname'] is None
