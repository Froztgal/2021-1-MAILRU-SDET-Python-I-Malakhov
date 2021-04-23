import allure
from ui.pages.base_page import BasePage
from ui.locators.locators_android import NewsSourcePageANDROIDLocators


# class NewsSourcePage(BasePage):
#
#     def click_on_needed_news_source(self):
#         pass


class NewsSourcePageANDROID(BasePage):
    locators = NewsSourcePageANDROIDLocators()

    @allure.step("Выбираем необходимый источник новостей...")
    def click_on_needed_news_source(self):
        self.click_for_android(self.locators.NEEDED_NEWS_SOURCE)
