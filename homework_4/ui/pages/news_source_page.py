import allure
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPageANDROID
from ui.pages.menu_page import MenuPageANDROID
from ui.locators.locators_android import NewsSourcePageANDROIDLocators


class NewsSourcePageANDROID(BasePage, MainPageANDROID, MenuPageANDROID):
    locators = NewsSourcePageANDROIDLocators()

    @allure.step("Выбираем необходимый источник новостей...")
    def click_on_needed_news_source(self):
        self.click_for_android(self.locators.NEEDED_NEWS_SOURCE)

    def choose_and_chek(self):
        self.main_page.click_on_menu_button()
        self.menu_page.go_to_news_settings()
        self.click_on_needed_news_source()
        assert self.find(self.locators.CHECK_NEEDED_NEWS_SOURCE)

    def one_more_check(self):
        self.main_page.find_text('News')
        self.driver.press_keycode(85)  # Не знаю насколько это нужно, так и не понял в чем проблема с взаимодействиями
        # при включенном аудио, но вроде с это строкой работает быстрее.
        assert self.main_page.find(self.main_page.locators.CHECK_NEWS).text == 'Вести ФМ'


