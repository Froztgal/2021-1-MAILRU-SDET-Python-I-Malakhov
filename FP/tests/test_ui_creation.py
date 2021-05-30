import time

import pytest
import allure
from tests.base import BaseCase


def pytest_generate_tests(metafunc):
    # вызывается один раз для каждой тестовой функции
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


@allure.feature('Тесты на создание пользователей.')
@pytest.mark.usefixtures('clear_reg_table')
@pytest.mark.UI  # skip / UI
class TestCreateUser(BaseCase):
    from data import get_random_string
    from faker import Faker
    from faker.providers import internet
    fake = Faker()
    fake.add_provider(internet)

    params = {
        "test_basic": [dict(username='username', password='password', email='ab@c.d')],
        "test_without_checkbox": [dict(username=get_random_string(), password='password', email=fake.email())],
        "test_wrong_re_password": [dict(username=get_random_string(), password='password', email=fake.email())],
        "test_existent_email": [dict(username=get_random_string(), password='password', email=fake.email())],
        "test_existent_username": [dict(username=get_random_string(), password='password', email=fake.email())],
        "test_username_length": [
            dict(username='', password='password', email=fake.email(), valid=False),
            dict(username='1', password='password', email=fake.email(), valid=False),
            dict(username=''.join('1' for i in range(5)), password='password', email=fake.email(), valid=False),
            dict(username=''.join('1' for i in range(6)), password='password', email=fake.email(), valid=True),
            dict(username=''.join('1' for i in range(16)), password='password', email=fake.email(), valid=True),
            dict(username=''.join('1' for i in range(17)), password='password', email=fake.email(), valid=False)
        ],
        "test_password_length": [
            dict(username=get_random_string(), password='', email=fake.email(), valid=False),
            dict(username=get_random_string(), password='1', email=fake.email(), valid=True),
            dict(username=get_random_string(), password=''.join('1' for i in range(255)), email=fake.email(),
                 valid=True),
            dict(username=get_random_string(), password=''.join('1' for i in range(256)), email=fake.email(),
                 valid=False)
        ],
        "test_email_length": [
            dict(username=get_random_string(), password='password', email='', valid=False),
            dict(username=get_random_string(), password='password', email=''.join('a' for i in range(58)) + 'ab@c.d',
                 valid=True),
            dict(username=get_random_string(), password='password', email=''.join('a' for i in range(59)) + 'ab@c.d',
                 valid=False)
        ],
        "test_rus_data": [
            dict(username='Аркадий', password=fake.password(), email=fake.email()),
            dict(username=get_random_string(), password='Пароль', email=fake.email()),
            dict(username=get_random_string(), password=fake.password(), email='гусь@кусь.рф')
        ],
        "test_spaces_data": [
            dict(username='   1   ', password=fake.password(), email=fake.email(), valid=True),
            dict(username=' username ', password=fake.password(), email=fake.email(), valid=True),
            dict(username=get_random_string(), password='      ', email=fake.email(), valid=False),
            dict(username=get_random_string(), password=' password ', email=fake.email(), valid=True),
            dict(username=get_random_string(), password=fake.password(), email=' ab@c.d ', valid=False)
        ]
    }

    # @allure.story('Тестирование данных сгенерированных при помощи Faker.')
    # PASS
    def test_basic(self, username, password, email):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        assert self.driver.current_url == self.main_page.url

    # FAIL
    def test_without_checkbox(self, username, password, email):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email, chekbox=False)
        assert self.driver.current_url == self.reg_page.url

    # PASS
    def test_wrong_re_password(self, username, password, email):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email, re_password='not_password')
        text = self.reg_page.get_flash_information()
        assert text == 'Passwords must match'

    # PASS, but it's bug!
    def test_existent_email(self, username, password, email):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        assert self.driver.current_url == self.main_page.url
        self.main_page.go_to_login_page()
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user('new' + username, password, email)
        text = self.reg_page.get_flash_information()
        assert text == 'Internal Server Error'

    # PASS
    def test_existent_username(self, username, password, email):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        assert self.driver.current_url == self.main_page.url
        self.main_page.go_to_login_page()
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, 'new' + email)
        text = self.reg_page.get_flash_information()
        assert text == 'User already exist'

    # PASS
    def test_username_length(self, username, password, email, valid):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url == self.reg_page.url

    # PASS
    def test_password_length(self, username, password, email, valid):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url == self.reg_page.url

    # PASS
    def test_email_length(self, username, password, email, valid):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            text = self.reg_page.get_flash_information()
            assert text == 'Incorrect email length'

    # PASS, but it's bug!
    def test_rus_data(self, username, password, email):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        text = self.reg_page.get_flash_information()
        assert text == 'Internal Server Error'

    # PASS
    def test_spaces_data(self, username, password, email, valid):
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url == self.reg_page.url
