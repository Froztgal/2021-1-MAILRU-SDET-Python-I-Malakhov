import pytest
from tests.base import BaseCase
from ui.locators import basic_locators


class TestLogOut(BaseCase):
    @pytest.mark.UI("UI")
    def test_logout(self, login):
        self.click(basic_locators.LOGOUT_LOCATOR_1)
        self.click(basic_locators.LOGOUT_LOCATOR_2)
        assert self.driver.current_url == "https://target.my.com/"
