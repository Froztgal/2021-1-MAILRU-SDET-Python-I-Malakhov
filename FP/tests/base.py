import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.auth_page import AuthPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.auth_page: AuthPage = request.getfixturevalue('auth_page')

        self.logger.debug('Initial setup done!')

    @pytest.fixture(scope='function')
    def login(self):
        return self.auth_page.login()
