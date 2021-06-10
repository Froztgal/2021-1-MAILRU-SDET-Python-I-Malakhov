import pytest
import allure
from faker import Faker
from tests.base import BaseCase
from data import get_random_string
from faker.providers import internet
from sql_models.models import TestUsers

fake = Faker()
fake.add_provider(internet)


@pytest.fixture
def block_superuser(db_client):
    db_client.session.query(TestUsers).filter(TestUsers.id == 1).update({TestUsers.access: 0})
    db_client.session.commit()
    yield db_client
    db_client.session.query(TestUsers).filter(TestUsers.id == 1).update({TestUsers.access: 1})
    db_client.session.commit()


def pytest_generate_tests(metafunc):
    # вызывается один раз для каждой тестовой функции
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


@allure.feature('Тесты на вход пользователей на странице логина.')
@pytest.mark.UI
class TestLogin(BaseCase):

    params = {
        'test_login_blocked': [dict(username='superuser', password='superuser')],
        "test_login_data": [dict(username='username', password='password', email='ab@c.d', valid=True),
                            dict(username='', password='password', email=fake.email(), valid=False),
                            dict(username='1', password='password', email=fake.email(), valid=False),
                            dict(username=''.join('1' for i in range(5)), password='password', email=fake.email(),
                                 valid=False),
                            dict(username=''.join('1' for i in range(6)), password='password', email=fake.email(),
                                 valid=True),
                            dict(username=''.join('1' for i in range(16)), password='password', email=fake.email(),
                                 valid=True),
                            dict(username=get_random_string(), password='1', email=fake.email(), valid=True),
                            dict(username=get_random_string(), password='password',
                                 email=''.join('a' for i in range(58)) + 'ab@c.d',
                                 valid=True),
                            dict(username='   1   ', password=fake.password(), email=fake.email(), valid=True),
                            dict(username=' username ', password=fake.password(), email=fake.email(), valid=True),
                            dict(username=get_random_string(), password='      ', email=fake.email(), valid=False),
                            dict(username=get_random_string(), password=' password ', email=fake.email(), valid=True),
                            dict(username=get_random_string(), password=fake.password(), email=' ab@c.d ', valid=False)
                            ]
    }

    @allure.story('Тест на логин заблокированного пользователя c username: {username}, password: {password}.')
    def test_login_blocked(self, ui_report, block_superuser, username, password):
        """
        Что тестирует - проверяет, что пользователь существующий в БД, но заблокированный, не может авторизоваться со
        своими данными;
        Шаги выполнения - ввод данных в поля на странице авторизации, проверка страницы;
        Ожидаемый результат - пользователь не вошел на страницу авторизации и получил сообщение об ошибке.
        """
        self.auth_page.login(username, password)
        assert self.driver.current_url == self.auth_page.url
        assert self.auth_page.get_error_text() == 'Ваша учетная запись заблокирована'

    @allure.story('Тест на логин пользователя c username: {username}, password: {password}, email: {email}.')
    @allure.title('Баг - пользователь с невалидной почтой может войти, если такая почта как то попала в БД!')
    def test_login_data(self, ui_report, my_builder, username, password, email, valid):
        """
        Что тестирует - проверяет, что пользователь существующий в БД, может авторизоваться со своими данными;
        Шаги выполнения - ввод данных в поля на странице авторизации, проверка страницы;
        Ожидаемый результат - пользователь вошел на страницу авторизации, если данные валидны.
        """
        my_builder.create_user(username, password, email)
        self.auth_page.login(username, password)
        self.auth_page.is_complete()
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url in [self.auth_page.url, self.base_page.url]
