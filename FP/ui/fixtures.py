import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.auth_page import AuthPage
from ui.pages.reg_page import RegPage
from webdriver_manager.chrome import ChromeDriverManager


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def auth_page(driver):
    return AuthPage(driver=driver)


@pytest.fixture
def reg_page(driver):
    return RegPage(driver=driver)


def get_driver(config, download_dir):
    browser_name = config['browser']
    selenoid = config['selenoid']
    vnc = config['vnc']
    enable_video = config['enable_video']

    if browser_name == 'chrome':
        options = ChromeOptions()

        if selenoid is not None:
            options.add_experimental_option("prefs", {"download.default_directory": '/home/selenoid/Downloads'})
            options.add_experimental_option("prefs", {"profile.default_content_settings.popups": 0})
            options.add_experimental_option("prefs", {"download.prompt_for_download": False})
            caps = {'browserName': browser_name,
                    'version': '89.0',
                    'sessionTimeout': '2m'}

            if vnc:
                caps['version'] += '_vnc'
                caps['enableVNC'] = True

            if enable_video:
                caps['enableVideo'] = True

            browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)

        else:
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})
            manager = ChromeDriverManager(version='latest', log_level=0)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')

    return browser


@pytest.fixture(scope='function', autouse=True)
def driver(config, test_dir):
    url = config['url']
    browser = get_driver(config, download_dir=test_dir)
    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)
        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")
        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)


def make_screenshot(request):
    driver = request.getfixturevalue('driver')
    test_dir = request.getfixturevalue('test_dir')
    screenshot_file = os.path.join(test_dir, 'not_faded_failure.png')
    driver.get_screenshot_as_file(screenshot_file)
    allure.attach.file(screenshot_file, 'not_faded_failure.png', attachment_type=allure.attachment_type.PNG)

# @pytest.fixture(scope='class')
# def connect_to_db():
#     from clients.db_client import MysqlClient
#     client = MysqlClient()
#     client.connect()
#     yield client
#     client.connection.close()


@pytest.fixture(scope='class')
def clear_reg_table():
    from clients.db_client import MysqlClient
    client = MysqlClient()
    client.connect()
    client.execute_query('truncate test_users;', False)
    client.connection.close()

