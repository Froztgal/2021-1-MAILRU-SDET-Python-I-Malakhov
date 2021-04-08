import pytest
import allure
import data
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.auth_page import AuthPage
from ui.pages.main_page import MainPage
from ui.locators.pages_locators import AuthPageLocators


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.auth_page: AuthPage = request.getfixturevalue('auth_page')

        self.logger.debug('Initial setup done!')

    @allure.step('Logging...')
    @pytest.fixture(scope='function')
    def login(self):
        self.auth_page.click(AuthPageLocators.LOGIN_LOCATOR_1)
        self.auth_page.fulfill(AuthPageLocators.EMAIL_FIELD_LOCATOR, data.email)
        self.auth_page.fulfill(AuthPageLocators.PASSWORD_FIELD_LOCATOR, data.password)
        self.auth_page.click(AuthPageLocators.LOGIN_LOCATOR_2)
        return MainPage(self.driver)
