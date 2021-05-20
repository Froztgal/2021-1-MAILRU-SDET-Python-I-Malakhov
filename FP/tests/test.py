import os
import data
import pytest
import allure
from tests.base import BaseCase
from ui.pages.base_page import PageNotLoadedException


@allure.feature('Тесты логина.')
@pytest.mark.UI
class TestLogin(BaseCase):

    @allure.story('Негативный тест на логин (неправильный формат email).')
    @allure.description("""
    Тест производит ввод некорректного логина (негативный).
    """)
    def test_login_negative_email(self):
        with pytest.raises(PageNotLoadedException):
            self.auth_page.login(email='abc@mail', password=data.password)
        assert self.base_page.find(self.auth_page.locators.INVALID_DATA_1).text == 'Введите email или телефон'

    @allure.story('Негативный тест на логин (неправильный пароль).')
    @allure.description("""
        Тест производит ввод некорректного пароля (негативный).
        """)
    def test_login_negative_password(self):
        with pytest.raises(PageNotLoadedException):
            self.auth_page.login(email=data.email, password='1234')
        assert self.base_page.find(self.auth_page.locators.INVALID_DATA_2).text == 'Invalid login or password'


@allure.feature('Тесты компаний.')
@pytest.mark.UI
class TestCompany(BaseCase):

    @pytest.fixture(scope='function')
    def file_path(self, repo_root):
        return os.path.join(repo_root, 'ui', 'test_img.jpg')

    @allure.story('Тест на создание компании.')
    @allure.description(
        "Тест производит создание новой компании и проверку ее наличия.")
    def test_creation(self, login, file_path):
        name = data.get_random_name()
        main_page = login
        creation_company_page = main_page.go_to_company_creation()
        creation_company_page.create_company(name, file_path)
        creation_company_page.is_complete()
        creation_company_page.check_company(name)


@allure.feature('Тесты аудиторий.')
@pytest.mark.UI
class TestAudience(BaseCase):

    @pytest.fixture(scope='function')
    def _create_segment(self, login):
        name = data.get_random_name()
        audience_page = login.go_to_audience()
        audience_page.create_segment(name)
        return name, audience_page

    @allure.story('Тест на создание сегмента аудитории.')
    @allure.description(
        "Тест производит создание нового семента аудитории и проверку его наличия.")
    def test_creation(self, _create_segment):
        name, page = _create_segment
        tmp = page.check_segment(name)
        assert tmp is not None

    @allure.story('Тест на удаление сегмента аудитории.')
    @allure.description("""Тест производит создание нового семента аудитории, проверку его наличия,
    удаление созданного сегмента и проверку того что сегмент удален.""")
    def test_delete(self, _create_segment):
        name, page = _create_segment
        seg_id = page.delete_segment(name)
        self.driver.refresh()
        page.is_complete()
        tmp = page.check_segment(seg_id)
        assert tmp is None
