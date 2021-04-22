import allure
from ui.pages.base_page import BasePage
from ui.locators.locators_android import AboutAppPageANDROIDLocators


class AboutAppPage(BasePage):

    def get_version(self):
        pass

    def get_copyright(self):
        pass


class AboutAppPageANDROID(AboutAppPage):
    locators = AboutAppPageANDROIDLocators()

    @allure.step("Получаем информацию о версии программы...")
    def get_version(self):
        return self.find(self.locators.ABOUT_VERSION_TEXT).text

    @allure.step("Получаем копирайт программы...")
    def get_copyright(self):
        return self.find(self.locators.ABOUT_COPYRIGHT_TEXT).text
