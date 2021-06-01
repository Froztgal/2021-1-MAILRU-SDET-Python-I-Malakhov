import json
import requests
import settings
from faker import Faker
from client.socket_http_client import SocketClientHTTP
from mock.flask_mock import SURNAME_DATA


fake = Faker()
s_client = SocketClientHTTP()
url = f'http://{settings.Mock.HOST}:{settings.Mock.PORT}'


def test_by_socket_get():
    name, surname = [fake.first_name(), fake.last_name()]
    SURNAME_DATA[name] = surname
    res = s_client.mock_request(f'/get_surname/{name}')
    assert json.loads(res[-1])['surname'] == surname


def test_by_socket_put():
    name, surname, new_surname = [fake.first_name(), fake.last_name(), fake.last_name()]
    SURNAME_DATA[name] = surname
    res = s_client.mock_request(f'/get_surname/{name}')
    assert json.loads(res[-1])['surname'] == surname
    s_client.mock_request(f'/put_surname/{name}', jdata={'surname': new_surname}, method='PUT')
    res = s_client.mock_request(f'/get_surname/{name}')
    assert json.loads(res[-1])['surname'] == new_surname


def test_by_socket_del():
    name, surname = [fake.first_name(), fake.last_name()]
    SURNAME_DATA[name] = surname
    res = s_client.mock_request(f'/get_surname/{name}')
    assert json.loads(res[-1])['surname'] == surname
    s_client.mock_request(f'/delete_surname/{name}', method='DELETE')
    res = s_client.mock_request(f'/get_surname/{name}')
    assert json.loads(res[-1]) == f"Surname for user {name} not fount"
