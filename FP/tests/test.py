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
from ui.fixtures import *


def get_app_ip_from_docker(name='mapp'):
    from docker import DockerClient
    client = DockerClient()
    container = client.containers.get(name)
    ip_add = container.attrs['NetworkSettings']['IPAddress']
    return ip_add


class TestCreateUser(BaseCase):
    def test_basic(self, request: FixtureRequest, username='username', password='password', email='ab@c.d'):
        ip_add = get_app_ip_from_docker()
        self.driver.get(f'http://{ip_add}:8080')
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        self.reg_page.is_complete()
        make_screenshot(request)
        assert self.driver.current_url == 'http://127.0.0.1:8080/welcome/'
