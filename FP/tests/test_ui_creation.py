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


@allure.feature('Тесты на создание пользователей на странице регистрации.')
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

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}.')
    def test_basic(self, ui_report, username, password, email):
        """
        Что тестирует - проверяет, что пользователь может зарегистрироваться с валидными данными;
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь зарегистрировался и попал на главную страницу, если данные валидны.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        assert self.driver.current_url == self.main_page.url

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. Без '
                  'галочки в чекбоксе.')
    def test_without_checkbox(self, ui_report, username, password, email):
        """
        Что тестирует - проверяет, что пользователь не может зарегистрироваться с валидными данными, если он не
        отметил галочку в чекбоксе;
        Шаги выполнения - ввод данных в поля на странице регистрации, без галочки, проверка страницы;
        Ожидаемый результат - пользователь не зарегистрировался и не попал на главную страницу.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email, chekbox=False)
        assert self.driver.current_url == self.reg_page.url

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. '
                  'Неверно введен пароль повторно.')
    def test_wrong_re_password(self, ui_report, username, password, email):
        """
        Что тестирует - проверяет, что пользователь не может зарегистрироваться с валидными данными, если он ввел
        неверно пароль повторно;
        Шаги выполнения - ввод данных в поля на странице регистрации, повторно пароль вводиться неверно,
        проверка страницы;
        Ожидаемый результат - пользователь не зарегистрировался и не попал на главную страницу.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email, re_password='not_password')
        text = self.reg_page.get_flash_information()
        assert text == 'Passwords must match'

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. Баг '
                  '- Internal Server Error (500)!')
    def test_existent_email(self, ui_report, username, password, email):
        """
        Что тестирует - проверяет, что пользователь не может зарегистрироваться с валидными данными, если он ввел
        уже зарегестрированную почту;
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь не зарегистрировался и не попал на главную страницу.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        assert self.driver.current_url == self.main_page.url
        self.main_page.go_to_login_page()
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user('new' + username, password, email)
        text = self.reg_page.get_flash_information()
        assert text == 'Internal Server Error'
        assert 0

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. '
                  'Такой пользователь уже существует.')
    def test_existent_username(self, ui_report, username, password, email):
        """
        Что тестирует - проверяет, что пользователь не может зарегистрироваться с валидными данными, если он ввел
        уже зарегестрированное имя пользователя;
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь не зарегистрировался и не попал на главную страницу.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        assert self.driver.current_url == self.main_page.url
        self.main_page.go_to_login_page()
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, 'new' + email)
        text = self.reg_page.get_flash_information()
        assert text == 'User already exist'

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. '
                  'Различные длинны для username (валидные от 6 до 16 символов).')
    def test_username_length(self, ui_report, username, password, email, valid):
        """
        Что тестирует - проверяет, что пользователь может зарегистрироваться с валидными данными (по длинне username);
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь зарегистрировался и попал на главную страницу, если данные валидны.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url == self.reg_page.url

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. '
                  'Различные длинны для password (валидные от 1 до 255 символов).')
    def test_password_length(self, ui_report, username, password, email, valid):
        """
        Что тестирует - проверяет, что пользователь может зарегистрироваться с валидными данными (по длинне password);
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь зарегистрировался и попал на главную страницу, если данные валидны.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url == self.reg_page.url

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. '
                  'Различные длинны для email (валидные от 4 до 64 символов).')
    def test_email_length(self, ui_report, username, password, email, valid):
        """
        Что тестирует - проверяет, что пользователь может зарегистрироваться с валидными данными (по длинне email);
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь зарегистрировался и попал на главную страницу, если данные валидны.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            text = self.reg_page.get_flash_information()
            assert text == 'Incorrect email length'

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. Баг '
                  '- Internal Server Error (500)!')
    def test_rus_data(self, ui_report, username, password, email):
        """
        Что тестирует - проверяет, что пользователь не может зарегистрироваться с данными на русском языке;
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь не зарегистрировался и не попал на главную страницу.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        text = self.reg_page.get_flash_information()
        assert text == 'Internal Server Error'

    @allure.story('Тест на добавление пользователя c username: {username}, password: {password}, email: {email}. '
                  'Данные содержат пробелы.')
    def test_spaces_data(self, ui_report, username, password, email, valid):
        """
        Что тестирует - проверяет, что пользователь может зарегистрироваться с данными с пробелами;
        Шаги выполнения - ввод данных в поля на странице регистрации, проверка страницы;
        Ожидаемый результат - пользователь зарегистрировался и попал на главную страницу.
        """
        self.auth_page.go_to_create_account_page()
        self.reg_page.create_user(username, password, email)
        if valid:
            assert self.driver.current_url == self.main_page.url
        else:
            assert self.driver.current_url == self.reg_page.url
