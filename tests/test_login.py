import pytest
from tests.base import BaseCase


class TestLogIn(BaseCase):
    @pytest.mark.UI("UI")
    def test_login(self, login):
        assert self.driver.current_url.find("dashboard") >= 0
