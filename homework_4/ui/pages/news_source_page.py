import allure
from ui.pages.main_page import MainPageANDROID
from ui.pages.menu_page import MenuPageANDROID
from ui.locators.locators_android import NewsSourcePageANDROIDLocators


class NewsSourcePageANDROID(MainPageANDROID, MenuPageANDROID):
    locators = NewsSourcePageANDROIDLocators()

    @allure.step("Выбираем необходимый источник новостей...")
    def click_on_needed_news_source(self):
        self.click_for_android(self.locators.NEEDED_NEWS_SOURCE)

    def choose_and_chek(self):
        self.click_on_menu_button()
        self.go_to_news_settings()
        self.click_on_needed_news_source()
        assert self.find(self.locators.CHECK_NEEDED_NEWS_SOURCE)

    def one_more_check(self):
        self.send_value_and_find_text('News')
        self.click_for_android(self.locators.STOP_PLAYER_BUTTON)
        assert self.find(self.locators.CHECK_NEWS).text == 'Вести ФМ'
