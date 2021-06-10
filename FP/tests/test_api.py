import json
import pytest
import allure
from sql_models.models import TestUsers


@pytest.fixture(scope='function', autouse=True)
def login_as_superuser(api_client):
    api_client.post_login('superuser', 'superuser')


@allure.feature('Тесты API.')
@pytest.mark.API
class TestAPI:

    @staticmethod
    def table_assertion(res, username, password, email, access=1, active=0, start_active_time=None):
        assert res.username == username
        assert res.password == password
        assert res.email == email
        assert res.access == access
        assert res.active == active
        assert res.start_active_time == start_active_time

    @allure.story('Тест на добавление пользователя.')
    @allure.title('Баг - неверный статус код!')
    def test_add_user(self, api_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на добавление
        пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка ответа;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ.
        """
        res = api_client.post_add_user('username0', 'password0', 'a0b@c.d')
        assert res.status_code == 201

    @allure.story('Тест на добавление существующего пользователя.')
    def test_add_existent_user(self, api_client, db_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на добавление
        существующего пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка добавления пользователя в БД,
        повторная отправка POST запроса на добавление пользователя, проверка ответа и того что пользователь в БД один;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ, в БД один пользователь с таким именем.
        """
        api_client.post_add_user('username1', 'password1', 'a1b@c.d')
        res = db_client.session.query(TestUsers).filter_by(username='username1').first()
        db_client.session.commit()
        self.table_assertion(res, 'username1', 'password1', 'a1b@c.d')
        res = api_client.post_add_user('username1', 'password1', 'a1b@c.d')
        assert res.status_code == 304
        res = db_client.session.query(TestUsers).filter_by(username='username1').all()
        db_client.session.commit()
        assert len(res) == 1

    @allure.story('Тест на добавление пользователя.')
    def test_add_user_without_status_code(self, api_client, db_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на добавление
        пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка добавления пользователя в БД;
        Ожидаемый результат - Пользователь добавлен в БД.
        """
        api_client.post_add_user('username2', 'password2', 'a2b@c.d')
        res = db_client.session.query(TestUsers).filter_by(username='username2').first()
        db_client.session.commit()
        self.table_assertion(res, 'username2', 'password2', 'a2b@c.d')

    @allure.story('Тест на удаление пользователя.')
    def test_del_user(self, api_client, db_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на удаление
        существующего пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка добавления пользователя в БД,
        отправка GET запроса на удаление пользователя, проверка ответа и того что пользователь удален из БД;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ, в БД пользователя нет.
        """
        api_client.post_add_user('username3', 'password3', 'a3b@c.d')
        res = db_client.session.query(TestUsers).filter_by(username='username3').first()
        db_client.session.commit()
        self.table_assertion(res, 'username3', 'password3', 'a3b@c.d')
        res = api_client.get_del_user('username3')
        assert res.status_code == 204
        res = db_client.session.query(TestUsers).filter_by(username='username3').all()
        db_client.session.commit()
        assert len(res) == 0

    @allure.story('Тест на блокировку пользователя.')
    def test_block_user(self, api_client, db_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на блокировку
        существующего пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка добавления пользователя в БД,
        отправка GET запроса на блокировку пользователя, проверка ответа и того что пользователь заблокирован в БД;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ, в БД пользователь заблокирован.
        """
        api_client.post_add_user('username4', 'password4', 'a4b@c.d')
        res = db_client.session.query(TestUsers).filter_by(username='username4').first()
        db_client.session.commit()
        self.table_assertion(res, 'username4', 'password4', 'a4b@c.d')
        res = api_client.get_block_user('username4')
        assert res.status_code == 200
        res = db_client.session.query(TestUsers).filter_by(username='username4').first()
        db_client.session.commit()
        assert res.access == 0

    @allure.story('Тест на разблокировку пользователя.')
    def test_unblock_user(self, api_client, db_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на разблокировку
        существующего пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка добавления пользователя в БД,
        отправка GET запроса на блокировку пользователя, проверка ответа и того что пользователь заблокирован в БД,
        отправка GET запроса на разблокировку пользователя, проверка ответа и того что пользователь раззаблокирован в
        БД;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ, в БД пользователь раззаблокирован.
        """
        api_client.post_add_user('username5', 'password5', 'a5b@c.d')
        res = db_client.session.query(TestUsers).filter_by(username='username5').first()
        db_client.session.commit()
        self.table_assertion(res, 'username5', 'password5', 'a5b@c.d')
        res = api_client.get_block_user('username5')
        assert res.status_code == 200
        res = db_client.session.query(TestUsers).filter_by(username='username5').first()
        db_client.session.commit()
        assert res.access == 0
        res = api_client.get_unblock_user('username5')
        assert res.status_code == 200
        res = db_client.session.query(TestUsers).filter_by(username='username5').first()
        db_client.session.commit()
        assert res.access == 1

    @allure.story('Тест на получение статуса приложения.')
    def test_app_status(self, api_client):
        """
        Что тестирует - проверяет, что API запрос, на получение статуса приложения, отрабатывает корректно;
        Шаги выполнения - отправка GET запроса на получение статуса приложения, проверка ответа;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ.
        """
        res = api_client.get_app_status()
        assert res.status_code == 200
        assert json.loads(res.content)['status'] == 'ok'

    @allure.story('Тест на код 404.')
    def test_404(self, api_client):
        """
        Что тестирует - проверяет, что API запросы, отправленный авторизованным пользователем, на удаление, блокировку и
        разблокировку несуществующего пользователя отрабатывают корректно;
        Шаги выполнения - отправка GET запроса на удаление пользователя, проверка ответа, отправка GET запроса на
        блокировку пользователя, проверка ответа, отправка GET запроса на разблокировку пользователя, проверка ответа;
        Ожидаемый результат - в ответ на запросы пришел корректный ответ.
        """
        res = api_client.get_del_user('username6')
        assert res.status_code == 404
        res = api_client.get_block_user('username6')
        assert res.status_code == 404
        res = api_client.get_unblock_user('username6')
        assert res.status_code == 404

    @allure.story('Тест на добавление пользователя.')
    @allure.title('Баг - невалидные данные пользователя!')
    def test_add_user_bad(self, api_client, db_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный авторизованным пользователем, на добавление невалидного
        пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление невалидного пользователя, проверка добавления
        пользователя в БД;
        Ожидаемый результат - Пользователь не добавлен в БД.
        """
        api_client.post_add_user('0', '0', 'a@b.c')
        res = db_client.session.query(TestUsers).filter_by(username='0').all()
        db_client.session.commit()
        assert len(res) == 0

    @allure.story('Тест на добавление пользователя неавторизованным пользователем.')
    def test_add_user_no_authorize(self, api_client):
        """
        Что тестирует - проверяет, что API запрос, отправленный неавторизованным пользователем, на добавление
        пользователя отрабатывает корректно;
        Шаги выполнения - отправка POST запроса на добавление пользователя, проверка ответа;
        Ожидаемый результат - в ответ на запрос пришел корректный ответ.
        """
        api_client.get_logout()
        res = api_client.post_add_user('username7', 'password7', 'a7b@c.d')
        assert res.status_code == 401
