import pytest
from homework_1.tests.base import BaseCase
from homework_1.ui.locators import basic_locators


class TestParametrized(BaseCase):
    @pytest.mark.UI("UI")
    @pytest.mark.parametrize(
        "section, expected_section_url",
        [
            pytest.param(basic_locators.PRO_LOCATOR, "pro"),
            pytest.param(basic_locators.STATISTICS_LOCATOR, "statistics"),
        ],
    )
    def test_parametrized(self, login, section, expected_section_url):
        self.click(section)
        assert self.driver.current_url.find(expected_section_url) >= 0
