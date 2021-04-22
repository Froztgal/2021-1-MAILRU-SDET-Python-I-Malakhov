import allure
from ui.pages.base_page import BasePage
from ui.locators.locators_android import MenuPageANDROIDLocators


class MenuPage(BasePage):

    def go_to_news_settings(self):
        pass

    def go_to_about_app(self):
        pass


class MenuPageANDROID(MenuPage):
    locators = MenuPageANDROIDLocators()

    @allure.step("Пролистываем до источника новостей и заходим в него...")
    def go_to_news_settings(self):
        self.swipe_to_element_up(self.locators.NEWS_SOURCE_BUTTON, 5)
        self.click_for_android(self.locators.NEWS_SOURCE_BUTTON)

    @allure.step("Пролистываем до раздела о приложении и заходим в него...")
    def go_to_about_app(self):
        self.swipe_to_element_up(self.locators.ABOUT_APP_BUTTON, 5)
        self.click_for_android(self.locators.ABOUT_APP_BUTTON)
