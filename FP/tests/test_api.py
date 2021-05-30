import json
import os
import time

import data
import pytest
import allure
from tests.base import BaseCase
from ui.pages.base_page import PageNotLoadedException
import requests
from clients.socket_http_client import SocketClientHTTP
from clients.api_client import ApiClient
from clients.db_client import MysqlClient
from sql_models.models import TestUsers
from _pytest.fixtures import FixtureRequest


# Работает подключение к БД и чтение из нее!
# def test_db():
#     client = MysqlClient()
#     client.connect()
#
#     res = client.session.query(TestUsers).all()
#     print(res)
#
#     client.connection.close()
#     assert 0

# Работает
# def test_mock():
#     client = SocketClientHTTP()
#     res = client.mock_post('/vk_id_add/Actonic1', jdata={'vk_id': '123456789'})
#     print(res)
#     res = client.mock_get('/vk_id/Actonic1')
#     print(res)
#     # print(json.loads(res[-1])['vk_id'])
#     assert 0

# def test_api():
#     client = ApiClient()
#     res = client.post_login('Actonic1', 'Actonic1')
#     # res = client.post_add_user('abcdefg', 'abcdefg', 'abcdefg@zxc.com')
#     # res = client.get_app_status() # Работает
#     res = client.get_block_user('asasasasas')
#     print(res.status_code)
#     print(res.content)
#     assert 0

def add_to_table(username, password, email):
    from clients.db_client import MysqlClient
    from builders import MySQLBuilder
    client = MysqlClient()
    client.connect()
    mysql_builder = MySQLBuilder(client)
    mysql_builder.create_user(username, password, email)
    client.connection.close()


def clear_reg_table():
    from clients.db_client import MysqlClient
    client = MysqlClient()
    client.connect()
    client.execute_query('truncate test_users;', False)
    client.connection.close()

@pytest.fixture(scope='class', autouse=True)
def setup():
    clear_reg_table()
    username = 'username'
    password = 'password'
    email = 'ab@c.d'
    add_to_table(username, password, email)
    api_client = ApiClient()
    api_client.post_login(username, password)
    db_client = MysqlClient()
    db_client.connect()

@allure.feature('Тесты главной страницы.')
@pytest.mark.UI  # skip / UI
class TestAPI:

    # @allure.story('Тестирование данных сгенерированных при помощи Faker.')
    # PASS
    @pytest.mark.skip
    def test_add_user(self):
        db_client = MysqlClient()
        db_client.connect()
        api_client = ApiClient()
        api_client.post_login('username', 'password')
        api_client.post_add_user('username1', 'password1', 'a1b@c.d')
        res = db_client.session.query(TestUsers).filter_by(username='username1').first()
        assert res.username == 'username1'
        assert res.password == 'password1'
        assert res.email == 'a1b@c.d'
        assert res.access == 1
        assert res.active == 0
        assert res.start_active_time is None

    @pytest.mark.skip
    def test_del_user(self):
        self.test_add_user()
        db_client = MysqlClient()
        db_client.connect()
        api_client = ApiClient()
        api_client.post_login('username', 'password')
        api_client.get_del_user('username1')
        res = db_client.session.query(TestUsers).filter_by(username='username1').all()
        assert len(res) == 0

    @pytest.mark.skip
    def test_block_user(self):
        self.test_add_user()
        db_client = MysqlClient()
        db_client.connect()
        api_client = ApiClient()
        api_client.post_login('username', 'password')
        api_client.get_block_user('username1')
        res = db_client.session.query(TestUsers).filter_by(username='username1').first()
        assert res.access == 0

    @pytest.mark.skip
    def test_unblock_user(self):
        self.test_block_user()
        db_client = MysqlClient()
        db_client.connect()
        api_client = ApiClient()
        api_client.post_login('username', 'password')
        api_client.get_unblock_user('username1')
        res = db_client.session.query(TestUsers).filter_by(username='username1').first()
        assert res.access == 1

    @pytest.mark.skip
    def test_app_status(self):
        api_client = ApiClient()
        res = api_client.get_app_status()
        assert res.status_code == 200
        assert json.loads(res.content)['status'] == 'ok'