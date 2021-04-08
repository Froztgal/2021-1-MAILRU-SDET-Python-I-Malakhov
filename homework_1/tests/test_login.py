import pytest
from homework_1.tests.base import BaseCase


class TestLogIn(BaseCase):
    @pytest.mark.UI("UI")
    def test_login(self, login):
        assert self.driver.current_url.find("dashboard") >= 0
