import os
import re
import allure
from ui.pages.base_page import BasePage
from ui.locators.locators_android import AboutAppPageANDROIDLocators


class AboutAppPageANDROID(BasePage):
    locators = AboutAppPageANDROIDLocators()

    @allure.step("Получаем информацию о версии программы...")
    def get_version(self):
        return self.find(self.locators.ABOUT_VERSION_TEXT).text

    @allure.step("Получаем копирайт программы...")
    def get_copyright(self):
        return self.find(self.locators.ABOUT_COPYRIGHT_TEXT).text

    @staticmethod
    def get_app_version():
        full_path = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'apk', 'Marussia_v1.39.1.apk')
        apk_name = full_path.split(os.path.sep)[-1]
        return 'Версия ' + re.findall(r'Marussia_v(.+).apk', apk_name)[0]
