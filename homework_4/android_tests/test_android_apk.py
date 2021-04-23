import os
import re
import pytest
from base import BaseCase
from ui.locators import locators_android


def get_app_version():
    full_path = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'apk', 'Marussia_v1.39.1.apk')
    apk_name = full_path.split(os.path.sep)[-1]
    return 'Версия ' + re.findall(r'Marussia_v(.+).apk', apk_name)[0]


class TestApkAndroidMain(BaseCase):

    @pytest.mark.AndroidUI
    def test_search(self):
        self.main_page.find_text('Russia')
        self.main_page.hide_keyboard_button()
        assert self.main_page.find(locators_android.MainPageANDROIDLocators.RESULT_HEADER).text == 'Россия'
        self.main_page.find_and_swipe()
        self.main_page.click_on_suggestion()
        self.main_page.find(locators_android.MainPageANDROIDLocators.NEEDED_SUGGESTION)
        assert self.main_page.find(locators_android.MainPageANDROIDLocators.RESULT_HEADER).text == '146 млн.'

    @pytest.mark.AndroidUI
    def test_math(self):
        expression = '2**10'
        self.main_page.find_text(expression)
        assert self.main_page.find(locators_android.MainPageANDROIDLocators.math_expression_result_locator(
            expression)).text == str(eval(expression))


class TestApkAndroidSettings(BaseCase):
    @pytest.mark.test
    @pytest.mark.AndroidUI
    def test_news_source(self):
        self.main_page.click_on_menu_button()
        self.menu_page.go_to_news_settings()
        self.news_source_page.click_on_needed_news_source()
        assert self.news_source_page.find(locators_android.NewsSourcePageANDROIDLocators.CHECK_NEEDED_NEWS_SOURCE)
        self.driver.back()
        self.driver.back()
        self.main_page.find_text('News')
        self.driver.press_keycode(85) # Не знаю насколько это нужно, так и не понял в чем проблема с взаимодействиями
        # при включенном аудио, но вроде с это строкой работает быстрее.
        assert self.main_page.find(locators_android.MainPageANDROIDLocators.CHECK_NEWS).text == 'Вести ФМ'

    @pytest.mark.AndroidUI
    def test_about_app(self):
        app_version = get_app_version()
        self.main_page.click_on_menu_button()
        self.menu_page.go_to_about_app()
        assert self.about_app_page.get_version() == app_version
        assert 'Все права защищены.' in self.about_app_page.get_copyright()
