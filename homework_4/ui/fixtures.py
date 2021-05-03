import os
import allure
import pytest
from appium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPageANDROID
from ui.pages.menu_page import MenuPageANDROID
from ui.pages.about_app_page import AboutAppPageANDROID
from ui.pages.news_source_page import NewsSourcePageANDROID
from ui.capability import capability_select


class UnsupportedOS(Exception):
    pass


@pytest.fixture
def base_page(driver, config):
    return BasePage(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    return MainPageANDROID(driver=driver, config=config)


@pytest.fixture
def menu_page(driver, config):
    return MenuPageANDROID(driver=driver, config=config)


@pytest.fixture
def news_source_page(driver, config):
    return NewsSourcePageANDROID(driver=driver, config=config)


@pytest.fixture
def about_app_page(driver, config):
    return AboutAppPageANDROID(driver=driver, config=config)


def get_driver(device_os, appium_url):
    if device_os == 'android':
        desired_caps = capability_select(device_os, '')
        driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
        return driver
    else:
        raise UnsupportedOS(f' Unsupported device_os type {device_os}')


@pytest.fixture(scope='function')
def driver(config, test_dir):
    device_os = config['device_os']
    appium_url = config['appium']
    browser = get_driver(device_os, appium_url)
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)
