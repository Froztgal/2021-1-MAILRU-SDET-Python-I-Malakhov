import pytest
import allure
from tests.base import BaseCase
from sql_models.models import TestUsers


@pytest.fixture(scope='function')
def block_superuser(db_client):
    db_client.session.query(TestUsers).filter(TestUsers.id == 1).update({TestUsers.access: 0})
    db_client.session.commit()
    yield db_client
    db_client.session.query(TestUsers).filter(TestUsers.id == 1).update({TestUsers.access: 1})
    db_client.session.commit()


@allure.feature('Тесты главной страницы.')
@pytest.mark.UI
class TestMain(BaseCase):

    @allure.story('Тест на разлогин забаненого пользователя, баг - в БД пользователь остается активен!')
    def test_main_logout_when_blocked(self, ui_report, login, block_superuser):
        """
        Что тестирует - проверяет, что авторизованный пользователь после блокировки, и обновления страницы вылетает
        на страницу авторизации и в БД его активность становится равна 0;
        Шаги выполнения - блокировка авторизованного пользователя, обновление страницы, проверка страницы, проверка БД;
        Ожидаемый результат - пользователь вылетел на страницу авторизации, в БД его активность равна 0.
        """
        self.driver.refresh()
        assert self.driver.current_url.find(self.auth_page.url) >= 0
        assert block_superuser.session.query(TestUsers).filter(TestUsers.id == 1).first().active == 0

    @allure.story('Тест на разлогин пользователя через кнопку.')
    def test_main_page_logout(self, ui_report, login, db_client):
        """
        Что тестирует - проверяет, что авторизованный пользователь после нажатия на кнопку Logout попадает на
        страницу авторизации;
        Шаги выполнения - нажатие на кнопку Logout, проверка страницы;
        Ожидаемый результат - пользователь попал на страницу авторизации.
        """
        self.main_page.go_to_login_page()
        assert self.driver.current_url == self.auth_page.url
        db_client.session.expire_all()
        assert db_client.session.query(TestUsers).filter(TestUsers.id == 1).first().active == 0

    @allure.story('Тест на нажатие кнопки HOME.')
    def test_main_page_go_to_home_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку HOME попадает на главную страницу;
        Шаги выполнения - нажатие на кнопку HOME, проверка страницы;
        Ожидаемый результат - пользователь ппопал на главную страницу.
        """
        self.main_page.go_to_home_page()
        assert self.driver.current_url == self.main_page.url

    @allure.story('Тест на нажатие кнопки Python.')
    def test_main_page_go_to_python_main_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Python попадает на страницу Python;
        Шаги выполнения - нажатие на кнопку Python, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Python.
        """
        self.main_page.go_to_python_main_page()
        assert self.driver.current_url == 'https://www.python.org/'

    @allure.story('Тест на нажатие кнопки Python->Python history.')
    def test_main_page_go_to_python_history_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Python history попадает на страницу
        Python history;
        Шаги выполнения - нажатие на кнопку Python history, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Python history.
        """
        self.main_page.go_to_python_history_page()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/History_of_Python'

    @allure.story('Тест на нажатие кнопки Python->About Flask, баг - эта страница скорее гайд, нежели о приложении!')
    def test_main_page_go_to_python_flask_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку About Flask попадает на страницу
        About Flask;
        Шаги выполнения - нажатие на кнопку About Flask, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу About Flask.
        """
        self.main_page.go_to_python_flask_page()
        # 'https://flask.palletsprojects.com/en/1.1.x/#'
        assert self.driver.current_url == 'https://palletsprojects.com/p/flask/'

    @allure.story('Тест на нажатие кнопки Linux->Download Centos7, баг - ссылка на Fedora, а не Centos!')
    def test_main_page_go_to_linux_centos_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Download Centos7 попадает на страницу
        Download Centos7;
        Шаги выполнения - нажатие на кнопку Download Centos7, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Download Centos7.
        """
        self.main_page.go_to_linux_centos_page()
        # 'https://getfedora.org/ru/workstation/download/'
        assert self.driver.current_url == 'https://www.centos.org/download/'

    @allure.story('Тест на нажатие кнопки Network->Wireshark->News.')
    def test_main_page_go_to_network_wireshark_news_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Network-Wireshark-News попадает на страницу
        Wireshark-News;
        Шаги выполнения - нажатие на кнопку Wireshark-News, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Wireshark-News.
        """
        self.main_page.go_to_network_wireshark_news_page()
        assert self.driver.current_url == 'https://www.wireshark.org/news/'

    @allure.story('Тест на нажатие кнопки Network->Wireshark->Download.')
    def test_main_page_go_to_network_wireshark_download_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Network-Wireshark-Download попадает на
        страницу Wireshark-Download;
        Шаги выполнения - нажатие на кнопку Wireshark-Download, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу Wireshark-Download.
        """
        self.main_page.go_to_network_wireshark_download_page()
        assert self.driver.current_url == 'https://www.wireshark.org/#download'

    @allure.story('Тест на нажатие кнопки Network->TCPDUMP->Examples.')
    def test_main_page_go_to_network_tcpdump_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку Network-TCPDUMP-Examples попадает на
        страницу TCPDUMP-Examples;
        Шаги выполнения - нажатие на кнопку TCPDUMP-Examples, проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу TCPDUMP-Examples.
        """
        self.main_page.go_to_network_tcpdump_page()
        assert self.driver.current_url == 'https://hackertarget.com/tcpdump-examples/'

    @allure.story('Тест на нажатие кнопки "What is an API?".')
    def test_main_page_go_to_api_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку 'What is an API?' попадает на
        страницу API;
        Шаги выполнения - нажатие на кнопку 'What is an API?', проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу API.
        """
        self.main_page.go_to_api_page()
        assert self.driver.current_url == 'https://en.wikipedia.org/wiki/API'

    @allure.story('Тест на нажатие кнопки "Future of internet".')
    def test_main_page_go_to_internet_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку 'Future of internet' попадает на
        страницу internet;
        Шаги выполнения - нажатие на кнопку 'Future of internet', проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу internet.
        """
        self.main_page.go_to_internet_page()
        assert self.driver.current_url == 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'

    @allure.story('Тест на нажатие кнопки "Lets talk about SMTP?".')
    def test_main_page_go_to_smtp_page(self, ui_report, login):
        """
        Что тестирует - проверяет, что пользователь после нажатия на кнопку 'Lets talk about SMTP?' попадает на
        страницу SMTP;
        Шаги выполнения - нажатие на кнопку 'Lets talk about SMTP?', проверка страницы;
        Ожидаемый результат - пользователь ппопал на страницу SMTP.
        """
        self.main_page.go_to_smtp_page()
        assert self.driver.current_url == 'https://ru.wikipedia.org/wiki/SMTP'

    @allure.story('Тест на верное отображение залогинененого пользователя.')
    def test_main_page_logged_user(self, ui_report, login):
        """
        Что тестирует - проверяет, что на главной странице отображается корректная информация об авторизованном
        пользователе;
        Шаги выполнения - проверка информации об авторизованном пользователе;
        Ожидаемый результат - отображается корректная информация об авторизованном пользователе.
        """
        res = self.main_page.get_logged_username()
        assert res.text == 'Logged as superuser'

    @allure.story('Тест на верное отображение VK_ID пользователя.')
    def test_main_page_vk_id(self, ui_report, socket_client, login):
        """
        Что тестирует - проверяет, что на главной странице отображается корректная информация vk_id о пользователе;
        Шаги выполнения - проверка информации vk_id о пользователе;
        Ожидаемый результат - отображается корректная информация vk_id о пользователе.
        """
        id = 1234567890
        res = self.main_page.get_vk_id(socket_client, id)
        assert res.text == f'VK ID: {id}'
