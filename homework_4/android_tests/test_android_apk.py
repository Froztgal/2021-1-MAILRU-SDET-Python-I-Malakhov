import pytest
from base import BaseCase
from ui.locators import locators_android


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
    @pytest.mark.parametrize(
        "a,b,sign",
        [
            pytest.param(
                '2', '10', '**'
            ),
            pytest.param(
                '2', '10', '+'
            ),
        ],
    )
    def test_math(self, a, b, sign):
        expression = a + sign + b
        self.main_page.find_text(expression)
        assert self.main_page.find(locators_android.MainPageANDROIDLocators.math_expression_result_locator(
            expression)).text == str(eval(expression))


class TestApkAndroidSettings(BaseCase):
    @pytest.mark.test
    @pytest.mark.AndroidUI
    def test_news_source(self):
        self.news_source_page.choose_and_chek()
        self.base_page.back(2)
        self.news_source_page.one_more_check()

    @pytest.mark.AndroidUI
    def test_about_app(self):
        app_version = self.about_app_page.get_app_version()
        self.main_page.click_on_menu_button()
        self.menu_page.go_to_about_app()
        assert self.about_app_page.get_version() == app_version
        assert 'Все права защищены.' in self.about_app_page.get_copyright()
