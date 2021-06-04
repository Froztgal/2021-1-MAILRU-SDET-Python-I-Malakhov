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


@pytest.fixture
def block_superuser(db_client):
    db_client.session.query(TestUsers).filter(TestUsers.id == 1).update({TestUsers.access: 0})
    yield db_client
    db_client.session.query(TestUsers).filter(TestUsers.id == 1).update({TestUsers.access: 0})


@allure.feature('Тесты главной страницы.')
@pytest.mark.UI
class TestMain(BaseCase):

    # @pytest.mark.skip
    def test_main_logout_when_blocked(self, ui_report, login, block_superuser):
        """
        Что тестирует - проверяет, что авторизованный пользователь после блокировки, и обновления страницы вылетает
        на страницу авторизации;
        Шаги выполнения - блокировка авторизованного пользователя, обновление страницы, проверка страницы;
        Ожидаемый результат - пользователь вылетел на страницу авторизации.
        """
        self.driver.refresh()
        assert self.driver.current_url == self.auth_page.url

    @pytest.mark.skip
    def test_main_page_logout(self, ui_report, login):
        """
        Что тестирует - проверяет, что авторизованный пользователь после нажатия на кнопку Logout попадает на
        страницу авторизации;
        Шаги выполнения - нажатие на кнопку Logout, проверка страницы;
        Ожидаемый результат - пользователь попал на страницу авторизации.
        """
        self.main_page.go_to_login_page()
        assert self.driver.current_url == self.auth_page.url

    @pytest.mark.skip
    def test_main_page_go_to_home_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку HOME попадает на главную страницу;
        Шаги выполнения - нажатие на кнопку HOME, проверка страницы;
        Ожидаемый результат - пользователь ппопал на главную страницу.
        """
        self.main_page.go_to_home_page()
        assert self.driver.current_url == self.main_page.url

    @pytest.mark.skip
    def test_main_page_go_to_python_main_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Python попадает на страницу Python;
        Шаги выполнения - нажатие на кнопку Python, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Python.
        """
        self.main_page.go_to_python_main_page()
        assert self.driver.current_url == 'https://www.python.org/'

    @pytest.mark.skip
    def test_main_page_go_to_python_history_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Python history попадает на страницу
        Python history;
        Шаги выполнения - нажатие на кнопку Python history, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Python history.
        """
        self.main_page.go_to_python_history_page()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/History_of_Python'

    @pytest.mark.skip
    def test_main_page_go_to_python_flask_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку About Flask попадает на страницу
        About Flask;
        Шаги выполнения - нажатие на кнопку About Flask, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу About Flask.
        """
        self.main_page.go_to_python_flask_page()
        # https://palletsprojects.com/p/flask/
        assert self.driver.current_url == 'https://flask.palletsprojects.com/en/1.1.x/#'

    @pytest.mark.skip
    def test_main_page_go_to_linux_centos_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Download Centos7 попадает на страницу
        Download Centos7;
        Шаги выполнения - нажатие на кнопку Download Centos7, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Download Centos7.
        """
        self.main_page.go_to_linux_centos_page()
        # https://www.centos.org/download/
        assert self.driver.current_url == 'https://getfedora.org/ru/workstation/download/'

    @pytest.mark.skip
    def test_main_page_go_to_network_wireshark_news_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Network-Wireshark-News попадает на страницу
        Wireshark-News;
        Шаги выполнения - нажатие на кнопку Wireshark-News, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Wireshark-News.
        """
        self.main_page.go_to_network_wireshark_news_page()
        assert self.driver.current_url == 'https://www.wireshark.org/news/'

    @pytest.mark.skip
    def test_main_page_go_to_network_wireshark_download_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Network-Wireshark-Download попадает на
        страницу Wireshark-Download;
        Шаги выполнения - нажатие на кнопку Wireshark-Download, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Wireshark-Download.
        """
        self.main_page.go_to_network_wireshark_download_page()
        assert self.driver.current_url == 'https://www.wireshark.org/#download'

    @pytest.mark.skip
    def test_main_page_go_to_network_tcpdump_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Network-TCPDUMP-Examples попадает на
        страницу TCPDUMP-Examples;
        Шаги выполнения - нажатие на кнопку TCPDUMP-Examples, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу TCPDUMP-Examples.
        """
        self.main_page.go_to_network_tcpdump_page()
        assert self.driver.current_url == 'https://hackertarget.com/tcpdump-examples/'

    @pytest.mark.skip
    def test_main_page_go_to_api_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку 'What is an API?' попадает на
        страницу API;
        Шаги выполнения - нажатие на кнопку 'What is an API?', проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу API.
        """
        self.main_page.go_to_api_page()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/API'

    @pytest.mark.skip
    def test_main_page_go_to_internet_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку 'Future of internet' попадает на
        страницу internet;
        Шаги выполнения - нажатие на кнопку 'Future of internet', проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу internet.
        """
        self.main_page.go_to_internet_page()
        assert self.driver.current_url == 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'

    @pytest.mark.skip
    def test_main_page_go_to_smtp_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку 'Lets talk about SMTP?' попадает на
        страницу SMTP;
        Шаги выполнения - нажатие на кнопку 'Lets talk about SMTP?', проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу SMTP.
        """
        self.main_page.go_to_smtp_page()
        assert self.driver.current_url == 'https://ru.wikipedia.org/wiki/SMTP'

    @pytest.mark.skip
    def test_main_page_logged_user(self, ui_report, login):
        """
        Что тестирует - проверяет, что на главной странице отображается корректная информация об авторизованном
        пользователе;
        Шаги выполнения - проверка информации об авторизованном пользователе;
        Ожидаемый результат - отображается корректная информация об авторизованном пользователе.
        """
        res = self.main_page.get_logged_username()
        assert res.text == 'Logged as superuser'

    @pytest.mark.skip
    def test_main_page_vk_id(self, mock_url, ui_report, login):
        """
        Что тестирует - проверяет, что на главной странице отображается корректная информация vk_id о пользователе;
        Шаги выполнения - проверка информации vk_id о пользователе;
        Ожидаемый результат - отображается корректная информация vk_id о пользователе.
        """
        res = self.main_page.get_vk_id(mock_url)
        assert res.text == 'Logged as superuser'