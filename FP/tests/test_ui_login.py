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


@allure.feature('Тесты на вход пользователей.')
@pytest.mark.usefixtures('clear_reg_table')
@pytest.mark.UI  # skip / UI
class TestLogin(BaseCase):
    from data import get_random_string
    from faker import Faker
    from faker.providers import internet
    fake = Faker()
    fake.add_provider(internet)

    params = {
        "test_login_data": [dict(username='username', password='password', email='ab@c.d'),
                       dict(username=''.join('1' for i in range(6)), password='password', email=fake.email()),
                       dict(username=''.join('1' for i in range(16)), password='password', email=fake.email()),
                       dict(username=get_random_string(), password='1', email=fake.email()),
                       dict(username=get_random_string(), password=''.join('1' for i in range(255)),
                            email=fake.email()),
                       dict(username=get_random_string(), password='password', email=''.join('a' for i in range(58))
                                                                                     + 'ab@c.d'),
                       dict(username='   1   ', password=fake.password(), email=fake.email()),
                       dict(username=' username ', password=fake.password(), email=fake.email()),
                       dict(username=get_random_string(), password=' password ', email=fake.email())
                       ]
    }

    def add_user_to_table(self, username, password, email):
        from clients.db_client import MysqlClient
        from builders import MySQLBuilder
        client = MysqlClient()
        client.connect()
        mysql_builder = MySQLBuilder(client)
        mysql_builder.create_user(username, password, email)
        client.connection.close()

    # @allure.story('Тестирование данных сгенерированных при помощи Faker.')
    # PASS
    def test_login_data(self, username, password, email):
        self.add_user_to_table(username, password, email)
        self.auth_page.login(username, password)
        assert self.driver.current_url == 'http://127.0.0.1:8080/welcome/'