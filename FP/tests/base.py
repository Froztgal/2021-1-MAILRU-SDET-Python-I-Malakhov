import time

import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.auth_page import AuthPage
from ui.pages.main_page import MainPage
from ui.pages.reg_page import RegPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, api_client):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.api_client = api_client

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.auth_page: AuthPage = request.getfixturevalue('auth_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.reg_page: RegPage = request.getfixturevalue('reg_page')

        self.logger.debug('Initial setup done!')

    @pytest.fixture(scope='function')
    def login(self, api_client):
        self.auth_page.login('superuser', 'superuser')
