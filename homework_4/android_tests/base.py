import pytest
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPageANDROID
from ui.pages.menu_page import MenuPageANDROID
from ui.pages.news_source_page import NewsSourcePageANDROID
from ui.pages.about_app_page import AboutAppPageANDROID
from _pytest.fixtures import FixtureRequest


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPageANDROID = request.getfixturevalue('main_page')
        self.menu_page: MenuPageANDROID = request.getfixturevalue('menu_page')
        self.news_source_page: NewsSourcePageANDROID = request.getfixturevalue('news_source_page')
        self.about_app_page: AboutAppPageANDROID = request.getfixturevalue('about_app_page')

        self.logger.debug('Initial setup done!')