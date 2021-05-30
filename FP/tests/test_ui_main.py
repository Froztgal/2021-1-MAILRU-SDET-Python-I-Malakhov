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


@allure.feature('Тесты главной страницы.')
@pytest.mark.usefixtures('clear_reg_table')
@pytest.mark.UI  # skip / UI
class TestMain(BaseCase):

    @pytest.fixture(scope='class', autouse=True)
    def setup(self):
        self.username = 'username'
        self.password = 'password'
        self.email = 'ab@c.d'
        self.add_to_table()

    def add_to_table(self):
        from clients.db_client import MysqlClient
        from builders import MySQLBuilder
        client = MysqlClient()
        client.connect()
        mysql_builder = MySQLBuilder(client)
        mysql_builder.create_user(self.username, self.password, self.email)
        client.connection.close()

    # @allure.story('Тестирование данных сгенерированных при помощи Faker.')
    # PASS
    def test_main_page(self):
        # self.fuoo(username, password, email)
        self.auth_page.login(self.username, self.password)
        assert self.driver.current_url == 'http://127.0.0.1:8080/welcome/'