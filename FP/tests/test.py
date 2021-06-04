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


class TestAPI:
    def test_add_user(self, api_client, db_client):
        # api_client.post_login('superuser', 'superuser')
        res = api_client.post_add_user('username1', 'password1', 'a1b@c.d')
        print(res.status_code)
        res = db_client.session.query(TestUsers).filter_by(username='username1').first()
        assert res.username == 'username1'
        assert res.password == 'password1'
        assert res.email == 'a1b@c.d'
        assert res.access == 1
        assert res.active == 0
        assert res.start_active_time is None


# class TestCreateUser(BaseCase):
#     def test_basic(self, ui_report, username='username', password='password', email='ab@c.d'):
#         self.auth_page.go_to_create_account_page()
#         self.reg_page.create_user(username, password, email)
#         self.reg_page.is_complete()
#         assert 0
#         assert self.driver.current_url == self.main_page.url
