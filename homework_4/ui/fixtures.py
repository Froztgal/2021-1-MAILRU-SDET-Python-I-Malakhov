import os
import allure
import pytest
from ui import pages
from appium import webdriver
from selenium import webdriver as wd
from ui.pages.base_page import BasePage
from ui.capability import capability_select
from webdriver_manager.chrome import ChromeDriverManager


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver, config):
    return BasePage(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    page = get_page(config['device_os'], 'MainPage')
    return page(driver=driver, config=config)


@pytest.fixture
def menu_page(driver, config):
    page = get_page(config['device_os'], 'MenuPage')
    return page(driver=driver, config=config)


@pytest.fixture
def news_source_page(driver, config):
    page = get_page(config['device_os'], 'NewsSourcePage')
    return page(driver=driver, config=config)


@pytest.fixture
def about_app_page(driver, config):
    page = get_page(config['device_os'], 'AboutAppPage')
    return page(driver=driver, config=config)


def get_page(device, page_class):
    if device == 'mw':
        page_class += 'MW'
    elif device == 'android':
        page_class += 'ANDROID'

    page = getattr(pages, page_class, None)
    if page is None:
        raise Exception(f'No such page {page_class}')
    return page


def get_driver(browser_name, device_os, appium_url, download_dir):
    if device_os in ['web', 'mw']:
        manager = ChromeDriverManager(version='latest')
        if browser_name == 'chrome':
            browser = wd.Chrome(executable_path=manager.install(),
                                options=capability_select(device_os, download_dir))
        elif device_os == 'mw':
            browser = wd.Chrome(executable_path=manager.install(),
                                options=capability_select(device_os, download_dir))
        else:
            raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')
    elif device_os == 'android':
        desired_caps = capability_select(device_os, '')
        driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
        return driver
    else:
        raise UnsupportedBrowserType(f' Unsupported device_os type {device_os}')
    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser_name = config['browser']
    device_os = config['device_os']
    appium_url = config['appium']
    browser = get_driver(browser_name, device_os, appium_url, test_dir)
    if device_os != 'android':
        browser.get(url)
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
        if config['device_os'] != 'android':
            browser_logfile = os.path.join(test_dir, 'browser.log')
            with open(browser_logfile, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

            with open(browser_logfile, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)