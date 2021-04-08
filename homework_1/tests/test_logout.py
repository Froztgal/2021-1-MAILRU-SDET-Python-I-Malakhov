import pytest
from homework_1.tests.base import BaseCase
from homework_1.ui.locators import basic_locators


class TestLogOut(BaseCase):
    @pytest.mark.UI("UI")
    def test_logout(self, login):
        self.click(basic_locators.LOGOUT_LOCATOR_1)
        self.click(basic_locators.LOGOUT_LOCATOR_2)
        assert self.driver.current_url == "https://target.my.com/"
